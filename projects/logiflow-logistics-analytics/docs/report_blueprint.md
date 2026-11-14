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


## Visual design direction — clean analyst-built, not AI concept art

Use a restrained Power BI-native layout. Avoid decorative gradients, fake 3D, oversized glowing cards, random illustrations, and excessive gold. Gold is an accent for key values and selected states only. Use consistent alignment, clear axis labels, source-aware footnotes and readable data labels.

### Page 1 — Executive Overview (question: where is service failing?)
- Header: report title, data period only if a real date is confirmed, and dynamic filter-context subtitle.
- Left rail: compact slicers for Region, Delivery Mode, Partner and Weather.
- Top strip: 4 compact KPI cards (Total Deliveries, On-Time %, Delay Rate %, Avg Actual Hours).
- Main canvas: delivery-mode on-time horizontal bar chart as the dominant visual; region comparison and weather delay-rate visuals as supporting charts.
- Footer: dynamic narrative card using `Mode Performance Insight`, plus data-quality note showing mismatch count.
- Interaction: selecting a mode filters region/weather visuals and all KPI cards. Selecting a region keeps the mode selection and narrows the full page.

### Page 2 — Partner Scorecard (question: which partner balances service and cost?)
- Header: dynamic partner/region context.
- Main left: sortable partner matrix with delivery volume, on-time %, delay %, cost/km and rating.
- Main right: scatter plot with cost/km on X, on-time % on Y and delivery count as bubble size.
- Bottom: partner on-time ranking, with minimum-volume threshold clearly documented.
- Footer: dynamic narrative card using `Partner Performance Insight`.
- Interaction: selecting one partner filters the page and the exception drill-through. A reset bookmark clears all slicers.

### Page 3 — Delay Investigation (question: what should operations inspect?)
- Header: selected filter context and delayed delivery count.
- Left: delay band distribution and delay rate by distance bucket.
- Right: delay rate by vehicle and weather.
- Bottom half: detailed exception table, filtered to delayed rows, sorted by delay hours descending.
- Footer: dynamic narratives for selected weather/mode; clearly label the 15% cost estimate as a scenario.
- Interaction: selecting a distance band, vehicle or weather category filters the exception table. Drill-through from partner/mode opens the same records with that context.

## Power BI interaction matrix

| Source visual | Target visuals | Interaction |
|---|---|---|
| Region slicer | All visuals on all pages | Filter |
| Delivery Mode slicer | All visuals on all pages | Filter |
| Partner slicer | All visuals on all pages | Filter |
| Weather slicer | All visuals on all pages | Filter |
| Page 1 delivery mode bar | Region, weather, KPI cards | Filter/highlight |
| Page 2 partner matrix | Scatter, ranking, KPI cards | Filter |
| Page 3 distance/vehicle/weather chart | Exception table and KPI cards | Filter |

Use View → Sync slicers to sync the core slicers across pages. Use Format → Edit interactions to verify every visual's filter/highlight/none behavior. Add a Reset Filters bookmark after clearing slicers and set the button action to that bookmark.

## Portfolio screenshot evidence
Capture the actual Power BI report in three states:
1. All data, all filters cleared.
2. One region selected, showing changed KPI values and chart distributions.
3. Same region plus one delivery mode selected, showing further recalculation.

Also capture the Power Query applied steps and DAX measures pane. These are evidence of the workflow, not decorative screenshots.
