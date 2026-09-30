import pandas as pd
import numpy as np
from typing import Tuple, List, Dict, Any

def detect_feature_columns(df: pd.DataFrame, config: Dict[str, Any]) -> List[str]:
    """
    Automatically detects usable feature columns by excluding ID columns,
    metadata, and target label. Open-set fields like country are left un-hardcoded.
    """
    exclude = set(config['data'].get('exclude_cols', []))
    feature_cols = [c for c in df.columns if c not in exclude]
    return feature_cols

def create_entity_level_split(
    df: pd.DataFrame, 
    config: Dict[str, Any]
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Creates an entity-level leakage-safe train/validation split using pure pandas/numpy.
    Guarantees that all candidate pairs belonging to the same s1_entity_id
    remain strictly within either train or validation, preventing entity leakage.
    """
    s1_col = config['data']['s1_id_col']
    val_size = config['split'].get('val_size', 0.2)
    random_state = config['split'].get('random_state', 42)

    unique_s1 = df[s1_col].unique()
    np.random.seed(random_state)
    np.random.shuffle(unique_s1)
    
    n_val = int(len(unique_s1) * val_size)
    val_entities = set(unique_s1[:n_val])
    
    val_mask = df[s1_col].isin(val_entities)
    train_df = df[~val_mask].reset_index(drop=True)
    val_df = df[val_mask].reset_index(drop=True)
    
    return train_df, val_df

