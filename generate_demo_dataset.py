import pandas as pd
import numpy as np
import os
import argparse

def generate_demo_entity_resolution_dataset(
    output_path: str = "demo_entity_resolution_output.csv",
    n_master: int = 150,
    n_pairs: int = 1000,
    seed: int = 42
) -> pd.DataFrame:
    """
    Generates a realistic demo dataset simulating Source 1 (Master Entities),
    Source 2 & Source 3 (Noisy External Records), pairwise similarity features,
    ground truth match labels, model match probabilities, and entity resolution predictions.
    """
    np.random.seed(seed)
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    
    company_prefixes = ["Apex", "Global", "Nexus", "Vertex", "Horizon", "Pinnacle", "Summit", "Quantum", "Beacon", "Vanguard"]
    company_suffixes = ["Technologies", "Solutions", "Logistics", "Enterprises", "Industries", "Health", "Capital", "Group", "Services", "Retail"]
    cities = ["New York", "London", "Tokyo", "Berlin", "Singapore", "Sydney", "Mumbai", "Toronto", "Paris", "Dubai"]
    countries = ["US", "GB", "JP", "DE", "SG", "AU", "IN", "CA", "FR", "AE"]
    
    # 1. Master entities S1
    master_entities = []
    for i in range(1, n_master + 1):
        s1_id = f"S1_{i:04d}"
        prefix = np.random.choice(company_prefixes)
        suffix = np.random.choice(company_suffixes)
        name = f"{prefix} {suffix}"
        city_idx = np.random.randint(0, len(cities))
        city = cities[city_idx]
        country = countries[city_idx]
        zip_code = f"{np.random.randint(10000, 99999)}"
        master_entities.append({
            "s1_entity_id": s1_id,
            "master_company_name": name,
            "master_city": city,
            "master_country": country,
            "master_zip": zip_code
        })
    
    master_df = pd.DataFrame(master_entities)
    
    # 2. Pairwise candidate pairs
    records = []
    for i in range(1, n_pairs + 1):
        m_row = master_df.sample(1).iloc[0]
        s1_id = m_row["s1_entity_id"]
        source = np.random.choice(["Source 2 (Noisy DB A)", "Source 3 (Noisy DB B)"])
        cand_id = f"EXT_{source[7:8]}_{i:05d}"
        
        is_true_match = np.random.choice([1, 0], p=[0.25, 0.75])
        
        if is_true_match:
            # High similarity signals with realistic noise
            name_sim = np.random.beta(8, 2)
            addr_sim = np.random.beta(7, 2)
            country_match = np.random.choice([1, 0], p=[0.96, 0.04])
            missing_name = np.random.choice([0, 1], p=[0.97, 0.03])
            missing_addr = np.random.choice([0, 1], p=[0.90, 0.10])
            cand_name = m_row["master_company_name"] if np.random.rand() > 0.3 else m_row["master_company_name"] + " Inc"
            cand_city = m_row["master_city"]
            cand_country = m_row["master_country"]
        else:
            # Lower similarity signals (Hard negatives or random pairs)
            is_hard_neg = np.random.rand() > 0.7
            if is_hard_neg:
                # Same name, different location
                name_sim = np.random.beta(7, 2)
                addr_sim = np.random.beta(2, 6)
                cand_name = m_row["master_company_name"]
                cand_city = np.random.choice(cities)
                cand_country = np.random.choice(countries)
            else:
                name_sim = np.random.beta(2, 5)
                addr_sim = np.random.beta(2, 5)
                cand_name = f"{np.random.choice(company_prefixes)} {np.random.choice(company_suffixes)}"
                cand_city = np.random.choice(cities)
                cand_country = np.random.choice(countries)
                
            country_match = 1 if cand_country == m_row["master_country"] else 0
            missing_name = np.random.choice([0, 1], p=[0.95, 0.05])
            missing_addr = np.random.choice([0, 1], p=[0.85, 0.15])
            
        name_token_overlap = name_sim * np.random.uniform(0.85, 1.0)
        addr_token_overlap = addr_sim * np.random.uniform(0.80, 1.0)
        
        # Model match probability (LightGBM simulated predictions)
        logit = (name_sim * 3.5) + (addr_sim * 2.5) + (country_match * 1.0) - (missing_name * 1.5) - 3.2
        match_prob = 1.0 / (1.0 + np.exp(-logit))
        
        # Decision threshold = 0.05
        is_pred_match = 1 if match_prob >= 0.05 else 0
        
        records.append({
            "s1_entity_id": s1_id,
            "candidate_entity_id": cand_id,
            "source": source,
            "master_company_name": m_row["master_company_name"],
            "candidate_company_name": cand_name,
            "master_city": m_row["master_city"],
            "candidate_city": cand_city,
            "country": m_row["master_country"],
            "name_similarity": round(float(name_sim), 4),
            "address_similarity": round(float(addr_sim), 4),
            "country_match": int(country_match),
            "name_token_overlap": round(float(name_token_overlap), 4),
            "address_token_overlap": round(float(addr_token_overlap), 4),
            "missing_name": int(missing_name),
            "missing_address": int(missing_addr),
            "ground_truth_label": int(is_true_match),
            "model_match_probability": round(float(match_prob), 4),
            "optimal_threshold": 0.05,
            "predicted_linkage": "MATCH" if is_pred_match == 1 else "UNMATCHED"
        })
        
    df_result = pd.DataFrame(records)
    df_result.to_csv(output_path, index=False)
    print(f"[SUCCESS] Demo Entity Resolution Dataset successfully generated at: {output_path}")

    print(f"  - Total Candidate Pairs: {len(df_result)}")
    print(f"  - Total Ground Truth Matches: {df_result['ground_truth_label'].sum()}")
    print(f"  - Total Model Linkages (MATCH): {(df_result['predicted_linkage'] == 'MATCH').sum()}")
    return df_result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Demo Entity Resolution Dataset Output")
    parser.add_argument("--output", type=str, default="demo_entity_resolution_output.csv", help="Output CSV filepath")
    parser.add_argument("--pairs", type=int, default=1000, help="Number of candidate pairs to generate")
    args = parser.parse_args()
    
    generate_demo_entity_resolution_dataset(output_path=args.output, n_pairs=args.pairs)
