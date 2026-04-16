# DEA — Data Engineering & Analysis | Polish Healthcare Datasets

An analytical database built on public Polish healthcare data (NFZ, GOV, e-Zdrowie, Ministry of Health).

## Overview

DEA is a data engineering and analytics project that ingests, transforms, and serves public Polish healthcare datasets through a DuckDB analytical database and a Streamlit dashboard.

## Database Schema

The project contains five tables:

**icd_codes** — Full ICD-10 dictionary in Polish, not available in structured form elsewhere online. Contains both category-level and detailed codes with Polish and English descriptions.

**hospital_dict** — All hospitals present in the NFZ datasets, enriched with geocoordinates obtained via reverse geocoding.

**diagnosis** — Patient counts by hospital and ICD-10 diagnosis code. Suppressed values (reported as `<5` in source data) are stored as `NULL` with an `is_suppressed` flag rather than being estimated.

**drug_treatment** — Patient counts by hospital, diagnosis, and drug EAN code.

**drug_registry** — Full Polish drug registry (URPL) with trade names, substance names, and EAN/GTIN codes parsed from structured strings.

## Dashboard

The Streamlit app exposes four views:

- ICD-10 dictionary browser
- Hospital dictionary with geocoordinates
- Top 10 most common diagnoses by total patient count (bar chart)
- Top 10 most prescribed drugs in hospital treatment (bar chart)

## Data Sources

- NFZ open data — diagnosis by ICD-10 and hospital (2023, 2024 H1)
- NFZ open data — diagnosis and drug by ICD-10 and hospital
- URPL drug registry (rejestr leków)
- ICD-10 Polish classification

## Getting Started

Clone the repository and install dependencies:

```bash
git clone https://github.com/justgodtears/DEA.git
cd DEA
pip install -r requirements.txt
```

Download the raw datasets and place them in `data_raw/`, then run the processing pipeline:

```bash
python data_processing.py
python db_ops.py
```

Launch the dashboard:

```bash
streamlit run streamlit_app.py
```

## Stack

- **Python** — data processing and pipeline scripts
- **Polars** — data transformation
- **DuckDB** — analytical database
- **Streamlit** — dashboard
