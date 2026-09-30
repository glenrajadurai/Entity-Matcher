import os
import sys
sys.path.insert(0, os.path.abspath('.'))

import pandas as pd
import json
from src.preprocessing.normalize import process_dataframe

os.makedirs('data/processed', exist_ok=True)
os.makedirs('reports', exist_ok=True)

# 1. Load Raw Datasets
s1_raw = pd.read_csv('data/official/source1.tsv', sep='\t')
s2_raw = pd.read_csv('data/official/source2.tsv', sep='\t')
s3_raw = pd.read_csv('data/official/source3.tsv', sep='\t')

# Store initial raw modification timestamps to check raw file integrity
raw_files = ['data/official/source1.tsv', 'data/official/source2.tsv', 'data/official/source3.tsv', 'data/official/ground_truth.tsv']
raw_mtimes_before = {f: os.path.getmtime(f) for f in raw_files}

# 2. Process Datasets
s1_proc = process_dataframe(s1_raw)
s2_proc = process_dataframe(s2_raw)
s3_proc = process_dataframe(s3_raw)

# 3. Save Processed Datasets
s1_proc.to_csv('data/processed/source1_normalized.tsv', sep='\t', index=False)
s2_proc.to_csv('data/processed/source2_normalized.tsv', sep='\t', index=False)
s3_proc.to_csv('data/processed/source3_normalized.tsv', sep='\t', index=False)

# 4. Perform Validations
val_results = {}

# Row counts
val_results['row_counts'] = {
    'S1': {'raw': len(s1_raw), 'processed': len(s1_proc), 'pass': len(s1_raw) == 500 and len(s1_proc) == 500},
    'S2': {'raw': len(s2_raw), 'processed': len(s2_proc), 'pass': len(s2_raw) == 540 and len(s2_proc) == 540},
    'S3': {'raw': len(s3_raw), 'processed': len(s3_proc), 'pass': len(s3_raw) == 506 and len(s3_proc) == 506}
}

# ID Preservation & Uniqueness
val_results['id_preservation'] = {
    'S1': {'equal': list(s1_raw['entity_id']) == list(s1_proc['entity_id']), 'unique': bool(s1_proc['entity_id'].is_unique)},
    'S2': {'equal': list(s2_raw['entity_id']) == list(s2_proc['entity_id']), 'unique': bool(s2_proc['entity_id'].is_unique)},
    'S3': {'equal': list(s3_raw['entity_id']) == list(s3_proc['entity_id']), 'unique': bool(s3_proc['entity_id'].is_unique)}
}

# Raw Files Touch Verification
raw_mtimes_after = {f: os.path.getmtime(f) for f in raw_files}
val_results['raw_files_untouched'] = all(raw_mtimes_before[f] == raw_mtimes_after[f] for f in raw_files)

# Missing Value Metrics Before vs After
missing_metrics = {}
for name, raw_df, proc_df in [('S1', s1_raw, s1_proc), ('S2', s2_raw, s2_proc), ('S3', s3_raw, s3_proc)]:
    missing_metrics[name] = {
        'business_name_missing_raw': int(raw_df['business_name'].isnull().sum()),
        'business_name_missing_norm': int(proc_df['business_name_normalized'].isnull().sum()),
        'business_address_missing_raw': int(raw_df['business_address'].isnull().sum()),
        'business_address_missing_norm': int(proc_df['business_address_normalized'].isnull().sum()),
        'country_missing_raw': int(raw_df['country'].isnull().sum()),
        'country_missing_norm': int(proc_df['country_normalized'].isnull().sum())
    }
val_results['missing_values'] = missing_metrics

# Country Distribution Before vs After
country_metrics = {}
for name, raw_df, proc_df in [('S1', s1_raw, s1_proc), ('S2', s2_raw, s2_proc), ('S3', s3_raw, s3_proc)]:
    country_metrics[name] = {
        'raw': raw_df['country'].value_counts().to_dict(),
        'normalized': proc_df['country_normalized'].value_counts().to_dict()
    }
val_results['country_distribution'] = country_metrics

# Transformation Change Metrics (Counts of modified values)
change_metrics = {}
for name, proc_df in [('S1', s1_proc), ('S2', s2_proc), ('S3', s3_proc)]:
    name_changed = (proc_df['business_name'].astype(str) != proc_df['business_name_normalized'].astype(str)).sum()
    addr_changed = (proc_df['business_address'].astype(str) != proc_df['business_address_normalized'].astype(str)).sum()
    country_changed = (proc_df['country'].astype(str) != proc_df['country_normalized'].astype(str)).sum()
    
    change_metrics[name] = {
        'business_names_changed': int(name_changed),
        'business_addresses_changed': int(addr_changed),
        'countries_changed': int(country_changed)
    }
val_results['transformations_changed'] = change_metrics

print(json.dumps(val_results, indent=2))

with open('scratch/stage2_validation_results.json', 'w') as f:
    json.dump(val_results, f, indent=2)
