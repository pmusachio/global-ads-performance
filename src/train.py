#!/usr/bin/env python3
"""Trains the per-channel revenue models and persists the deployment artifacts.

This script reproduces the modeling steps from `notebooks/budget_optimization.ipynb`
end to end (data load -> feature engineering -> model fit -> evaluation ->
persistence), so the API and dashboard can be served without opening Jupyter.

Usage:
    python -m src.train
"""
import json
import os
import random
import time
import warnings

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import Pipeline

from src.optimizer import optimize_allocation
from src.transformers import AdstockTransformer, SaturationRegressor

warnings.filterwarnings("ignore")

SEED = 42
np.random.seed(SEED)
random.seed(SEED)

DATA_URL = "https://raw.githubusercontent.com/pmusachio/global-ads-performance/refs/heads/main/data/raw.csv"
DATA_PATH = "data/raw.csv"
MODELS_DIR = "models"
INDUSTRY_FILTER = "E-commerce"

# Business policy used to validate the saved optimization snapshot.
TOTAL_BUDGET = 15_000
MIN_ROAS_GLOBAL = 1.3
MIN_SHARE = 0.10
MAX_SHARE = 0.60


def load_data(url: str = DATA_URL, local_path: str = DATA_PATH) -> pd.DataFrame:
    """Loads the raw dataset, falling back to the public URL on first run."""
    if os.path.exists(local_path):
        df = pd.read_csv(local_path, parse_dates=["date"])
        print(f"Loaded {len(df):,} rows from {local_path}")
    else:
        df = pd.read_csv(url, parse_dates=["date"])
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        df.to_csv(local_path, index=False)
        print(f"Loaded {len(df):,} rows from remote URL and cached to {local_path}")
    return df


def prepare_channel_data(daily: pd.DataFrame, channels):
    """Builds chronological 70/15/15 train/val/test splits for each channel."""
    data_by_channel = {}
    for channel in channels:
        cdf = daily[daily["platform"] == channel].sort_values("date").reset_index(drop=True)
        X = cdf["ad_spend"].values.reshape(-1, 1)
        y = cdf["revenue"].values

        n = len(cdf)
        train_end = int(n * 0.7)
        val_end = int(n * 0.85)

        data_by_channel[channel] = {
            "X_train": X[:train_end], "y_train": y[:train_end],
            "X_val": X[train_end:val_end], "y_val": y[train_end:val_end],
            "X_test": X[val_end:], "y_test": y[val_end:],
        }
    return data_by_channel


def main():
    print("=" * 60)
    print("TRAINING PIPELINE - Marketing Budget Optimization")
    print("=" * 60)

    df_raw = load_data()
    df = df_raw[df_raw["industry"] == INDUSTRY_FILTER].copy()
    channels = sorted(df["platform"].unique())
    print(f"Filtered to '{INDUSTRY_FILTER}': {len(df):,} rows across {len(channels)} channels")

    daily = (
        df.groupby(["date", "platform"])
        .agg(ad_spend=("ad_spend", "sum"), revenue=("revenue", "sum"))
        .reset_index()
    )

    data_by_channel = prepare_channel_data(daily, channels)
    print("Built chronological 70/15/15 train/val/test splits per channel")

    final_models = {}
    for channel in channels:
        d = data_by_channel[channel]
        X_trainval = np.vstack([d["X_train"], d["X_val"]])
        y_trainval = np.concatenate([d["y_train"], d["y_val"]])

        model = SaturationRegressor(L_init=max(y_trainval) * 1.5, k_init=5e-4)
        model.fit(X_trainval, y_trainval)
        final_models[channel] = model
        print(f"  {channel:<12} fitted -> L={model.L_:,.2f}  k={model.k_:.6f}")

    os.makedirs(MODELS_DIR, exist_ok=True)

    # 1. Persist one end-to-end pipeline (adstock -> saturation model) per channel.
    for channel, model in final_models.items():
        pipeline = Pipeline([
            ("adstock", AdstockTransformer(decay_rate=0.3)),
            ("model", model),
        ])
        filename = f"{MODELS_DIR}/pipeline_{channel.replace(' ', '_').lower()}.joblib"
        joblib.dump(pipeline, filename)
        print(f"  saved {filename}")

    # 2. Persist a reference optimization snapshot under the default business policy.
    channel_params = {c: {"L": m.L_, "k": m.k_} for c, m in final_models.items()}
    opt_result = optimize_allocation(
        channel_params, total_budget=TOTAL_BUDGET, min_roas=MIN_ROAS_GLOBAL,
        min_share=MIN_SHARE, max_share=MAX_SHARE,
    )
    joblib.dump(opt_result, f"{MODELS_DIR}/optimization_result.joblib")

    # 3. Persist evaluation metrics + saturation params for serving / monitoring.
    metrics = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "optimization": opt_result,
        "channels": {},
    }
    for channel in channels:
        d = data_by_channel[channel]
        y_pred = np.maximum(final_models[channel].predict(d["X_test"]), 0)
        metrics["channels"][channel] = {
            "r2_test": float(r2_score(d["y_test"], y_pred)),
            "rmse_test": float(np.sqrt(mean_squared_error(d["y_test"], y_pred))),
            "saturation_params": {"L": float(final_models[channel].L_), "k": float(final_models[channel].k_)},
        }

    with open(f"{MODELS_DIR}/metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    print("\n" + "=" * 60)
    print(f"Done. Artifacts written to '{MODELS_DIR}/':")
    for fname in sorted(os.listdir(MODELS_DIR)):
        size = os.path.getsize(os.path.join(MODELS_DIR, fname))
        print(f"  {fname}  ({size:,} bytes)")
    print("=" * 60)
    print("\nNext steps:")
    print("  uvicorn src.api:app --reload          # start the inference API")
    print("  streamlit run src/dashboard.py        # start the interactive dashboard")


if __name__ == "__main__":
    main()
