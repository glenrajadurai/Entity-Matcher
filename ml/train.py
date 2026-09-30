import os
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier

def train_candidate_models(
    X_train: pd.DataFrame,
    y_train: np.ndarray,
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Trains candidate models (LightGBM, XGBoost, CatBoost)
    using identical training data and hyperparameters defined in model_config.yaml.
    Handles class imbalance using scale_pos_weight.
    """
    models = {}
    
    # Calculate scale pos weight for imbalance
    pos_count = np.sum(y_train == 1)
    neg_count = np.sum(y_train == 0)
    scale_pos_weight = neg_count / max(1, pos_count)
    
    # 1. LightGBM
    lgb_cfg = config.get('models', {}).get('lightgbm', {})
    lgb = LGBMClassifier(
        n_estimators=lgb_cfg.get('n_estimators', 300),
        learning_rate=lgb_cfg.get('learning_rate', 0.05),
        max_depth=lgb_cfg.get('max_depth', 6),
        scale_pos_weight=scale_pos_weight,
        random_state=lgb_cfg.get('random_state', 42),
        verbose=-1
    )
    lgb.fit(X_train, y_train)
    models['LightGBM'] = lgb
    
    # 2. XGBoost
    xgb_cfg = config.get('models', {}).get('xgboost', {})
    xgb = XGBClassifier(
        n_estimators=xgb_cfg.get('n_estimators', 300),
        learning_rate=xgb_cfg.get('learning_rate', 0.05),
        max_depth=xgb_cfg.get('max_depth', 6),
        scale_pos_weight=scale_pos_weight,
        random_state=xgb_cfg.get('random_state', 42),
        eval_metric='logloss'
    )
    xgb.fit(X_train, y_train)
    models['XGBoost'] = xgb
    
    # 3. CatBoost
    cat_cfg = config.get('models', {}).get('catboost', {})
    cat = CatBoostClassifier(
        iterations=cat_cfg.get('iterations', 300),
        learning_rate=cat_cfg.get('learning_rate', 0.05),
        depth=cat_cfg.get('depth', 6),
        scale_pos_weight=scale_pos_weight,
        random_seed=cat_cfg.get('random_seed', 42),
        verbose=0
    )
    cat.fit(X_train, y_train)
    models['CatBoost'] = cat

    return models

