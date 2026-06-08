# 🎯 Global Ads Performance — Marketing Budget Optimization

End-to-end machine learning project that models how digital ad spend converts
into revenue across channels (Google Ads, Meta Ads, TikTok Ads), and uses
those models to recommend the **daily budget allocation that maximizes
revenue** under business constraints (total budget, minimum ROAS, per-channel
share limits).

The project follows the end-to-end ML project workflow described in
*Hands-On Machine Learning with Scikit-Learn and PyTorch* (Aurélien Géron):
frame the problem → explore the data → engineer features and pipelines →
shortlist and tune models → evaluate and interpret → ship a reproducible,
servable artifact.

> Built as a portfolio piece to demonstrate an end-to-end data science
> workflow: from exploratory analysis in a notebook to a served model behind
> a REST API and an interactive dashboard.

---

## 🧠 What the project does

1. **Models channel-level revenue response.** For each ad channel, a custom
   `SaturationRegressor` fits a diminishing-returns curve
   `revenue = L · (1 − e^(−k · spend))`, capturing the fact that extra spend
   yields progressively smaller returns. An `AdstockTransformer` models the
   carryover effect of yesterday's spend on today's revenue.
2. **Validates with time-aware techniques.** Chronological train/val/test
   splits, `TimeSeriesSplit` cross-validation, learning curves and residual
   analysis — avoiding the leakage that a random split would introduce on
   time series data.
3. **Optimizes the budget allocation.** Given the fitted saturation curves,
   `scipy.optimize.minimize` (SLSQP) finds the spend allocation that maximizes
   total predicted revenue subject to: a total budget cap, a minimum global
   ROAS, and minimum/maximum share-of-budget bounds per channel.
4. **Serves the result two ways**: a FastAPI inference service for
   programmatic access, and a Streamlit dashboard for interactive
   exploration and what-if simulation.

---

## 🗂️ Project structure

```
global-ads-performance/
├── notebooks/
│   └── budget_optimization.ipynb   # Exploratory analysis + full modeling walkthrough
├── src/
│   ├── transformers.py             # Shared custom sklearn components (Adstock, SaturationRegressor)
│   ├── optimizer.py                # Budget allocation optimizer (shared by API & dashboard)
│   ├── train.py                    # Reproducible training pipeline -> writes models/
│   ├── api.py                      # FastAPI inference & optimization service
│   └── dashboard.py                # Streamlit interactive dashboard
├── data/
│   └── raw.csv                     # Historical ad performance dataset
├── models/                         # Generated artifacts: pipelines, metrics.json (git-ignored after first run)
├── requirements.txt
├── Makefile                        # make setup / train / api / dashboard
├── run.sh                          # One-command bootstrap (setup + train + serve)
└── docs/                           # Supplementary MLOps notes
```

The notebook (`notebooks/budget_optimization.ipynb`) is the original research
artifact — written in Portuguese with direct citations to the *Hands-On ML*
chapters that motivate each step. The `src/` package is the productionized,
English-documented version of the same pipeline, refactored so the API and
dashboard share a single source of truth for the model and optimization logic.

---

## 🚀 How to run it (for recruiters & reviewers)

You only need Python 3.9+. Two equivalent options:

### Option A — one-line bootstrap script

```bash
git clone https://github.com/pmusachio/global-ads-performance.git
cd global-ads-performance
./run.sh            # creates a venv, installs deps, trains the models (first run only),
                    # and launches the dashboard at http://localhost:8501
```

To launch the API instead of the dashboard:

```bash
./run.sh api        # serves http://localhost:8000  (interactive docs at /docs)
```

### Option B — Makefile

```bash
make setup          # create .venv and install dependencies
make train          # train models and write artifacts to models/ (skipped if already present)
make dashboard      # streamlit dashboard at http://localhost:8501
make api            # FastAPI service at http://localhost:8000
```

### Option C — manual steps

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.train                       # trains models, writes models/*.joblib + metrics.json
streamlit run src/dashboard.py             # or: uvicorn src.api:app --reload
```

> The first run trains the models from `data/raw.csv` (falls back to the
> dataset's public GitHub URL if the file is missing) and writes the
> artifacts to `models/`. Subsequent runs reuse them — no retraining needed.

---

## 🔌 API reference

Once the API is running (`http://localhost:8000`), interactive docs are
available at `/docs` (Swagger UI). Main endpoints:

| Method | Endpoint     | Description                                                        |
|--------|--------------|--------------------------------------------------------------------|
| GET    | `/`          | Health check + list of loaded channel models                      |
| POST   | `/predict`   | Predicts revenue for a given `{channel: spend}` allocation        |
| GET    | `/metrics`   | Returns the latest training run metrics (R², RMSE, fitted params) |
| POST   | `/optimize`  | Recommends the revenue-maximizing allocation under constraints    |

Example:

```bash
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{"total_budget": 15000, "min_roas": 2.0, "min_share": 0.10, "max_share": 0.50}'
```

```json
{
  "success": true,
  "allocation": {"Google Ads": 1719.16, "Meta Ads": 4280.84, "TikTok Ads": 9000.0},
  "estimated_revenue": 102553.78,
  "estimated_spend": 15000.0,
  "estimated_roas": 6.84
}
```

---

## 📊 Dashboard

The Streamlit dashboard (`src/dashboard.py`) provides:

- **Simulator & Optimizer tab** — sliders for total budget, minimum ROAS, and
  per-channel share bounds; live-recomputed optimal allocation, projected
  revenue/ROAS, and saturation-curve visualizations showing where each
  channel sits on its diminishing-returns curve.
- **Historical Data tab** — raw dataset preview and a macro view of spend vs.
  revenue over time.

---

## 🧪 Methodology highlights

- **Domain-informed modeling**: instead of a generic regressor, the channel
  response is modeled with a parametric saturation curve `L·(1 − e^(−k·x))`,
  which is interpretable (`L` = revenue ceiling, `k` = saturation speed) and
  directly usable inside the optimizer's objective function.
- **Time-aware validation**: chronological 70/15/15 splits and
  `TimeSeriesSplit` cross-validation prevent look-ahead bias inherent to ad
  performance time series.
- **Reproducibility**: `src/train.py` is a deterministic, single-command
  reproduction of the full notebook pipeline (seeded, idempotent artifact
  generation), so the served models can always be regenerated from raw data.
- **Single source of truth**: `src/transformers.py` and `src/optimizer.py`
  are imported by training, the API, and the dashboard — eliminating the
  drift risk of duplicated model/optimization code across services.

---

## 🛠️ Tech stack

`Python` · `scikit-learn` · `SciPy` (curve fitting & constrained optimization)
· `pandas` / `numpy` · `FastAPI` + `uvicorn` · `Streamlit` · `matplotlib`

---

## 📄 License

See [LICENSE](LICENSE).
