-- 1. Monthly item revenue. Keep item-grain measures in the item fact.
SELECT d.calendar_year, d.calendar_month,
       SUM(f.item_price) AS item_revenue,
       SUM(f.freight_value) AS freight_revenue
FROM analytics.fact_order_item f
JOIN analytics.dim_date d ON d.date_key = f.order_date_key
GROUP BY d.calendar_year, d.calendar_month
ORDER BY d.calendar_year, d.calendar_month;

-- 2. Product category performance.
SELECT p.category_name_english,
       SUM(f.item_price) AS item_revenue,
       SUM(f.order_item_id * 0 + 1) AS item_lines
FROM analytics.fact_order_item f
JOIN analytics.dim_product p ON p.product_key = f.product_key
GROUP BY p.category_name_english
ORDER BY item_revenue DESC;

-- 3. Customer state contribution.
SELECT c.customer_state, SUM(f.item_price) AS item_revenue
FROM analytics.fact_order_item f
JOIN analytics.dim_customer c ON c.customer_key = f.customer_key
GROUP BY c.customer_state
ORDER BY item_revenue DESC;

-- 4. Payment mix. Payment value is not joined to item fact to avoid fan-out.
SELECT payment_type, COUNT(DISTINCT order_id) AS orders,
       SUM(payment_value) AS paid_value,
       AVG(payment_installments) AS avg_installments
FROM analytics.fact_order_payment
GROUP BY payment_type
ORDER BY paid_value DESC;
