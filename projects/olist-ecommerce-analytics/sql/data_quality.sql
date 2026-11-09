-- Run after staging loads. Every query should return zero rows unless noted.
-- 1. Duplicate order primary keys.
SELECT order_id, COUNT(*) FROM staging.orders GROUP BY order_id HAVING COUNT(*) > 1;
-- 2. Orphan order items.
SELECT i.order_id FROM staging.order_items i
LEFT JOIN staging.orders o USING(order_id) WHERE o.order_id IS NULL;
-- 3. Invalid negative amounts.
SELECT * FROM staging.order_items WHERE price < 0 OR freight_value < 0;
-- 4. Missing purchase timestamps.
SELECT COUNT(*) AS missing_purchase_timestamps FROM staging.orders
WHERE order_purchase_timestamp IS NULL;
-- 5. Payment rows without a matching order.
SELECT p.order_id FROM staging.order_payments p
LEFT JOIN staging.orders o USING(order_id) WHERE o.order_id IS NULL;
-- 6. Row counts by source.
SELECT 'orders' AS source, COUNT(*) AS rows FROM staging.orders
UNION ALL SELECT 'order_items', COUNT(*) FROM staging.order_items
UNION ALL SELECT 'payments', COUNT(*) FROM staging.order_payments
UNION ALL SELECT 'reviews', COUNT(*) FROM staging.order_reviews;
