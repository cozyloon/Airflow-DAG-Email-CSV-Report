CREATE TABLE IF NOT EXISTS sales_records (
    id            SERIAL PRIMARY KEY,
    product       VARCHAR(100)   NOT NULL,
    category      VARCHAR(50)    NOT NULL,
    quantity      INTEGER        NOT NULL,
    unit_price    DECIMAL(10, 2) NOT NULL,
    total_amount  DECIMAL(10, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    sale_date     DATE           NOT NULL,
    region        VARCHAR(50)    NOT NULL,
    salesperson   VARCHAR(100)   NOT NULL
);

INSERT INTO sales_records (product, category, quantity, unit_price, sale_date, region, salesperson) VALUES
    ('Laptop Pro 15',       'Electronics',    5,  1299.99, '2024-01-15', 'North', 'Alice Johnson'),
    ('Wireless Mouse',      'Electronics',   25,    29.99, '2024-01-16', 'South', 'Bob Smith'),
    ('USB-C Hub',           'Electronics',   15,    49.99, '2024-01-17', 'East',  'Carol White'),
    ('Standing Desk',       'Furniture',      3,   799.99, '2024-01-18', 'West',  'David Brown'),
    ('Office Chair',        'Furniture',      8,   349.99, '2024-01-19', 'North', 'Eve Davis'),
    ('Monitor 27"',         'Electronics',   10,   459.99, '2024-01-20', 'South', 'Frank Miller'),
    ('Mechanical Keyboard', 'Electronics',   20,   129.99, '2024-01-21', 'East',  'Grace Wilson'),
    ('Webcam HD',           'Electronics',   12,    89.99, '2024-01-22', 'West',  'Henry Moore'),
    ('Desk Lamp',           'Office Supplies',30,   39.99, '2024-01-23', 'North', 'Iris Taylor'),
    ('Notebook Set',        'Office Supplies',50,   12.99, '2024-01-24', 'South', 'Jack Anderson'),
    ('Headphones Pro',      'Electronics',    7,   299.99, '2024-01-25', 'East',  'Karen Thomas'),
    ('Filing Cabinet',      'Furniture',      4,   249.99, '2024-01-26', 'West',  'Liam Jackson'),
    ('Printer Ink Set',     'Office Supplies',40,   24.99, '2024-01-27', 'North', 'Mia Harris'),
    ('External SSD 1TB',    'Electronics',   18,   119.99, '2024-01-28', 'South', 'Noah Martin'),
    ('Whiteboard Large',    'Office Supplies', 6,   89.99, '2024-01-29', 'East',  'Olivia Garcia');
