# LogiFlow | Analyst Storytelling & Interview Notes

This file is a speaking guide for the three-page Power BI report. It deliberately separates published source findings from conclusions that must be recalculated from the CSV.

## The business problem

A last-mile delivery operation needs to understand not only how many deliveries are late, but where service reliability changes, which operational factors are associated with delay, and what teams should investigate first.

The report is designed to answer three questions:
1. What is the service-level picture across the selected data?
2. How does delivery partner performance compare when delivery volume and cost are considered together?
3. Which delivery conditions and individual shipments deserve operational investigation?

## Page 1 — Executive Overview

### What the viewer should understand
This page establishes the baseline. The KPI cards answer "how much" and "how well"; the mode, region and weather visuals answer "where does the pattern vary?"

### How to explain it in an interview
"I started with the overall service picture, then broke the on-time rate down by delivery mode, region and weather. I added shared slicers so a reviewer can select a region or mode and see every KPI and chart recalculate under the same filter context."

### What to investigate
- Does the on-time rate change materially by delivery mode?
- Are regional differences large enough to matter, or are they within a narrow range?
- Does a weather segment have a different delay rate after checking its delivery volume?
- Do selected filters change the conclusion, or only the number of records?

### Avoid saying
- Do not call a category the root cause based only on a chart association.
- Do not show a monthly trend unless a genuine delivery date is present and validated.
- Do not use source-published percentages as if this project independently recalculated them.

## Page 2 — Partner Scorecard

### What the viewer should understand
A partner should not be ranked by on-time percentage alone. Volume, cost per kilometre and rating provide context.

### How to explain it in an interview
"I compared delivery partners using reliability, delivery volume, unit cost and rating. The scatter plot helps identify partners that combine stronger on-time performance with competitive cost. I kept delivery count visible because a percentage based on a small sample can be misleading."

### What to investigate
- Which partners have both meaningful delivery volume and strong on-time performance?
- Are high on-time rates associated with higher cost per kilometre?
- Are rating and on-time performance moving together in this filtered sample?
- Does a partner's position change when a region or delivery mode is selected?

### Avoid saying
- Do not recommend reallocating deliveries based on a small percentage-point gap alone.
- Do not infer causation from the scatter plot.
- Do not hide the number of deliveries behind a percentage ranking.

## Page 3 — Delay Drivers & Exceptions

### What the viewer should understand
This page moves from aggregate patterns to operational investigation. It shows delay magnitude and allows a user to inspect the individual delayed records behind a selected segment.

### How to explain it in an interview
"I designed the third page as an investigation view. When I select a weather condition, vehicle type or delivery mode, the exception table responds to that context. An operations user can then inspect the delayed shipments rather than stopping at an aggregate percentage."

### What to investigate
- Which segments have the largest delay rate and enough records to be credible?
- Are delays concentrated in a particular distance band or vehicle category?
- Which delayed records combine long delay duration with high delivery cost?
- How many records disagree between the source delay label and a delay recalculated from actual versus expected duration?

### Avoid saying
- A mismatch between label and calculated duration is a data-quality flag, not proof that the source label is wrong.
- The 15% estimated delay-cost measure is a scenario assumption, not observed financial loss.
- Do not describe weather or vehicle as a cause unless further evidence supports causality.

## Interaction demonstration script

Use this sequence in a live portfolio walkthrough:
1. Start with all filters cleared and explain the baseline KPIs.
2. Select one region. Point out which KPIs and charts recalculate.
3. Keep that region selected and choose one delivery mode. Explain how the mode comparison changes within that region.
4. Open Partner Scorecard and select one partner. Show the volume, reliability and cost context.
5. Open Delay Drivers, select a segment and inspect the filtered exception records.
6. Reset filters and explain the difference between the full dataset and the selected segment.

## Data integrity and reproducibility

The linked source project's README reports 25,000 rows, 73.32% overall on-time delivery, around 1,203 label/measurement mismatches, and a large difference across delivery modes. These are source-published reference figures only. Recalculate all figures from the downloaded CSV before presenting them as findings from this portfolio project.

The source README also describes malformed duration fields and a non-unique delivery identifier. The cleaning workflow must preserve a raw copy, repair duration fields only using a verified source-specific method, generate a surrogate row key, and retain both the original delay label and a separate calculated flag.

## What makes this an analyst-built report

- Clear business questions define each page.
- A documented data-cleaning process preserves raw values and flags quality issues.
- Measures are separated from calculated columns.
- Shared slicers and cross-filtering let users test their own questions.
- Dynamic narrative cards explain the selected filter context.
- SQL checks independently validate key measures.
- The portfolio distinguishes verified findings, source-reported figures, and scenario assumptions.
