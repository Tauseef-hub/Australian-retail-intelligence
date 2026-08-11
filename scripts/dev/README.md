# Development scripts

One-off utilities used while building and validating the pipeline. They are not
part of the deployed service — the API entry point is `src/api/main.py` and the
pipeline lives under `src/`.

| Script | Purpose |
|---|---|
| `health_check.py` | Print database connectivity and table counts from the local `.env` |
| `verify_data_quality.py` | Row-level quality checks on the cleaned dataset |
| `check_historical_data.py` | Inspect the loaded historical series |
| `check_forecasts.py` / `check_total_forecasts.py` | Count and spot-check generated forecasts |
| `check_forecast_pattern.py` | Sanity-check forecast shape against history |
| `check_m1_duplicates.py` | Detect duplicate rows in the raw ABS M1 extract |
| `debug_abs_api.py` | Probe the ABS SDMX API response format |
| `test_transformation.py` | Ad-hoc check of the ETL transformation step |
| `fix_all_forecasts.py` | Backfill/repair forecast rows after a schema change |
| `clear_all_data.py` | Truncate all tables — destructive, local use only |
