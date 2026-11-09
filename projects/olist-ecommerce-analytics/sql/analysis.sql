-- Revenue and item metrics must be calculated at item grain.
-- Never join raw item rows to raw payment/review rows before aggregating:
-- one order can contain multiple items, payment records and reviews.

-- 1. Monthly item GMV and freight.
SELECT d.calendar_year,d.calendar_month,
       SUM(f.item_price) AS item_gmv,
       SUM(f.freight_value) AS freight_total,
       COUNT(DISTINCT f.order_id) AS orders
FROM analytics.fact_order_item f
JOIN analytics.dim_date d ON d.date_key=f.order_date_key
WHERE f.order_status NOT IN ('canceled','unavailable')
GROUP BY d.calendar_year,d.calendar_month
ORDER BY 1,2;

-- 2. Category contribution.
SELECT p.category_name,
       SUM(f.item_price) AS item_gmv,
       COUNT(DISTINCT f.order_id) AS orders
FROM analytics.fact_order_item f
JOIN analytics.dim_product p USING(product_key)
WHERE f.order_status NOT IN ('canceled','unavailable')
GROUP BY p.category_name
ORDER BY item_gmv DESC;

-- 3. State contribution.
SELECT c.customer_state,SUM(f.item_price) AS item_gmv,
       COUNT(DISTINCT f.order_id) AS orders
FROM analytics.fact_order_item f
JOIN analytics.dim_customer c USING(customer_key)
WHERE f.order_status NOT IN ('canceled','unavailable')
GROUP BY c.customer_state ORDER BY item_gmv DESC;

-- 4. Payment mix (separate payment fact).
SELECT payment_type,COUNT(DISTINCT order_id) AS orders,
       SUM(payment_value) AS paid_amount,
       ROUND(AVG(payment_installments),2) AS avg_installments
FROM analytics.fact_order_payment
GROUP BY payment_type ORDER BY paid_amount DESC;

-- 5. Month-over-month change.
WITH monthly AS (
 SELECT d.calendar_year,d.calendar_month,SUM(f.item_price) AS item_gmv
 FROM analytics.fact_order_item f
 JOIN analytics.dim_date d ON d.date_key=f.order_date_key
 WHERE f.order_status NOT IN ('canceled','unavailable')
 GROUP BY d.calendar_year,d.calendar_month
), compared AS (
 SELECT *,LAG(item_gmv) OVER(ORDER BY calendar_year,calendar_month) AS prior_month_gmv
 FROM monthly
)
SELECT calendar_year,calendar_month,item_gmv,prior_month_gmv,
       ROUND(100.0*(item_gmv-prior_month_gmv)/NULLIF(prior_month_gmv,0),2) AS mom_growth_pct
FROM compared ORDER BY calendar_year,calendar_month;
