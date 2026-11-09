-- Build order-level and item-level analytical facts.
-- PostgreSQL 15+. Run after staging.sql has been loaded and validated.
CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.dim_customer AS
SELECT ROW_NUMBER() OVER (ORDER BY customer_id) AS customer_key,
       customer_id, customer_unique_id, customer_city, customer_state
FROM staging.customers
WITH NO DATA;
INSERT INTO analytics.dim_customer
SELECT ROW_NUMBER() OVER (ORDER BY customer_id),
       customer_id, customer_unique_id, customer_city, customer_state
FROM staging.customers
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS analytics.dim_product AS
SELECT ROW_NUMBER() OVER (ORDER BY p.product_id) AS product_key,
       p.product_id, p.product_category_name,
       COALESCE(t.product_category_name_english,p.product_category_name,'unknown') AS category_name
FROM staging.products p
LEFT JOIN staging.category_translation t USING(product_category_name)
WITH NO DATA;
INSERT INTO analytics.dim_product
SELECT ROW_NUMBER() OVER (ORDER BY p.product_id),
       p.product_id, p.product_category_name,
       COALESCE(t.product_category_name_english,p.product_category_name,'unknown')
FROM staging.products p
LEFT JOIN staging.category_translation t USING(product_category_name)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS analytics.dim_seller AS
SELECT ROW_NUMBER() OVER (ORDER BY seller_id) AS seller_key,
       seller_id,seller_city,seller_state
FROM staging.sellers WITH NO DATA;
INSERT INTO analytics.dim_seller
SELECT ROW_NUMBER() OVER (ORDER BY seller_id),seller_id,seller_city,seller_state
FROM staging.sellers
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS analytics.dim_date (
 date_key INTEGER PRIMARY KEY, full_date DATE UNIQUE NOT NULL,
 calendar_year SMALLINT NOT NULL, calendar_month SMALLINT NOT NULL,
 month_name TEXT NOT NULL, quarter SMALLINT NOT NULL
);
INSERT INTO analytics.dim_date
SELECT DISTINCT TO_CHAR(d::date,'YYYYMMDD')::INTEGER,d::date,
       EXTRACT(YEAR FROM d)::SMALLINT,EXTRACT(MONTH FROM d)::SMALLINT,
       TO_CHAR(d,'FMMonth'),EXTRACT(QUARTER FROM d)::SMALLINT
FROM (
 SELECT order_purchase_timestamp::date AS d FROM staging.orders
 WHERE order_purchase_timestamp IS NOT NULL
) dates
ON CONFLICT(full_date) DO NOTHING;

CREATE TABLE IF NOT EXISTS analytics.fact_order_item (
 order_id TEXT NOT NULL, order_item_id INTEGER NOT NULL,
 customer_key BIGINT, product_key BIGINT, seller_key BIGINT,
 order_date_key INTEGER, order_status TEXT,
 item_price NUMERIC(12,2) NOT NULL, freight_value NUMERIC(12,2) NOT NULL,
 PRIMARY KEY(order_id,order_item_id)
);
INSERT INTO analytics.fact_order_item
SELECT i.order_id,i.order_item_id,c.customer_key,p.product_key,s.seller_key,
       TO_CHAR(o.order_purchase_timestamp::date,'YYYYMMDD')::INTEGER,
       o.order_status,i.price,i.freight_value
FROM staging.order_items i
JOIN staging.orders o USING(order_id)
LEFT JOIN analytics.dim_customer c USING(customer_id)
LEFT JOIN analytics.dim_product p USING(product_id)
LEFT JOIN analytics.dim_seller s USING(seller_id)
ON CONFLICT(order_id,order_item_id) DO NOTHING;

CREATE TABLE IF NOT EXISTS analytics.fact_order_payment (
 order_id TEXT NOT NULL, payment_sequential INTEGER NOT NULL,
 payment_type TEXT, payment_installments INTEGER,
 payment_value NUMERIC(12,2) NOT NULL,
 PRIMARY KEY(order_id,payment_sequential)
);
INSERT INTO analytics.fact_order_payment
SELECT order_id,payment_sequential,payment_type,payment_installments,payment_value
FROM staging.order_payments
ON CONFLICT(order_id,payment_sequential) DO NOTHING;

-- Keep reviews at review grain, not joined directly to item rows.
CREATE TABLE IF NOT EXISTS analytics.fact_order_review (
 review_id TEXT PRIMARY KEY, order_id TEXT NOT NULL,
 review_score SMALLINT, review_creation_date TIMESTAMP
);
INSERT INTO analytics.fact_order_review
SELECT review_id,order_id,review_score,review_creation_date
FROM staging.order_reviews
ON CONFLICT(review_id) DO NOTHING;
