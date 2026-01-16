CREATE TABLE orders (
    row_id INT PRIMARY KEY,
    order_id VARCHAR(255),
    order_date DATE,
    ship_date DATE,
    ship_mode VARCHAR(255),
    customer_id VARCHAR(255),
    customer_name VARCHAR(255),
    segment VARCHAR(255),
    country VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(255),
    postal_code VARCHAR(20), -- Kept as string for leading zeros
    region VARCHAR(255),
    product_id VARCHAR(255),
    category VARCHAR(255),
    sub_category VARCHAR(255),
    product_name TEXT,
    sales DECIMAL(10, 2),
    quantity INT,
    discount DECIMAL(5, 2), -- Changed to 5,2 to handle potential rounding
    profit DECIMAL(10, 2)
);




