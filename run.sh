#!/usr/bin/env bash
# One-command bootstrap: creates a virtualenv, installs dependencies, trains
# the models if needed, and launches the dashboard.
#
# Usage:
#   ./run.sh            # setup + train (if needed) + dashboard
#   ./run.sh api        # setup + train (if needed) + inference API
set -euo pipefail
cd "$(dirname "$0")"

VENV=".venv"
TARGET="${1:-dashboard}"

if [ ! -d "$VENV" ]; then
    echo "==> Creating virtual environment in $VENV"
    python3 -m venv "$VENV"
fi

echo "==> Installing dependencies"
"$VENV/bin/pip" install --upgrade pip -q
"$VENV/bin/pip" install -r requirements.txt -q

if [ ! -f "models/metrics.json" ]; then
    echo "==> No trained artifacts found — training models (this runs once)"
    "$VENV/bin/python" -m src.train
else
    echo "==> Found existing models/metrics.json — skipping training"
fi

case "$TARGET" in
    dashboard)
        echo "==> Launching dashboard at http://localhost:8501"
        "$VENV/bin/streamlit" run src/dashboard.py
        ;;
    api)
        echo "==> Launching API at http://localhost:8000 (docs at /docs)"
        "$VENV/bin/python" -m uvicorn src.api:app --host 0.0.0.0 --port 8000
        ;;
    *)
        echo "Unknown target '$TARGET'. Use 'dashboard' or 'api'."
        exit 1
        ;;
esac
