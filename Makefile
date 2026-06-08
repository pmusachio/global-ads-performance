.PHONY: setup train api dashboard run clean

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

# Creates a virtual environment and installs all dependencies.
setup:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "\nSetup complete. Activate it with: source $(VENV)/bin/activate"

# Trains the models and writes the artifacts to models/ (skips if they already exist).
train:
	@if [ -f models/metrics.json ]; then \
		echo "models/metrics.json already exists — skipping training. Run 'make train-force' to retrain."; \
	else \
		$(PYTHON) -m src.train; \
	fi

train-force:
	$(PYTHON) -m src.train

# Starts the inference API on http://localhost:8000 (docs at /docs).
api:
	$(PYTHON) -m uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload

# Starts the interactive dashboard on http://localhost:8501.
dashboard:
	$(VENV)/bin/streamlit run src/dashboard.py

# One-shot: install deps, train if needed, then launch the dashboard.
run: setup train dashboard

clean:
	rm -rf $(VENV) models/*.joblib models/metrics.json
