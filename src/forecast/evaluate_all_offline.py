"""
Offline model-accuracy evaluation (no database required).

Backtests the Prophet forecasting models across ALL 192 category/state series
using the committed transformed dataset, so the reported accuracy is fully
reproducible without the production database. For each series with >= 24 months
of history it trains on all-but-the-last-6 months, forecasts 6 months, and
measures MAPE against the held-out actuals -- the same protocol as
evaluate_model.py, but over every series instead of only a top-5 sample.

Run:
    python src/forecast/evaluate_all_offline.py

Writes results/metrics.json.
"""
import json
import logging
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
for _name in ("prophet", "cmdstanpy"):
    logging.getLogger(_name).setLevel(logging.CRITICAL)
from prophet import Prophet  # noqa: E402  (import after logging config)

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "abs_transformed_full.csv"
OUT = ROOT / "results" / "metrics.json"
TEST_MONTHS = 6


def backtest_series(group: pd.DataFrame) -> float | None:
    """Return the 6-month hold-out MAPE (%) for one category/state series."""
    group = group.sort_values("sale_date")
    if len(group) < 24:
        return None
    train, test = group.iloc[:-TEST_MONTHS], group.iloc[-TEST_MONTHS:]
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False,
        seasonality_mode="multiplicative",
    )
    model.add_country_holidays(country_name="AU")
    model.fit(pd.DataFrame({"ds": train["sale_date"].values, "y": train["turnover_millions"].values}))
    future = model.make_future_dataframe(periods=TEST_MONTHS, freq="MS")
    predicted = model.predict(future).tail(TEST_MONTHS)["yhat"].values
    actual = test["turnover_millions"].values
    return float(np.mean(np.abs((actual - predicted) / actual)) * 100)


def main() -> None:
    df = pd.read_csv(DATA, parse_dates=["sale_date"])
    df["category"] = df["category"].astype(str)
    df["state"] = df["state"].astype(str)
    sizes = df.groupby(["category", "state"]).size()

    rows = []
    for (category, state), group in df.groupby(["category", "state"]):
        mape = backtest_series(group)
        if mape is not None:
            rows.append({"category": category, "state": state, "mape_pct": round(mape, 2)})
            print(f"[{len(rows)}] cat {category} / state {state}: MAPE {mape:.2f}%")

    results = pd.DataFrame(rows)
    top5 = {tuple(map(str, k)) for k in sizes.sort_values(ascending=False).head(5).index}
    top5_rows = results[[(c, s) in top5 for c, s in zip(results["category"], results["state"])]]

    summary = {
        "method": "6-month hold-out backtest per series; Prophet yearly + multiplicative + AU holidays",
        "series_evaluated": int(len(results)),
        "all_series_mean_mape_pct": round(float(results["mape_pct"].mean()), 2),
        "all_series_median_mape_pct": round(float(results["mape_pct"].median()), 2),
        "share_of_series_under_10pct": round(float((results["mape_pct"] < 10).mean() * 100), 1),
        "best": results.nsmallest(1, "mape_pct").to_dict("records")[0],
        "worst": results.nlargest(1, "mape_pct").to_dict("records")[0],
        "top5_high_volume_mean_mape_pct": round(float(top5_rows["mape_pct"].mean()), 2),
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({"summary": summary, "per_series": rows}, indent=2))
    print("\n" + json.dumps(summary, indent=2))
    print(f"\nSaved {OUT}")


if __name__ == "__main__":
    main()
