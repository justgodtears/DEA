# NFZ Data Pipeline

A personal data engineering project built on publicly available Polish National Health Fund (NFZ) datasets.

## Current State

The project currently includes a DuckDB analytical database with:

- **Full ICD-10 dictionary in Polish** — a complete, structured table of ICD-10 codes with Polish disease names, not available in this form anywhere else online
- **Bilingual ICD-10 lookup table** — a clean Polish/English dictionary of ICD-10 codes, deduplicated and ready for joins

## Planned

- Patient statistics by diagnosis and hospital loaded as a fact table
- Hospital dictionary with geolocation
- Interactive map in Streamlit — click a hospital to see which diseases were treated and how many patients
- Streamlit dashboard with KPI visualizations

## Stack

- **Python** — data processing and pipeline scripts
- **Polars** — data transformation
- **DuckDB** — analytical database

## Status

Work in progress.