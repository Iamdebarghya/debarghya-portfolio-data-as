-- LogiFlow | SQL validation and business analysis
-- Dialect: SQLite-compatible SQL.
-- Rename/alias source columns to canonical names before running.

-- 1. Executive KPI summary
SELECT
    COUNT(*) AS total_deliveries,
    SUM(CASE WHEN delayed = 1 THEN 1 ELSE 0 END) AS delayed_deliveries,
    ROUND(100.0 * SUM(CASE WHEN delayed = 0 THEN 1 ELSE 0 END) / COUNT(*), 2) AS on_time_pct,
    ROUND(AVG(delivery_time_hours), 2) AS avg_actual_hours,
    ROUND(SUM(delivery_cost), 2) AS total_delivery_cost,
    ROUND(SUM(delivery_cost) / NULLIF(SUM(distance_km), 0), 2) AS cost_per_km
FROM fact_deliveries;

-- 2. Delivery mode is a key operational dimension
SELECT
    delivery_mode,
    COUNT(*) AS deliveries,
    ROUND(100.0 * SUM(CASE WHEN delayed = 0 THEN 1 ELSE 0 END) / COUNT(*), 2) AS on_time_pct,
    ROUND(AVG(delivery_time_hours), 2) AS avg_actual_hours,
    ROUND(AVG(expected_time_hours), 2) AS avg_expected_hours
FROM fact_deliveries
GROUP BY delivery_mode
ORDER BY on_time_pct ASC;

-- 3. Partner scorecard
SELECT
    delivery_partner,
    COUNT(*) AS deliveries,
    ROUND(100.0 * SUM(CASE WHEN delayed = 0 THEN 1 ELSE 0 END) / COUNT(*), 2) AS on_time_pct,
    ROUND(SUM(delivery_cost) / NULLIF(SUM(distance_km), 0), 2) AS cost_per_km,
    ROUND(AVG(delivery_rating), 2) AS avg_rating
FROM fact_deliveries
GROUP BY delivery_partner
HAVING COUNT(*) >= 100
ORDER BY on_time_pct DESC;

-- 4. Region and weather segmentation
SELECT
    region,
    weather,
    COUNT(*) AS deliveries,
    ROUND(100.0 * AVG(CASE WHEN delayed = 1 THEN 1.0 ELSE 0.0 END), 2) AS delay_rate_pct
FROM fact_deliveries
GROUP BY region, weather
ORDER BY delay_rate_pct DESC;

-- 5. Delay magnitude bands
SELECT
    CASE
        WHEN delay_hours <= 0 THEN 'On time / Early'
        WHEN delay_hours <= 2 THEN '0-2 hours'
        WHEN delay_hours <= 6 THEN '2-6 hours'
        WHEN delay_hours <= 12 THEN '6-12 hours'
        ELSE '12+ hours'
    END AS delay_band,
    COUNT(*) AS deliveries
FROM fact_deliveries
GROUP BY delay_band
ORDER BY deliveries DESC;

-- 6. Label/measurement mismatch audit
SELECT
    COUNT(*) AS mismatch_rows
FROM fact_deliveries
WHERE delayed <>
    CASE WHEN delivery_time_hours > expected_time_hours THEN 1 ELSE 0 END;

-- 7. Exception review queue
SELECT
    row_id, delivery_partner, region, delivery_mode, vehicle_type,
    distance_km, package_weight_kg, delivery_time_hours,
    expected_time_hours, delay_hours, delivery_cost
FROM fact_deliveries
WHERE delayed = 1
ORDER BY delay_hours DESC, delivery_cost DESC
LIMIT 500;
