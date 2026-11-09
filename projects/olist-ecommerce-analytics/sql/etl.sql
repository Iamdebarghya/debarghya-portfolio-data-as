-- PostgreSQL 15+ idempotent dimensional load.
-- Run staging.sql, load CSVs, run data_quality.sql, then run this script.
CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.dim_customer (
 customer_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 customer_id TEXT UNIQUE NOT NULL,
 customer_unique_id TEXT,
 customer_city TEXT,
 customer_state CHAR(2)
);
CREATE TABLE IF NOT EXISTS analytics.dim_product (
 product_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 product_id TEXT UNIQUE NOT NULL,
 product_category_name TEXT,
 category_name TEXT
);
CREATE TABLE IF NOT EXISTS analytics.dim_seller (
 seller_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 seller_id TEXT UNIQUE NOT NULL,
 seller_city TEXT,
 seller_state CHAR(2)
);
CREATE TABLE IF NOT EXISTS analytics.dim_date (
 date_key INTEGER PRIMARY KEY,
 full_date DATE UNIQUE NOT NULL,
 calendar_year SMALLINT NOT NULL,
 calendar_month SMALLINT NOT NULL,
 month_name TEXT NOT NULL,
 quarter SMALLINT NOT NULL
);
CREATE TABLE IF NOT EXISTS analytics.fact_order_item (
 order_id TEXT NOT NULL,
 order_item_id INTEGER NOT NULL,
 customer_key BIGINT REFERENCES analytics.dim_customer(customer_key),
 product_key BIGINT REFERENCES analytics.dim_product(product_key),
 seller_key BIGINT REFERENCES analytics.dim_seller(seller_key),
 order_date_key INTEGER REFERENCES analytics.dim_date(date_key),
 order_status TEXT,
 item_price NUMERIC(12,2) NOT NULL,
 freight_value NUMERIC(12,2) NOT NULL,
 PRIMARY KEY(order_id,order_item_id)
);
CREATE TABLE IF NOT EXISTS analytics.fact_order_payment (
 order_id TEXT NOT NULL,
 payment_sequential INTEGER NOT NULL,
 payment_type TEXT,
 payment_installments INTEGER,
 payment_value NUMERIC(12,2) NOT NULL,
 PRIMARY KEY(order_id,payment_sequential)
);
CREATE TABLE IF NOT EXISTS analytics.fact_order_review (
 review_id TEXT PRIMARY KEY,
 order_id TEXT NOT NULL,
 review_score SMALLINT,
 review_creation_date TIMESTAMP
);

INSERT INTO analytics.dim_customer(customer_id,customer_unique_id,customer_city,customer_state)
SELECT customer_id,customer_unique_id,customer_city,customer_state
FROM staging.customers
ON CONFLICT(customer_id) DO UPDATE SET
 customer_unique_id=EXCLUDED.customer_unique_id,
 customer_city=EXCLUDED.customer_city,
 customer_state=EXCLUDED.customer_state;

INSERT INTO analytics.dim_product(product_id,product_category_name,category_name)
SELECT p.product_id,p.product_category_name,
       COALESCE(t.product_category_name_english,p.product_category_name,'unknown')
FROM staging.products p
LEFT JOIN staging.category_translation t USING(product_category_name)
ON CONFLICT(product_id) DO UPDATE SET
 product_category_name=EXCLUDED.product_category_name,
 category_name=EXCLUDED.category_name;

INSERT INTO analytics.dim_seller(seller_id,seller_city,seller_state)
SELECT seller_id,seller_city,seller_state FROM staging.sellers
ON CONFLICT(seller_id) DO UPDATE SET
 seller_city=EXCLUDED.seller_city,seller_state=EXCLUDED.seller_state;

INSERT INTO analytics.dim_date(date_key,full_date,calendar_year,calendar_month,month_name,quarter)
SELECT DISTINCT TO_CHAR(order_purchase_timestamp::date,'YYYYMMDD')::INTEGER,
       order_purchase_timestamp::date,
       EXTRACT(YEAR FROM order_purchase_timestamp)::SMALLINT,
       EXTRACT(MONTH FROM order_purchase_timestamp)::SMALLINT,
       TO_CHAR(order_purchase_timestamp,'FMMonth'),
       EXTRACT(QUARTER FROM order_purchase_timestamp)::SMALLINT
FROM staging.orders WHERE order_purchase_timestamp IS NOT NULL
ON CONFLICT(full_date) DO NOTHING;

INSERT INTO analytics.fact_order_item(
 order_id,order_item_id,customer_key,product_key,seller_key,order_date_key,
 order_status,item_price,freight_value)
SELECT i.order_id,i.order_item_id,c.customer_key,p.product_key,s.seller_key,
       TO_CHAR(o.order_purchase_timestamp::date,'YYYYMMDD')::INTEGER,
       o.order_status,i.price,i.freight_value
FROM staging.order_items i
JOIN staging.orders o USING(order_id)
LEFT JOIN analytics.dim_customer c USING(customer_id)
LEFT JOIN analytics.dim_product p USING(product_id)
LEFT JOIN analytics.dim_seller s USING(seller_id)
ON CONFLICT(order_id,order_item_id) DO UPDATE SET
 customer_key=EXCLUDED.customer_key,product_key=EXCLUDED.product_key,
 seller_key=EXCLUDED.seller_key,order_date_key=EXCLUDED.order_date_key,
 order_status=EXCLUDED.order_status,item_price=EXCLUDED.item_price,
 freight_value=EXCLUDED.freight_value;

INSERT INTO analytics.fact_order_payment(order_id,payment_sequential,payment_type,payment_installments,payment_value)
SELECT order_id,payment_sequential,payment_type,payment_installments,payment_value
FROM staging.order_payments
ON CONFLICT(order_id,payment_sequential) DO UPDATE SET
 payment_type=EXCLUDED.payment_type,
 payment_installments=EXCLUDED.payment_installments,
 payment_value=EXCLUDED.payment_value;

INSERT INTO analytics.fact_order_review(review_id,order_id,review_score,review_creation_date)
SELECT review_id,order_id,review_score,review_creation_date
FROM staging.order_reviews
ON CONFLICT(review_id) DO UPDATE SET
 order_id=EXCLUDED.order_id,review_score=EXCLUDED.review_score,
 review_creation_date=EXCLUDED.review_creation_date;

CREATE INDEX IF NOT EXISTS idx_fact_order_item_date ON analytics.fact_order_item(order_date_key);
CREATE INDEX IF NOT EXISTS idx_fact_order_item_customer ON analytics.fact_order_item(customer_key);
CREATE INDEX IF NOT EXISTS idx_fact_order_item_product ON analytics.fact_order_item(product_key);
