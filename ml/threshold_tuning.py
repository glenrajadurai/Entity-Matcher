import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from ml.evaluate import compute_er_metrics

def tune_decision_threshold(
    y_true: np.ndarray, 
    y_pred_proba: np.ndarray, 
    config: Dict[str, Any]
) -> Tuple[float, Dict[str, Any], pd.DataFrame]:
    """
    Searches for the optimal decision threshold using ONLY the validation set.
    Evaluates thresholds from min_threshold to max_threshold at step intervals.
    Optimizes for F0.5 (or configured metric).
    """
    cfg = config.get('threshold_tuning', {})
    min_t = cfg.get('min_threshold', 0.05)
    max_t = cfg.get('max_threshold', 0.95)
    step = cfg.get('step', 0.02)
    primary_metric = cfg.get('metric', 'f0_5')
    
    thresholds = np.arange(min_t, max_t + step / 2, step)
    results = []
    
    best_threshold = 0.5
    best_score = -1.0
    best_metrics = {}
    
    for t in thresholds:
        metrics = compute_er_metrics(y_true, y_pred_proba, threshold=t)
        metrics['threshold'] = float(t)
        results.append(metrics)
        
        score = metrics.get(primary_metric, 0.0)
        if score > best_score:
            best_score = score
            best_threshold = float(t)
            best_metrics = metrics
            
    results_df = pd.DataFrame(results)
    return best_threshold, best_metrics, results_df
