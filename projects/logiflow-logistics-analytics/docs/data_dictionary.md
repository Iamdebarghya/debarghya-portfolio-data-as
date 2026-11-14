# Data Dictionary & Source-to-Model Mapping

The source notebook's displayed raw CSV preview confirms these 15 raw headers. The Power Query staging file renames/derives fields into the canonical model below.

| Raw source column | Canonical model field | Type | Transformation |
|---|---|---|---|
| delivery_id | delivery_id | Text | Preserve for traceability; not unique |
| delivery_partner | delivery_partner | Text | Trim/lowercase |
| package_type | package_type | Text | Trim/lowercase |
| vehicle_type | vehicle_type | Text | Trim/lowercase |
| delivery_mode | delivery_mode | Text | Trim/lowercase |
| region | region | Text | Trim/lowercase |
| weather_condition | weather | Text | Rename; trim/lowercase |
| distance_km | distance_km | Decimal | Numeric |
| package_weight_kg | package_weight_kg | Decimal | Numeric |
| delivery_time_hours | delivery_time_hours | Decimal | Extract trailing nanosecond integer from malformed 1970 timestamp, following source notebook method |
| expected_time_hours | expected_time_hours | Decimal | Same source-specific conversion |
| delayed | delayed | Whole number | yes → 1, no → 0; retain original source label during audit if desired |
| delivery_status | delivery_status | Text | Trim/lowercase |
| delivery_rating | delivery_rating | Whole number | Numeric |
| delivery_cost | delivery_cost | Currency | Numeric |
| generated | row_id | Whole number | Sequential surrogate key |
| generated | delay_hours | Decimal | Actual hours minus expected hours |
| generated | calculated_delay_flag | Whole number | 1 when actual duration > expected duration, else 0 |
| generated | label_measurement_mismatch | Whole number | 1 when source delayed flag differs from calculated flag |
| generated | cost_per_km | Decimal | Delivery cost / distance when distance > 0 |
| generated | distance_bucket | Text | 0-50, 51-100, 101-200, 200+ km |
| generated | delay_band | Text | On time/Early, 0-2, 2-6, 6-12, 12+ hours |

## Source data quality rules

1. Preserve an unchanged raw source copy.
2. The source notebook shows duration strings such as `1970-01-01 00:00:00.000000008`; the source analysis extracts the trailing nanosecond integer as the hour value. Do not interpret these as real event dates.
3. `delivery_id` is non-unique. Use generated `row_id` for row identity.
4. The source README reports approximately 1,203 label/measurement mismatches (~4.8%). Retain the source `delayed` label as the primary outcome and keep the calculated flag separately.
5. Remove exact duplicate rows only after recording row counts before and after.
6. No genuine delivery date is confirmed in the source schema. Do not create date-based trends or a date slicer.
7. Check zero/negative distance before cost-per-km calculations.
