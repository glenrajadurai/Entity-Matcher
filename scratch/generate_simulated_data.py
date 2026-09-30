import numpy as np
import pandas as pd
import os

def generate_simulated_feature_table(output_path: str = "scratch/simulated_feature_table.csv", num_samples: int = 1000):
    """
    Generates a realistic simulated pairwise feature table to test the Member 3 pipeline end-to-end
    without modifying official datasets or hardcoding country constraints.
    """
    np.random.seed(42)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 100 unique s1 master entities
    s1_entities = [f"E1_{i:04d}" for i in range(1, 101)]
    s1_ids = np.random.choice(s1_entities, size=num_samples)
    candidate_ids = [f"E23_{i:06d}" for i in range(1, num_samples + 1)]
    sources = np.random.choice(["source2", "source3"], size=num_samples)
    
    # Labels (~20% positive matches)
    labels = np.random.choice([0, 1], size=num_samples, p=[0.8, 0.2])
    
    # Features correlated with match label
    name_sim = np.where(labels == 1, np.random.beta(8, 2, size=num_samples), np.random.beta(2, 5, size=num_samples))
    addr_sim = np.where(labels == 1, np.random.beta(7, 2, size=num_samples), np.random.beta(2, 6, size=num_samples))
    country_match = np.where(labels == 1, np.random.choice([1, 0], p=[0.95, 0.05], size=num_samples), np.random.choice([1, 0], p=[0.5, 0.5], size=num_samples))
    name_token_overlap = name_sim * np.random.uniform(0.8, 1.0, size=num_samples)
    addr_token_overlap = addr_sim * np.random.uniform(0.7, 1.0, size=num_samples)
    
    missing_name = np.random.choice([0, 1], p=[0.95, 0.05], size=num_samples)
    missing_addr = np.random.choice([0, 1], p=[0.85, 0.15], size=num_samples)
    
    df = pd.DataFrame({
        "s1_entity_id": s1_ids,
        "candidate_entity_id": candidate_ids,
        "source": sources,
        "name_similarity": np.round(name_sim, 4),
        "address_similarity": np.round(addr_sim, 4),
        "country_match": country_match,
        "name_token_overlap": np.round(name_token_overlap, 4),
        "address_token_overlap": np.round(addr_token_overlap, 4),
        "missing_name": missing_name,
        "missing_address": missing_addr,
        "label": labels
    })
    
    df.to_csv(output_path, index=False)
    print(f"Simulated feature table generated at: {output_path} ({len(df)} candidate pairs)")
    return output_path

if __name__ == "__main__":
    generate_simulated_feature_table()
