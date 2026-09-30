import numpy as np
import pandas as pd
from typing import Dict, Any

def compute_er_metrics(y_true: np.ndarray, y_pred_proba: np.ndarray, threshold: float = 0.5) -> Dict[str, Any]:
    """
    Computes comprehensive ER evaluation metrics using native NumPy.
    Includes Precision, Recall, F0.5 (primary), F1, PR-AUC, Confusion Matrix, FP & FN counts.
    """
    y_pred = (y_pred_proba >= threshold).astype(int)
    
    tp = int(np.sum((y_pred == 1) & (y_true == 1)))
    fp = int(np.sum((y_pred == 1) & (y_true == 0)))
    fn = int(np.sum((y_pred == 0) & (y_true == 1)))
    tn = int(np.sum((y_pred == 0) & (y_true == 0)))
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0.0
    
    beta = 0.5
    beta_sq = beta ** 2
    f0_5 = (1 + beta_sq) * (precision * recall) / (beta_sq * precision + recall) if (precision + recall) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    # Calculate PR-AUC via trapezoidal rule over sorted probability thresholds
    sort_idx = np.argsort(y_pred_proba)[::-1]
    y_true_sorted = y_true[sort_idx]
    
    tps = np.cumsum(y_true_sorted == 1)
    fps = np.cumsum(y_true_sorted == 0)
    
    precisions = tps / (tps + fps)
    recalls = tps / np.sum(y_true == 1) if np.sum(y_true == 1) > 0 else np.zeros_like(tps)
    
    pr_auc = float(np.trapezoid(precisions, recalls)) if len(recalls) > 1 else 0.0
    
    return {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f0_5": float(f0_5),
        "f1": float(f1),
        "pr_auc": abs(float(pr_auc)),
        "false_positives": fp,
        "false_negatives": fn,
        "true_positives": tp,
        "true_negatives": tn,
        "confusion_matrix": [[tn, fp], [fn, tp]]
    }


