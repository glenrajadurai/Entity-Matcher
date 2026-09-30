import os
import yaml
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any

from ml.data_splitter import detect_feature_columns, create_entity_level_split
from ml.train import train_candidate_models
from ml.evaluate import compute_er_metrics
from ml.threshold_tuning import tune_decision_threshold

def run_model_comparison(data_path: str, config_path: str = "configs/model_config.yaml") -> Dict[str, Any]:
    """
    Runs fair model comparison across all candidate models using identical
    train/val splits, feature sets, target labels, and evaluation metrics.
    """
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        
    df = pd.read_csv(data_path)
    feature_cols = detect_feature_columns(df, config)
    target_col = config['data']['target_col']
    
    train_df, val_df = create_entity_level_split(df, config)
    
    X_train = train_df[feature_cols]
    y_train = train_df[target_col].values
    X_val = val_df[feature_cols]
    y_val = val_df[target_col].values
    
    models = train_candidate_models(X_train, y_train, config)
    
    comparison_results = []
    trained_evals = {}
    
    for model_name, model in models.items():
        if hasattr(model, "predict_proba"):
            val_probs = model.predict_proba(X_val)[:, 1]
        else:
            val_probs = model.predict(X_val)
            
        # Default 0.5 metrics
        default_metrics = compute_er_metrics(y_val, val_probs, threshold=0.5)
        
        # Validation Threshold Tuning
        best_threshold, tuned_metrics, _ = tune_decision_threshold(y_val, val_probs, config)
        
        trained_evals[model_name] = {
            "model": model,
            "val_probs": val_probs,
            "default_metrics": default_metrics,
            "best_threshold": best_threshold,
            "tuned_metrics": tuned_metrics
        }
        
        comparison_results.append({
            "Model": model_name,
            "Accuracy (0.5)": round(default_metrics["accuracy"], 4),
            "Precision (0.5)": round(default_metrics["precision"], 4),
            "Recall (0.5)": round(default_metrics["recall"], 4),
            "F0.5 (0.5)": round(default_metrics["f0_5"], 4),
            "F1 (0.5)": round(default_metrics["f1"], 4),
            "PR-AUC": round(default_metrics["pr_auc"], 4),
            "Optimal Threshold": round(best_threshold, 2),
            "Accuracy (Opt)": round(tuned_metrics["accuracy"], 4),
            "Precision (Opt)": round(tuned_metrics["precision"], 4),
            "Recall (Opt)": round(tuned_metrics["recall"], 4),
            "F0.5 (Opt)": round(tuned_metrics["f0_5"], 4),
            "F1 (Opt)": round(tuned_metrics["f1"], 4),
            "FP Count (Opt)": tuned_metrics["false_positives"],
            "FN Count (Opt)": tuned_metrics["false_negatives"]
        })
        
    comp_df = pd.DataFrame(comparison_results).sort_values(by="Accuracy (Opt)", ascending=False)

    
    # Identify winner based on validation F0.5
    winner_name = comp_df.iloc[0]["Model"]
    winner_info = trained_evals[winner_name]
    
    # Save winner model & metadata
    final_dir = config['output']['final_model_dir']
    os.makedirs(final_dir, exist_ok=True)
    
    joblib.dump(winner_info["model"], os.path.join(final_dir, "best_model.joblib"))
    
    metadata = {
        "best_model_name": winner_name,
        "best_threshold": winner_info["best_threshold"],
        "feature_columns": feature_cols,
        "target_col": target_col,
        "metrics_at_optimal_threshold": winner_info["tuned_metrics"]
    }
    joblib.dump(metadata, os.path.join(final_dir, "model_metadata.joblib"))
    
    # Save comparison table to markdown
    report_dir = config['output']['report_dir']
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, "model_comparison.md")
    
    with open(report_path, 'w') as f:
        f.write("# Model Comparison Report\n\n")
        f.write(f"**Empirically Selected Model:** {winner_name}\n")
        f.write(f"**Optimal Threshold:** {winner_info['best_threshold']:.2f}\n\n")
        f.write(comp_df.to_markdown(index=False))
        f.write("\n")
        
    return {
        "comparison_table": comp_df,
        "winner_name": winner_name,
        "winner_metadata": metadata,
        "val_df": val_df,
        "val_probs": winner_info["val_probs"],
        "feature_cols": feature_cols,
        "winner_model": winner_info["model"]
    }
