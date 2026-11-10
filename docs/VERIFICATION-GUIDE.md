# Recruiter & Technical Verification Guide

This guide explains how to inspect the projects in this portfolio and reproduce their work locally. It describes the repository as it exists; it does not claim private client work or invent business results.

## Project evidence map

| Project | What to inspect | Data provenance |
|---|---|---|
| Olist E-commerce Analytics | Python data preparation and metrics in `src/olist.py`; SQL schema, staging, ETL, data-quality checks and analysis in `sql/`; Streamlit/browser dashboards; unit and integration tests | Anonymised public Olist dataset (2016–2018), sourced via Kaggle |
| HR Attrition Analysis | Python metrics in `src/hr_metrics.py`; SQL analysis; Streamlit/browser dashboards; unit tests | IBM fictional educational HR dataset |
| Sales dashboard | `dashboard.html`, including CSV upload and dashboard calculations | Reviewer-provided CSV; results depend on the input file |

## Run HR Attrition Analysis

1. Download the dataset from the source linked in the HR project README.
2. Put the CSV in the data location documented by that README.
3. From the HR project directory, create and activate a virtual environment, install requirements, run tests, and start Streamlit:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
streamlit run app.py
```

The dataset is fictional and must not be presented as real employee records.

## Run Olist E-commerce Analytics

1. Download the public Olist dataset from the Kaggle source linked in the Olist project README and follow its license/terms.
2. Extract the eight required CSV files into the data directory documented in that README. The optional geolocation CSV is not used by the current app.
3. From the Olist project directory:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
streamlit run app.py
```

Integration tests require the raw dataset. If those files are absent, integration tests may be skipped.

## SQL review path

For Olist, inspect `sql/schema.sql`, `sql/staging.sql`, `sql/etl.sql`, `sql/data_quality.sql`, and `sql/analysis.sql`. For HR, inspect `sql/analysis.sql`.

Olist orders, items, payments and reviews have different grains and one-to-many relationships. Review how child tables are aggregated before they are joined to avoid inflated totals.

## How an interviewer can verify understanding

A repository and commit history are useful evidence of development activity, but neither alone proves who authored every line. A fair technical review can:

1. Inspect commits and changes over time.
2. Clone the repository and run the project using the instructions above.
3. Ask the author to explain a selected function, SQL query, metric definition and data-quality check.
4. Request a small live change, such as adding a KPI, validating an input condition or changing a chart grouping.
5. Compare the changed output with the expected result.

The author should accurately disclose the use of templates, libraries, documentation and AI assistance, where applicable.

## Validation status and limitations

- A previous local review of the supplied repository archive reported 8 tests passed and 3 Olist integration tests skipped because the raw Kaggle data was not included in that archive. This is a historical result, not a fresh run of the current main branch.
- The GitHub Actions Olist test job for the merge commit did not start because GitHub reported that the account was locked due to a billing issue. This is not a test assertion failure.
- GitHub Pages deployment for that merge commit completed successfully.
- Re-run the commands above with the datasets present to obtain a fresh result.

## Data integrity

- Olist findings relate to the public anonymised Olist dataset, not an employer or client.
- HR findings relate to a fictional educational dataset, not actual employees.
- Sales dashboard output depends on the CSV supplied by the reviewer.
- Descriptive associations should not be presented as causal findings.
- Dataset licenses and attribution requirements remain applicable; consult the individual project READMEs.
