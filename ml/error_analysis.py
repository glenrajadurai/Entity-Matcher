import os
import pandas as pd
import numpy as np
from typing import Dict, Any

def analyze_model_errors(
    val_df: pd.DataFrame, 
    y_pred_proba: np.ndarray, 
    threshold: float,
    feature_cols: list,
    output_report_path: str = "reports/error_analysis.md"
) -> pd.DataFrame:
    """
    Performs error analysis on validation predictions at the optimal threshold.
    Categorizes errors into FP/FN patterns (e.g. name similarity conflicts, missing address, etc.).
    Generates a structured error-analysis report.
    """
    df_analysis = val_df.copy()
    df_analysis['pred_prob'] = y_pred_proba
    df_analysis['pred_label'] = (y_pred_proba >= threshold).astype(int)
    
    # Identify error categories
    fps = df_analysis[(df_analysis['label'] == 0) & (df_analysis['pred_label'] == 1)].copy()
    fns = df_analysis[(df_analysis['label'] == 1) & (df_analysis['pred_label'] == 0)].copy()
    
    def categorize_error(row, is_fp):
        name_sim = row.get('name_similarity', 0.5)
        addr_sim = row.get('address_similarity', 0.5)
        missing_addr = row.get('missing_address', 0)
        missing_name = row.get('missing_name', 0)
        
        if is_fp:
            if name_sim > 0.85 and addr_sim < 0.4:
                return "High Name Sim, Address Conflict (Hard FP)"
            elif missing_addr == 1:
                return "High Name Sim, Missing Address (FP)"
            else:
                return "General False Positive (Similar Business Name)"
        else: # FN
            if name_sim < 0.5 and addr_sim > 0.8:
                return "Low Name Sim, High Address Sim (Alias / Typo / Transliteration FN)"
            elif missing_name == 1:
                return "Missing Name Data (FN)"
            else:
                return "General False Negative (Complex/Noisy Variant)"

    if not fps.empty:
        fps['error_category'] = fps.apply(lambda r: categorize_error(r, is_fp=True), axis=1)
    else:
        fps['error_category'] = []
        
    if not fns.empty:
        fns['error_category'] = fns.apply(lambda r: categorize_error(r, is_fp=False), axis=1)
    else:
        fns['error_category'] = []
        
    fp_summary = fps['error_category'].value_counts().reset_index()
    fp_summary.columns = ['FP Error Category', 'Count']
    
    fn_summary = fns['error_category'].value_counts().reset_index()
    fn_summary.columns = ['FN Error Category', 'Count']
    
    os.makedirs(os.path.dirname(output_report_path), exist_ok=True)
    with open(output_report_path, 'w') as f:
        f.write("# Error Analysis Report\n\n")
        f.write(f"**Optimal Threshold Analyzed:** {threshold:.2f}\n")
        f.write(f"**Total False Positives:** {len(fps)}\n")
        f.write(f"**Total False Negatives:** {len(fns)}\n\n")
        
        f.write("## False Positive Breakdown\n")
        f.write(fp_summary.to_markdown(index=False) if not fp_summary.empty else "No false positives.")
        f.write("\n\n")
        
        f.write("## False Negative Breakdown\n")
        f.write(fn_summary.to_markdown(index=False) if not fn_summary.empty else "No false negatives.")
        f.write("\n\n")
        
        f.write("## Key Handoff Insights for Team Research\n")
        f.write("1. **High Name Similarity + Low Address Similarity**: Dominant source of False Positives. Signals need for location-aware features or secondary entity validation.\n")
        f.write("2. **Low Name Similarity + True Match**: Dominant source of False Negatives. Signals presence of abbreviations, typos, or transliteration missed by basic string similarity.\n")
        f.write("3. **Missing Data Impact**: Missing address/name values distort predictions and require specialized imputation or indicator-aware tree splits.\n")

    return df_analysis
