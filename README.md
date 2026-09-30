# ⚡ Business Entity Resolution (ER) System

A scalable, end-to-end Machine Learning and Record Linkage pipeline for Business Entity Resolution. The system includes multi-pass blocking, candidate pair generation, string & numeric similarity feature extraction, ML model comparison (LightGBM, XGBoost, CatBoost, HistGradientBoosting), threshold tuning, error analysis, a FastAPI backend service, and a Streamlit analytics dashboard.

---

## 🚀 Features

- **Record Linkage & Multi-Pass Blocking**: Exact, Soundex, Prefix, Year, and Compound blocking rules to prune search space while maintaining high recall.
- **Similarity Feature Extraction**: Jaro-Winkler, Levenshtein, N-gram Cosine similarity, token match, and numeric field comparison algorithms.
- **ML Model Comparison & Selection**: Automated cross-validation and hyperparameter evaluation for LightGBM, XGBoost, CatBoost, and HistGradientBoosting with threshold optimization.
- **Error Analysis & Diagnostics**: Automated breakdown of false positives, false negatives, feature importance, and error metrics exported to Markdown reports.
- **Interactive Analytics Dashboard**: Streamlit web dashboard for real-time model prediction inspection and metrics.
- **RESTful API Backend**: FastAPI server for real-time pairwise scoring and dataset batch predictions.

---

## 🛠️ Installation & Setup

1. **Set Up Python Virtual Environment**:
   ```bash
   python -m venv venv
   # Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # Linux/macOS:
   source venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚡ Quick Start: Running the Pipeline

Run the unified `main.py` script:

```bash
# Run End-to-End Pipeline (Candidate Generation + Feature Extraction + ML Training & Eval)
python main.py

# Run with explicit mode selection:
python main.py --mode all

# Run Record Linkage & Candidate Generation step only:
python main.py --mode linkage

# Run ML Model Comparison & Error Analysis only:
python main.py --mode ml --data_path extracted_features.csv --config_path configs/model_config.yaml
```

---

## 📊 Analytics Dashboard & API Services

### 1. Streamlit ML Analytics Dashboard
To run the interactive Streamlit dashboard:
```bash
streamlit run app.py
```

### 2. FastAPI Backend API
To launch the FastAPI backend server:
```bash
uvicorn backend_api:app --reload --port 8000
```
Interactive API docs will be accessible at `http://localhost:8000/docs`.

---

## 📂 Project Structure

```
├── main.py                  # Unified pipeline entrypoint (Linkage + Feature Extraction + ML)
├── app.py                   # Streamlit Analytics Dashboard
├── backend_api.py           # FastAPI backend server
├── generate_data.py         # Synthetic dataset generation utility
├── blocking.py              # Multi-pass blocking strategy implementations
├── candidate_generation.py  # Candidate pair generator
├── features.py              # Pairwise similarity feature extractor
├── recall.py                # Blocking recall & candidate evaluation
├── ml/                      # Machine learning modules
│   ├── compare_models.py    # Model trainer, cross-validation & comparison
│   ├── error_analysis.py    # Error diagnostics & report generation
│   └── predict.py          # Prediction inference pipeline
├── configs/                 # YAML configuration files
│   └── model_config.yaml    # ML pipeline parameters & model hyperparams
├── models/                  # Saved model artifacts & checkpoints
├── reports/                 # Markdown error analysis & evaluation reports
├── er-dashboard-ui/         # React + TypeScript UI Dashboard
└── requirements.txt         # Python project dependencies
```

