import re
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np


def levenshtein_distance(s1: str, s2: str) -> int:
    """Computes exact Levenshtein edit distance between two strings."""
    if s1 == s2:
        return 0
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)

    v0 = list(range(len(s2) + 1))
    v1 = [0] * (len(s2) + 1)

    for i in range(len(s1)):
        v1[0] = i + 1
        for j in range(len(s2)):
            cost = 0 if s1[i] == s2[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        v0 = list(v1)

    return v1[len(s2)]


def levenshtein_ratio(s1: str, s2: str) -> float:
    """Computes normalized Levenshtein similarity ratio between 0.0 and 1.0."""
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    s1, s2 = s1.lower().strip(), s2.lower().strip()
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0
    dist = levenshtein_distance(s1, s2)
    return max(0.0, 1.0 - dist / max_len)


def jaro_winkler_similarity(s1: str, s2: str, p: float = 0.1) -> float:
    """Computes Jaro-Winkler similarity between two strings."""
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0

    s1, s2 = s1.lower().strip(), s2.lower().strip()
    if s1 == s2:
        return 1.0

    len1, len2 = len(s1), len(s2)
    max_dist = max(len1, len2) // 2 - 1
    if max_dist < 0:
        max_dist = 0

    s1_matches = [False] * len1
    s2_matches = [False] * len2

    matches = 0
    transpositions = 0

    for i in range(len1):
        start = max(0, i - max_dist)
        end = min(i + max_dist + 1, len2)
        for j in range(start, end):
            if s2_matches[j]:
                continue
            if s1[i] != s2[j]:
                continue
            s1_matches[i] = True
            s2_matches[j] = True
            matches += 1
            break

    if matches == 0:
        return 0.0

    k = 0
    for i in range(len1):
        if not s1_matches[i]:
            continue
        while not s2_matches[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1

    jaro = (matches / len1 + matches / len2 + (matches - transpositions / 2.0) / matches) / 3.0

    prefix = 0
    for i in range(min(4, len1, len2)):
        if s1[i] == s2[i]:
            prefix += 1
        else:
            break

    return jaro + prefix * p * (1.0 - jaro)


def char_ngram_cosine_similarity(s1: str, s2: str, n_range=(2, 3)) -> float:
    """Computes character n-gram cosine similarity without external dependencies."""
    if not s1 or not s2:
        return 0.0
    s1_clean, s2_clean = s1.lower().strip(), s2.lower().strip()
    if s1_clean == s2_clean:
        return 1.0

    def get_ngrams(text):
        counts = {}
        for n in range(n_range[0], n_range[1] + 1):
            for i in range(len(text) - n + 1):
                gram = text[i:i + n]
                counts[gram] = counts.get(gram, 0) + 1
        return counts

    c1 = get_ngrams(s1_clean)
    c2 = get_ngrams(s2_clean)

    common = set(c1.keys()) & set(c2.keys())
    if not common:
        return 0.0

    dot = sum(c1[g] * c2[g] for g in common)
    norm1 = sum(v ** 2 for v in c1.values()) ** 0.5
    norm2 = sum(v ** 2 for v in c2.values()) ** 0.5

    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


class FeatureExtractor:
    """
    Extracts numerical feature vectors for candidate pairs of records.
    """

    def __init__(self, text_fields: List[str] = None):
        self.text_fields = text_fields or ["first_name", "last_name", "city", "email"]

    def extract_features(
        self,
        candidate_pairs: pd.DataFrame,
        df_a: pd.DataFrame,
        df_b: pd.DataFrame,
        id_col: str = "id"
    ) -> pd.DataFrame:
        """
        Calculates similarity features for each pair in candidate_pairs.

        Args:
            candidate_pairs: DataFrame containing ['id_a', 'id_b'].
            df_a: DataFrame of records A.
            df_b: DataFrame of records B.
            id_col: Unique identifier column name.

        Returns:
            DataFrame containing pair IDs and computed feature columns.
        """
        if candidate_pairs.empty:
            return pd.DataFrame()

        # Map records by ID for fast lookup
        map_a = df_a.set_index(id_col).to_dict(orient="index")
        map_b = df_b.set_index(id_col).to_dict(orient="index")

        feature_rows = []

        for _, row in candidate_pairs.iterrows():
            id_a, id_b = str(row["id_a"]), str(row["id_b"])
            rec_a = map_a.get(id_a, {})
            rec_b = map_b.get(id_b, {})

            feat = {"id_a": id_a, "id_b": id_b}

            # Field-level similarity features
            for field in ["first_name", "last_name", "email", "city"]:
                v1 = str(rec_a.get(field, "") or "")
                v2 = str(rec_b.get(field, "") or "")
                feat[f"{field}_lev"] = levenshtein_ratio(v1, v2)
                feat[f"{field}_jw"] = jaro_winkler_similarity(v1, v2)
                feat[f"{field}_exact"] = 1.0 if v1 and v1.lower() == v2.lower() else 0.0

            # Special categorical/numeric features
            fn_a, fn_b = str(rec_a.get("first_name", "")), str(rec_b.get("first_name", ""))
            ln_a, ln_b = str(rec_a.get("last_name", "")), str(rec_b.get("last_name", ""))

            feat["initial_match"] = 1.0 if fn_a and fn_b and fn_a[0].lower() == fn_b[0].lower() else 0.0
            feat["name_swapped"] = 1.0 if (fn_a.lower() == ln_b.lower() and ln_a.lower() == fn_b.lower() and fn_a) else 0.0

            # Zip code exact match
            zip_a, zip_b = str(rec_a.get("zip_code", "")), str(rec_b.get("zip_code", ""))
            feat["zip_exact"] = 1.0 if zip_a and zip_a == zip_b else 0.0

            # DOB exact match and year match
            dob_a, dob_b = str(rec_a.get("dob", "")), str(rec_b.get("dob", ""))
            feat["dob_exact"] = 1.0 if dob_a and dob_a == dob_b else 0.0
            year_a = dob_a[:4] if len(dob_a) >= 4 else ""
            year_b = dob_b[:4] if len(dob_b) >= 4 else ""
            feat["dob_year_match"] = 1.0 if year_a and year_a == year_b else 0.0

            # Overall record text similarity
            str_a = " ".join([str(rec_a.get(f, "")) for f in self.text_fields if rec_a.get(f)])
            str_b = " ".join([str(rec_b.get(f, "")) for f in self.text_fields if rec_b.get(f)])
            feat["full_text_ngram_cos"] = char_ngram_cosine_similarity(str_a, str_b)

            feature_rows.append(feat)

        features_df = pd.DataFrame(feature_rows)
        print(f"[Feature Extractor] Extracted {len(features_df.columns) - 2} features for {len(features_df)} candidate pairs.")
        return features_df
