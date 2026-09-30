import os
import joblib
import pandas as pd
import numpy as np
from typing import Union, Dict

def predict_pairs(
    feature_df: pd.DataFrame, 
    model_dir: str = "models/final/"
) -> pd.DataFrame:
    """
    Inference module to generate match probabilities and predictions for new feature tables
    produced by Member 2. Uses the saved best model and optimal validation threshold.
    """
    model_path = os.path.join(model_dir, "best_model.joblib")
    meta_path = os.path.join(model_dir, "model_metadata.joblib")
    
    if not os.path.exists(model_path) or not os.path.exists(meta_path):
        raise FileNotFoundError(f"Model or metadata not found in {model_dir}. Run training first.")
        
    model = joblib.load(model_path)
    metadata = joblib.load(meta_path)
    
    feature_cols = metadata["feature_columns"]
    threshold = metadata["best_threshold"]
    
    # Ensure all required features are present
    missing_cols = [c for c in feature_cols if c not in feature_df.columns]
    if missing_cols:
        raise ValueError(f"Input feature table is missing required columns: {missing_cols}")
        
    X = feature_df[feature_cols]
    
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X)[:, 1]
    else:
        probs = model.predict(X)
        
    preds = (probs >= threshold).astype(int)
    
    output_df = feature_df.copy()
    output_df["match_probability"] = probs
    output_df["is_match_prediction"] = preds
    output_df["applied_threshold"] = threshold
    
    return output_df
