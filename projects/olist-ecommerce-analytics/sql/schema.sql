-- PostgreSQL star-schema DDL aligned with sql/etl.sql.
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE TABLE IF NOT EXISTS analytics.dim_customer (
 customer_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 customer_id TEXT UNIQUE NOT NULL, customer_unique_id TEXT,
 customer_city TEXT, customer_state CHAR(2));
CREATE TABLE IF NOT EXISTS analytics.dim_product (
 product_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 product_id TEXT UNIQUE NOT NULL, product_category_name TEXT, category_name TEXT);
CREATE TABLE IF NOT EXISTS analytics.dim_seller (
 seller_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 seller_id TEXT UNIQUE NOT NULL, seller_city TEXT, seller_state CHAR(2));
CREATE TABLE IF NOT EXISTS analytics.dim_date (
 date_key INTEGER PRIMARY KEY, full_date DATE UNIQUE NOT NULL,
 calendar_year SMALLINT NOT NULL, calendar_month SMALLINT NOT NULL,
 month_name TEXT NOT NULL, quarter SMALLINT NOT NULL);
CREATE TABLE IF NOT EXISTS analytics.fact_order_item (
 order_id TEXT NOT NULL, order_item_id INTEGER NOT NULL,
 customer_key BIGINT REFERENCES analytics.dim_customer(customer_key),
 product_key BIGINT REFERENCES analytics.dim_product(product_key),
 seller_key BIGINT REFERENCES analytics.dim_seller(seller_key),
 order_date_key INTEGER REFERENCES analytics.dim_date(date_key),
 order_status TEXT, item_price NUMERIC(12,2) NOT NULL,
 freight_value NUMERIC(12,2) NOT NULL, PRIMARY KEY(order_id,order_item_id));
CREATE TABLE IF NOT EXISTS analytics.fact_order_payment (
 order_id TEXT NOT NULL, payment_sequential INTEGER NOT NULL,
 payment_type TEXT, payment_installments INTEGER,
 payment_value NUMERIC(12,2) NOT NULL, PRIMARY KEY(order_id,payment_sequential));
CREATE TABLE IF NOT EXISTS analytics.fact_order_review (
 review_id TEXT PRIMARY KEY, order_id TEXT NOT NULL,
 review_score SMALLINT, review_creation_date TIMESTAMP);
CREATE INDEX IF NOT EXISTS idx_fact_order_item_date ON analytics.fact_order_item(order_date_key);
CREATE INDEX IF NOT EXISTS idx_fact_order_item_product ON analytics.fact_order_item(product_key);
