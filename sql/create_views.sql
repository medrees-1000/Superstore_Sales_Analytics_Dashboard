CREATE VIEW vw_orders_time AS
SELECT
  *,
  CAST(strftime('%Y', order_date) AS INTEGER) AS order_year,
  CAST(strftime('%m', order_date) AS INTEGER) AS order_month,
  strftime('%Y-%m', order_date) AS year_month
FROM orders;

SELECT * FROM vw_orders_time LIMIT 5;


-- Step 2: Overall KPIs
CREATE VIEW vw_overall_kpis AS
SELECT
  ROUND(SUM(sales), 2) AS total_sales,
  ROUND(SUM(profit), 2) AS total_profit,
  COUNT(DISTINCT order_id) AS total_orders,
  ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct
FROM orders;


-- Step 3: Monthly Trend
CREATE VIEW vw_monthly_performance AS
SELECT
  year_month,
  order_year,
  order_month,
  ROUND(SUM(sales), 2) AS monthly_sales,
  ROUND(SUM(profit), 2) AS monthly_profit
FROM vw_orders_time
GROUP BY year_month, order_year, order_month
ORDER BY year_month;


-- Step 4: Regional
CREATE VIEW vw_region_performance AS
SELECT
  region,
  ROUND(SUM(sales), 2) AS total_sales,
  ROUND(SUM(profit), 2) AS total_profit,
  COUNT(DISTINCT order_id) AS total_orders
FROM orders
GROUP BY region;

-- Step 5: Category
CREATE VIEW vw_category_performance AS
SELECT
  category,
  sub_category,
  ROUND(SUM(sales), 2) AS total_sales,
  ROUND(SUM(profit), 2) AS total_profit,
  COUNT(*) AS line_items
FROM orders
GROUP BY category, sub_category;

CREATE VIEW vw_discount_impact AS
SELECT
  CASE
    WHEN discount = 0 THEN '0%'
    WHEN discount <= 0.10 THEN '1–10%'
    WHEN discount <= 0.30 THEN '11–30%'
    WHEN discount <= 0.50 THEN '31–50%'
    ELSE '50%+'
  END AS discount_bucket,
  ROUND(AVG(discount) * 100, 2) AS avg_discount_pct,
  ROUND(SUM(sales), 2) AS total_sales,
  ROUND(SUM(profit), 2) AS total_profit,
  COUNT(*) AS order_lines
FROM orders
GROUP BY discount_bucket
ORDER BY avg_discount_pct;

Select * From vw_discount_impact limit 5;

SELECT 'Total Sales Check' as metric, total_sales FROM vw_overall_kpis
UNION ALL
SELECT 'Category Row Check', COUNT(*) FROM vw_category_performance;