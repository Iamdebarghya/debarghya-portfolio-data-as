# LogiFlow | Dark Gold Power BI Report Blueprint

## Theme
- Canvas: `#111111`
- Visual panel: `#1D1D1D`
- Gold accent: `#D6AE52`
- Main text: `#F2EBDD`
- Secondary text: `#B6AA91`
- Page ratio: 16:9
- Typography: Segoe UI; concise labels; restrained gridlines.

## Page 1 — Executive Delivery Overview
**KPI strip:** Total Deliveries · On-Time % · Delay Rate % · Avg Actual Hours · Total Delivery Cost · Cost per KM.

**Visuals**
- Horizontal bar: on-time rate by delivery mode.
- Column chart: delayed vs on-time by region.
- Bar chart: delay rate by weather.
- Matrix: region × delivery mode with delivery count and on-time %.

**Slicers:** Region, delivery mode, vehicle type, weather, partner.

## Page 2 — Partner Scorecard
**Visuals**
- Ranked partner table: delivery count, on-time %, cost/km, average rating.
- Scatter: cost/km vs on-time %, bubble size = deliveries.
- Bar: on-time rate by partner.
- Tooltip: delivery volume, rating, delay rate and average delivery time.

**Interpretation guardrail:** Partner gaps in the source project are relatively small. Avoid claiming partner allocation is the dominant lever.

## Page 3 — Delay Drivers & Exceptions
**Visuals**
- Delay-hour band distribution.
- Delay rate by distance bucket.
- Delay rate by vehicle type and package type.
- Exception detail table with partner, region, mode, distance, weight, actual/expected hours and cost.
- Conditional formatting on delay hours and cost.

**Drill-through:** Delivery mode or partner to detail page.

## UX and QA
- Add page navigation buttons and report tooltips.
- Use synced slicers across pages.
- Keep table headers short and enable search.
- Test interactions on a phone-sized viewport after publishing.
- Reconcile KPI cards with SQL before sharing.
- Do not create a monthly trend unless the raw source has a genuine date field.
