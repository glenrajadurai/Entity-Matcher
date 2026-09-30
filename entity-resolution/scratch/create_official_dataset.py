import os
import pandas as pd
import numpy as np

# Ensure directory structure exists
os.makedirs('data/official', exist_ok=True)
os.makedirs('data/stress_test', exist_ok=True)
os.makedirs('reports', exist_ok=True)

np.random.seed(42)

# Generate S1 (Master Entities)
countries = ['US', 'IN', 'FR', 'DE', 'GB', 'JP', 'CA', 'AU']
company_prefixes = ['Apex', 'Nexus', 'Vertex', 'Starlight', 'Omni', 'Horizon', 'Global', 'Synergy', 'Vanguard', 'Quantum', 'Biolab', 'Cybertech', 'Societe', 'Muller', 'Leclerc', 'Tata', 'Reliance', 'Satoshi']
company_types = ['Solutions', 'Technologies', 'Enterprises', 'Logistics', 'Industries', 'Pharmaceuticals', 'Holdings', 'Group', 'GmbH', 'S.A.', 'Ltd.', 'Corp.']
street_types = ['St', 'Street', 'Ave', 'Avenue', 'Blvd', 'Boulevard', 'Rd', 'Road', 'Way', 'Rue', 'Strasse', 'Chaussee']

s1_records = []
for i in range(1, 501):
    e_id = f"S1_{i:04d}"
    country = np.random.choice(countries, p=[0.3, 0.2, 0.15, 0.1, 0.1, 0.05, 0.05, 0.05])
    
    if country == 'FR':
        b_name = f"{np.random.choice(['Societe', 'Groupe', 'Compagnie', 'Atelier'])} {np.random.choice(['Dufour', 'Moreau', 'Laurent', 'Girard'])} {np.random.choice(['S.A.', 'S.A.R.L.', 'SAS'])}"
        b_addr = f"{np.random.randint(1, 200)} {np.random.choice(['Rue de la Paix', 'Avenue des Champs-Elysees', 'Boulevard Saint-Germain', 'Rue de Rivoli'])}, {np.random.choice(['Paris', 'Lyon', 'Marseille'])}"
    elif country == 'DE':
        b_name = f"{np.random.choice(['Muller', 'Schmidt', 'Schneider', 'Weber'])} {np.random.choice(['Technik', 'Handel', 'Industrie'])} {np.random.choice(['GmbH', 'AG', 'KG'])}"
        b_addr = f"{np.random.choice(['Hauptstrasse', 'Bahnhofstrasse', 'Berliner Strasse'])} {np.random.randint(1, 150)}, {np.random.choice(['Berlin', 'Munchen', 'Hamburg'])}"
    elif country == 'IN':
        b_name = f"{np.random.choice(['Tata', 'Reliance', 'Infosys', 'Wipro', 'Mahindra'])} {np.random.choice(['Services', 'Exports', 'Digital', 'Infra'])} {np.random.choice(['Ltd', 'Pvt Ltd', 'Limited'])}"
        b_addr = f"{np.random.randint(1, 100)}, {np.random.choice(['MG Road', 'Inner Ring Rd', 'GC Avenue', 'NH-44'])}, {np.random.choice(['Bengaluru', 'Mumbai', 'Delhi', 'Hyderabad'])}"
    else:
        b_name = f"{np.random.choice(company_prefixes)} {np.random.choice(company_types)}"
        b_addr = f"{np.random.randint(10, 999)} {np.random.choice(['Main', 'Oak', 'Washington', 'Market', 'Broadway'])} {np.random.choice(street_types)}, Suite {np.random.randint(100, 900)}, {np.random.choice(['New York', 'London', 'Toronto', 'Sydney'])}"
    
    # Introduce occasional null address in master (rare)
    if i % 70 == 0:
        b_addr = None

    s1_records.append({
        'entity_id': e_id,
        'business_name': b_name,
        'business_address': b_addr,
        'country': country
    })

df_s1 = pd.DataFrame(s1_records)

# Generate S2 and S3 with controlled noise patterns and ground truth mappings
gt_records = []
s2_records = []
s3_records = []

s2_count = 0
s3_count = 0

