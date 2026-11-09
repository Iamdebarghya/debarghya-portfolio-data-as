-- PostgreSQL 15+ staging layer. Load Kaggle CSVs with psql \copy after creating these tables.
CREATE SCHEMA IF NOT EXISTS staging;
CREATE TABLE IF NOT EXISTS staging.orders (
 order_id TEXT PRIMARY KEY, customer_id TEXT, order_status TEXT,
 order_purchase_timestamp TIMESTAMP, order_approved_at TIMESTAMP,
 order_delivered_carrier_date TIMESTAMP, order_delivered_customer_date TIMESTAMP,
 order_estimated_delivery_date TIMESTAMP
);
CREATE TABLE IF NOT EXISTS staging.customers (
 customer_id TEXT PRIMARY KEY, customer_unique_id TEXT,
 customer_zip_code_prefix TEXT, customer_city TEXT, customer_state TEXT
);
CREATE TABLE IF NOT EXISTS staging.order_items (
 order_id TEXT, order_item_id INTEGER, product_id TEXT, seller_id TEXT,
 shipping_limit_date TIMESTAMP, price NUMERIC(12,2), freight_value NUMERIC(12,2),
 PRIMARY KEY(order_id,order_item_id)
);
CREATE TABLE IF NOT EXISTS staging.order_payments (
 order_id TEXT, payment_sequential INTEGER, payment_type TEXT,
 payment_installments INTEGER, payment_value NUMERIC(12,2),
 PRIMARY KEY(order_id,payment_sequential)
);
CREATE TABLE IF NOT EXISTS staging.order_reviews (
 review_id TEXT PRIMARY KEY, order_id TEXT, review_score INTEGER,
 review_comment_title TEXT, review_comment_message TEXT,
 review_creation_date TIMESTAMP, review_answer_timestamp TIMESTAMP
);
CREATE TABLE IF NOT EXISTS staging.products (
 product_id TEXT PRIMARY KEY, product_category_name TEXT,
 product_name_lenght INTEGER, product_description_lenght INTEGER,
 product_photos_qty INTEGER, product_weight_g INTEGER,
 product_length_cm INTEGER, product_height_cm INTEGER, product_width_cm INTEGER
);
CREATE TABLE IF NOT EXISTS staging.sellers (
 seller_id TEXT PRIMARY KEY, seller_zip_code_prefix TEXT,
 seller_city TEXT, seller_state TEXT
);
CREATE TABLE IF NOT EXISTS staging.category_translation (
 product_category_name TEXT PRIMARY KEY, product_category_name_english TEXT
);

-- Example imports (run from psql; update paths for your machine):
-- \copy staging.orders FROM 'data/raw/olist_orders_dataset.csv' CSV HEADER
-- \copy staging.customers FROM 'data/raw/olist_customers_dataset.csv' CSV HEADER
-- \copy staging.order_items FROM 'data/raw/olist_order_items_dataset.csv' CSV HEADER
-- \copy staging.order_payments FROM 'data/raw/olist_order_payments_dataset.csv' CSV HEADER
-- \copy staging.order_reviews FROM 'data/raw/olist_order_reviews_dataset.csv' CSV HEADER
-- \copy staging.products FROM 'data/raw/olist_products_dataset.csv' CSV HEADER
-- \copy staging.sellers FROM 'data/raw/olist_sellers_dataset.csv' CSV HEADER
-- \copy staging.category_translation FROM 'data/raw/product_category_name_translation.csv' CSV HEADER
