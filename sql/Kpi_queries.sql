
--checking for num of rows
SELECT count(*) AS total_rows FROM orders;

-- checking the 3 important things to confirm the data migrated succesfuly and accuratly
SELECT 
    COUNT(*) as total_rows, 
    SUM(sales) as total_revenue, 
    COUNT(DISTINCT region) as unique_regions
FROM orders;

SELECT 
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,
    (SUM(profit) / SUM(sales)) * 100 AS profit_margin_percent,
    COUNT(DISTINCT order_id) AS total_orders
FROM orders;

SELECT 
    strftime('%Y-%m', order_date) AS month, 
    SUM(sales) AS monthly_sales,
    SUM(profit) AS monthly_profit
FROM orders
GROUP BY 1  -- This tells SQL to group by the first column (the formatted month)
ORDER BY 1;

SELECT 
    category, 
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,
    AVG(discount) AS avg_discount
FROM orders
GROUP BY category
ORDER BY total_profit DESC;



SELECT 
    sub_category, 
    SUM(profit) AS total_profit,
    AVG(discount) AS avg_discount
FROM orders
GROUP BY sub_category
HAVING total_profit < 0
ORDER BY total_profit ASC;