for idx, row in df_s1.iterrows():
    e_id = row['entity_id']
    b_name = row['business_name']
    b_addr = row['business_address']
    country = row['country']
    
    num_s2_matches = np.random.choice([0, 1, 2], p=[0.15, 0.75, 0.10])
    num_s3_matches = np.random.choice([0, 1, 2], p=[0.20, 0.70, 0.10])
    
    for m in range(num_s2_matches):
        s2_count += 1
        rec_id = f"S2_{s2_count:04d}"
        
        corrupt_type = np.random.choice(['exact', 'typo', 'abbreviation', 'missing_addr', 'case_change'], p=[0.3, 0.25, 0.25, 0.1, 0.1])
        mod_name = b_name
        mod_addr = b_addr
        
        if corrupt_type == 'typo' and isinstance(mod_name, str):
            if len(mod_name) > 5:
                pos = np.random.randint(2, len(mod_name) - 2)
                mod_name = mod_name[:pos] + mod_name[pos+1] + mod_name[pos] + mod_name[pos+2:]
        elif corrupt_type == 'abbreviation' and isinstance(mod_name, str):
            mod_name = mod_name.replace('Corporation', 'Corp').replace('Limited', 'Ltd').replace('Technologies', 'Tech').replace('Solutions', 'Soln')
            if isinstance(mod_addr, str):
                mod_addr = mod_addr.replace('Street', 'St.').replace('Avenue', 'Ave.').replace('Boulevard', 'Blvd.')
        elif corrupt_type == 'missing_addr':
            mod_addr = None
        elif corrupt_type == 'case_change' and isinstance(mod_name, str):
            mod_name = mod_name.lower()
            
        s2_records.append({
            'entity_id': rec_id,
            'business_name': mod_name,
            'business_address': mod_addr,
            'country': country
        })
        gt_records.append({
            's1_entity_id': e_id,
            'source_id': 'Source2',
            'target_entity_id': rec_id
        })
        
    for m in range(num_s3_matches):
        s3_count += 1
        rec_id = f"S3_{s3_count:04d}"
        
        corrupt_type = np.random.choice(['exact', 'word_reorder', 'typo', 'missing_name_part', 'accent_strip'], p=[0.25, 0.25, 0.25, 0.15, 0.10])
        mod_name = b_name
        mod_addr = b_addr
        
        if corrupt_type == 'word_reorder' and isinstance(mod_name, str):
            words = mod_name.split()
            if len(words) > 2:
                mod_name = " ".join([words[-1]] + words[:-1])
        elif corrupt_type == 'typo' and isinstance(mod_addr, str):
            if len(mod_addr) > 8:
                mod_addr = mod_addr.replace('Road', 'Rd').replace('0', 'O').replace('1', 'l')
        elif corrupt_type == 'missing_name_part' and isinstance(mod_name, str):
            words = mod_name.split()
            if len(words) > 1:
                mod_name = " ".join(words[:-1])
        elif corrupt_type == 'accent_strip':
            if isinstance(mod_name, str):
                mod_name = mod_name.replace('E', 'E').replace('e', 'e')
            if isinstance(mod_addr, str):
                mod_addr = mod_addr.replace('E', 'E').replace('e', 'e')
                
        s3_records.append({
            'entity_id': rec_id,
            'business_name': mod_name,
            'business_address': mod_addr,
            'country': country
        })
        gt_records.append({
            's1_entity_id': e_id,
            'source_id': 'Source3',
            'target_entity_id': rec_id
        })

# Add 50 unmapped/zero-match entities to S2 and S3 (external noise entities)
for u in range(1, 51):
    s2_count += 1
    s2_records.append({
        'entity_id': f"S2_{s2_count:04d}",
        'business_name': f"Unmapped S2 Enterprise {u}",
        'business_address': f"{u*5} Unknown Blvd, City_{u}",
        'country': np.random.choice(countries)
    })
    
    s3_count += 1
    s3_records.append({
        'entity_id': f"S3_{s3_count:04d}",
        'business_name': f"Unmapped S3 Global {u}",
        'business_address': f"{u*10} Remote Street, Town_{u}",
        'country': np.random.choice(countries)
    })

df_s1 = pd.DataFrame(s1_records)
df_s2 = pd.DataFrame(s2_records)
df_s3 = pd.DataFrame(s3_records)
df_gt = pd.DataFrame(gt_records)

# Save TSV files with sep="\t"
df_s1.to_csv('data/official/source1.tsv', sep='\t', index=False)
df_s2.to_csv('data/official/source2.tsv', sep='\t', index=False)
df_s3.to_csv('data/official/source3.tsv', sep='\t', index=False)
df_gt.to_csv('data/official/ground_truth.tsv', sep='\t', index=False)

print("Official challenge datasets generated successfully in data/official/")
print(f"S1 shape: {df_s1.shape}")
print(f"S2 shape: {df_s2.shape}")
print(f"S3 shape: {df_s3.shape}")
print(f"Ground Truth shape: {df_gt.shape}")
