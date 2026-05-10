from __future__ import annotations

import csv
import os
import smtplib
from datetime import datetime, timedelta
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import psycopg2
from airflow import DAG
from airflow.operators.python import PythonOperator


SMTP_HOST = os.getenv("AIRFLOW__SMTP__SMTP_HOST", "mailpit")
SMTP_PORT = int(os.getenv("AIRFLOW__SMTP__SMTP_PORT", "1025"))
SMTP_FROM = os.getenv("AIRFLOW__SMTP__SMTP_MAIL_FROM", "airflow@example.com")
REPORT_EMAIL_TO = os.getenv("REPORT_EMAIL_TO", "report@example.com")

DB_CONFIG = {
    "host": os.getenv("DATA_DB_HOST", "data_postgres"),
    "port": int(os.getenv("DATA_DB_PORT", "5432")),
    "dbname": os.getenv("DATA_DB_NAME", "sales_db"),
    "user": os.getenv("DATA_DB_USER", "datauser"),
    "password": os.getenv("DATA_DB_PASSWORD", "datapassword"),
}

QUERY = """
    SELECT
        id,
        product,
        category,
        quantity,
        unit_price,
        total_amount,
        sale_date,
        region,
        salesperson
    FROM sales_records
    ORDER BY sale_date DESC
"""

CSV_PATH = "/tmp/sales_report.csv"


def extract_to_csv(**context):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(QUERY)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()

    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)

    context["ti"].xcom_push(key="row_count", value=len(rows))


def send_email_report(**context):
    row_count = context["ti"].xcom_pull(key="row_count", task_ids="extract_to_csv")
    run_date = context["ds"]

    msg = MIMEMultipart()
    msg["From"] = SMTP_FROM
    msg["To"] = REPORT_EMAIL_TO
    msg["Subject"] = f"Sales Report — {run_date}"

    msg.attach(MIMEText(
        f"<h2>Daily Sales Report</h2>"
        f"<p><b>Date:</b> {run_date}</p>"
        f"<p><b>Records exported:</b> {row_count}</p>"
        f"<p>Please find the full report attached as a CSV file.</p>",
        "html",
    ))

    with open(CSV_PATH, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f'attachment; filename="sales_report_{run_date}.csv"',
        )
        msg.attach(part)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.sendmail(SMTP_FROM, REPORT_EMAIL_TO, msg.as_string())


default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="postgres_to_email_report",
    description="Query PostgreSQL, export to CSV, and email the report",
    schedule_interval=timedelta(seconds=20),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["report", "postgres", "email"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_to_csv",
        python_callable=extract_to_csv,
    )

    email_task = PythonOperator(
        task_id="send_email_report",
        python_callable=send_email_report,
    )

    extract_task >> email_task
