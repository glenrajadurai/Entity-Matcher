import pandas as pd
import numpy as np
import json
import re

# Load TSV files with sep="\t"
s1 = pd.read_csv('data/official/source1.tsv', sep='\t')
s2 = pd.read_csv('data/official/source2.tsv', sep='\t')
s3 = pd.read_csv('data/official/source3.tsv', sep='\t')
gt = pd.read_csv('data/official/ground_truth.tsv', sep='\t')

audit_results = {}

# 1 & 2. Row and Column Counts
audit_results['row_counts'] = {'S1': len(s1), 'S2': len(s2), 'S3': len(s3), 'GT': len(gt)}
audit_results['columns'] = {'S1': list(s1.columns), 'S2': list(s2.columns), 'S3': list(s3.columns), 'GT': list(gt.columns)}

# 3. Missing values by field and source
missing_s1 = s1.isnull().sum().to_dict()
missing_s2 = s2.isnull().sum().to_dict()
missing_s3 = s3.isnull().sum().to_dict()
audit_results['missing_values'] = {'S1': missing_s1, 'S2': missing_s2, 'S3': missing_s3}

# 4. Country distribution
audit_results['country_dist'] = {
    'S1': s1['country'].value_counts().to_dict(),
    'S2': s2['country'].value_counts().to_dict(),
    'S3': s3['country'].value_counts().to_dict()
}

# 5. Duplicate business names
for name, df in [('S1', s1), ('S2', s2), ('S3', s3)]:
    names = df['business_name'].dropna()
    exact_dupes = names.duplicated().sum()
    norm_names = names.str.lower().str.replace(r'[^\w\s]', '', regex=True)
    norm_dupes = norm_names.duplicated().sum()
    audit_results[f'duplicate_names_{name}'] = {
        'exact_duplicates': int(exact_dupes),
        'normalized_duplicates': int(norm_dupes),
        'total_non_null': len(names)
    }

# 6. Duplicate/near-duplicate addresses
for name, df in [('S1', s1), ('S2', s2), ('S3', s3)]:
    addrs = df['business_address'].dropna()
    exact_dupes = addrs.duplicated().sum()
    norm_addrs = addrs.str.lower().str.replace(r'[^\w\s]', '', regex=True)
    norm_dupes = norm_addrs.duplicated().sum()
    audit_results[f'duplicate_addresses_{name}'] = {
        'exact_duplicates': int(exact_dupes),
        'normalized_duplicates': int(norm_dupes),
        'total_non_null': len(addrs)
    }

# 7. Length distributions (character and word counts)
for name, df in [('S1', s1), ('S2', s2), ('S3', s3)]:
    b_names = df['business_name'].dropna().astype(str)
    b_addrs = df['business_address'].dropna().astype(str)
    
    name_lens = b_names.apply(len)
    name_words = b_names.apply(lambda x: len(x.split()))
    
    addr_lens = b_addrs.apply(len)
    addr_words = b_addrs.apply(lambda x: len(x.split()))
    
    audit_results[f'length_dist_{name}'] = {
        'name_char_len': {'min': int(name_lens.min()), 'max': int(name_lens.max()), 'mean': round(float(name_lens.mean()), 2), 'median': float(name_lens.median())},
        'name_word_len': {'min': int(name_words.min()), 'max': int(name_words.max()), 'mean': round(float(name_words.mean()), 2), 'median': float(name_words.median())},
        'addr_char_len': {'min': int(addr_lens.min()), 'max': int(addr_lens.max()), 'mean': round(float(addr_lens.mean()), 2), 'median': float(addr_lens.median())},
        'addr_word_len': {'min': int(addr_words.min()), 'max': int(addr_words.max()), 'mean': round(float(addr_words.mean()), 2), 'median': float(addr_words.median())}
    }

# 8. Unusual characters / scripts / non-ASCII
non_ascii_pattern = re.compile(r'[^\x00-\x7F]')
for name, df in [('S1', s1), ('S2', s2), ('S3', s3)]:
    non_ascii_names = df['business_name'].dropna().apply(lambda x: bool(non_ascii_pattern.search(x))).sum()
    non_ascii_addrs = df['business_address'].dropna().apply(lambda x: bool(non_ascii_pattern.search(x))).sum()
    audit_results[f'unusual_chars_{name}'] = {
        'non_ascii_names_count': int(non_ascii_names),
        'non_ascii_addrs_count': int(non_ascii_addrs)
    }

# 9. Incomplete records (missing either name or address)
for name, df in [('S1', s1), ('S2', s2), ('S3', s3)]:
    incomplete = df[df['business_name'].isnull() | df['business_address'].isnull()]
    audit_results[f'incomplete_records_{name}'] = int(len(incomplete))

# 10. Ground truth match distribution
# Match counts per S1 entity for S2 and S3
gt_s2 = gt[gt['source_id'] == 'Source2']
gt_s3 = gt[gt['source_id'] == 'Source3']

s1_ids = s1['entity_id'].unique()

s2_match_counts = pd.Series(0, index=s1_ids)
s2_counts = gt_s2['s1_entity_id'].value_counts()
s2_match_counts.update(s2_counts)

s3_match_counts = pd.Series(0, index=s1_ids)
s3_counts = gt_s3['s1_entity_id'].value_counts()
s3_match_counts.update(s3_counts)

total_match_counts = pd.Series(0, index=s1_ids)
gt_all_counts = gt['s1_entity_id'].value_counts()
total_match_counts.update(gt_all_counts)

audit_results['gt_match_dist_s2'] = s2_match_counts.value_counts().to_dict()
audit_results['gt_match_dist_s3'] = s3_match_counts.value_counts().to_dict()
audit_results['gt_match_dist_total'] = total_match_counts.value_counts().to_dict()

# Breakdown zero-match, one-match, many-match entities
audit_results['entity_match_breakdown'] = {
    'S2': {
        'zero_match': int((s2_match_counts == 0).sum()),
        'one_match': int((s2_match_counts == 1).sum()),
        'many_match': int((s2_match_counts > 1).sum())
    },
    'S3': {
        'zero_match': int((s3_match_counts == 0).sum()),
        'one_match': int((s3_match_counts == 1).sum()),
        'many_match': int((s3_match_counts > 1).sum())
    },
    'Combined': {
        'zero_match': int((total_match_counts == 0).sum()),
        'one_match': int((total_match_counts == 1).sum()),
        'many_match': int((total_match_counts > 1).sum())
    }
}

# Print summary
print(json.dumps(audit_results, indent=2))

with open('scratch/audit_results.json', 'w') as f:
    json.dump(audit_results, f, indent=2)
