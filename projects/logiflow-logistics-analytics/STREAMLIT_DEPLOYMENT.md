# LogiFlow Interactive Dashboard

## Run locally
```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Deploy free on Streamlit Community Cloud
1. Sign in to https://share.streamlit.io/ using GitHub.
2. Choose repository `Iamdebarghya/debarghya-portfolio-data-as`.
3. Set branch to `main`.
4. Set Main file path to `projects/logiflow-logistics-analytics/app.py`.
5. Deploy. Streamlit installs dependencies from the adjacent `requirements.txt`.

The app attempts to load the public source CSV from the original dataset repository. If the source URL changes or is unavailable, upload `Delivery_Logistics.csv` through the sidebar.

## Data source and caveats
Dataset source: https://github.com/dikagra123/Last-Mile-Delivery-Project

The app is designed around the fields described in the source README. It includes basic column aliases and a data-quality audit. Inspect the CSV headers and verify the repaired duration fields before presenting results as independently reproduced. The source documentation reports malformed epoch-like time columns and approximately 1,203 label-vs-measurement mismatches. The original `delayed` label is retained as the primary KPI target.

This app does not redistribute the CSV, does not contain a Power BI PBIX file, and does not claim the source's published results have been independently reproduced. Review the original dataset terms before reuse.
