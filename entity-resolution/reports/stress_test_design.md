# Stage 1: Stress-Test Benchmark Dataset Design Report

## 1. Executive Summary & Research Rationale

The official challenge dataset provides an initial evaluation ground for Business Entity Resolution (ER). However, real-world entity resolution pipelines encounter severe corner cases, adversarial noisy text, homonyms, missing metadata, and cross-lingual script variations. 

To scientifically evaluate future ER model robustness without risking data leakage or overfitting to the challenge set, we design a **Separate Synthetic Stress-Test Benchmark**.

### Crucial Scientific Principles
1. **Model Independence**: Corruption rules and difficulty categories are defined entirely independently of any candidate model architecture (LightGBM, XGBoost, Transformers, Graph Neural Networks, or Heuristics).
2. **Strict Dataset Separation**: The stress-test benchmark will exist in `data/stress_test/` and will **NEVER** be mixed into training or validation splits.
3. **Exact Ground-Truth Preservation**: Every generated corrupted record traces back to its true master entity via explicit metadata and deterministic mapping IDs.
4. **Metadata Provenance**: Every generated record records the exact corruption category (A–P), severity parameters, and seed used in `corruption_metadata.tsv`.
5. **No Domain Overclaims**: Generated records represent synthetic benchmark entities designed for failure mode analysis, avoiding unverified real-world claims.

---

## 2. Proposed Directory & Metadata Schema

### Directory Structure

```
data/
├── official/
│   ├── source1.tsv
│   ├── source2.tsv
│   ├── source3.tsv
│   └── ground_truth.tsv
├── stress_test/
│   ├── master.tsv
│   ├── source2.tsv
│   ├── source3.tsv
│   ├── ground_truth.tsv
│   └── corruption_metadata.tsv
└── reports/
    ├── dataset_audit.md
    └── stress_test_design.md
```

### `corruption_metadata.tsv` Schema
- `record_id`: Unique identifier of corrupted external record (e.g., `ST_S2_0102`)
- `master_entity_id`: Ground-truth master ID in `master.tsv` (e.g., `ST_M_0045` or `NULL` for zero-match)
- `source_id`: Source identifier (`Source2` or `Source3`)
- `category_code`: Corruption category letter (`A` through `P`)
- `category_name`: Human-readable category label (e.g., `Simultaneous_Name_Address_Corruption`)
- `original_name`: Name before corruption
- `corrupted_name`: Name after corruption
- `original_address`: Address before corruption
- `corrupted_address`: Address after corruption
- `seed_used`: Fixed seed parameter (e.g., `42`)

---

## 3. Comprehensive Corruption Categories (A through P)

We establish 16 systematic corruption categories to stress-test every component of an ER pipeline (blocking, indexing, string matching, vector embedding, context fusion, and classification).

| Code | Category Name | Description & Noise Mechanism | Proposed Record Count | Target Failure Mode |
| :---: | :--- | :--- | :---: | :--- |
| **A** | **Exact / Near-Exact Matches** | Identical or whitespace-cleaned copy of master entity. | 100 | Baseline recall check; sanity check for exact matchers. |
| **B** | **Minor Spelling Typos** | Single/double character insertion, deletion, substitution, or adjacent transposition (Damerau-Levenshtein dist 1-2). | 100 | Tests fuzzy string similarity robustness (Jaro-Winkler, Levenshtein). |
| **C** | **Abbreviations** | Expansion/contraction of legal entities (*Corporation* $\leftrightarrow$ *Corp*, *Limited* $\leftrightarrow$ *Ltd*, *Société Anonyme* $\leftrightarrow$ *SA*) and street types (*Street* $\leftrightarrow$ *St*, *Avenue* $\leftrightarrow$ *Ave*). | 100 | Tests standardization & dictionary-based canonicalization. |
| **D** | **Word Reordering** | Permutation of token positions in business name (*Tata Consultancy Services* $\rightarrow$ *Services Consultancy Tata*). | 80 | Tests bag-of-words / token-set vs sequence-order sensitivity. |
| **E** | **Partial Business Names** | Truncation of secondary brand terms or qualifiers (*Acme Precision Logistics Solutions* $\rightarrow$ *Acme Precision*). | 80 | Tests token overlap thresholds and prefix matching. |
| **F** | **Partial Addresses** | Truncation of suite numbers, street numbers, or postal codes (*123 Main St, Suite 400, New York* $\rightarrow$ *Main St, New York*). | 80 | Tests soft-geocoding and street-level address matching. |
| **G** | **Missing Business Name Components** | Omission of primary brand word, retaining only general generic category word (*Apex Cybertech* $\rightarrow$ *Cybertech*). | 60 | Tests over-reliance on high-frequency generic terms. |
| **H** | **Missing Address Components** | Address set to `NULL` / empty string while name is intact. | 60 | Tests single-field fallback logic when address is absent. |
| **I** | **Simultaneous Name + Address Corruption** | Typos/Abbreviations in name AND partial/truncated address simultaneously. | 80 | Tests multi-attribute joint similarity scoring. |
| **J** | **Transliteration / Cross-Script Variation** | Diacritic stripping, accent removal (*Société Généralé* $\rightarrow$ *Societe Generale*), or romanization variants (*Müller* $\rightarrow$ *Mueller*). | 60 | Tests multilingual & character set normalization. |
| **K** | **Same Name, Different Address (Hard Negative)** | Identical business name paired with a completely different city/street address (Homonyms). | 80 | Prevents false positives caused by name-only matching. |
| **L** | **Similar Address, Different Business (Hard Negative)** | Identical building address paired with a completely different business name (Co-tenants / Office Parks). | 80 | Prevents false positives caused by address-only matching. |
| **M** | **Completely Unrelated Hard Negatives** | High TF-IDF word overlap but distinct real entities (*Quantum Logistics* vs *Quantum Pharmaceuticals* in different countries). | 60 | Tests discriminative vector embeddings and tf-idf weighting. |
| **N** | **Multiple Valid Matches (1-to-Many)** | 2 or 3 distinct corrupted records in S2/S3 mapping to a single S1 master entity. | 80 | Tests multi-match deduplication and cluster merging. |
| **O** | **Zero-Match Entities (Unmapped)** | External records created from synthetic templates that do not exist in Master S1. | 80 | Tests precision against out-of-KB noise entities. |
| **P** | **Unseen Country / International Domains** | Entities from countries not prevalent in primary training set (e.g. France FR, Japan JP, Brazil BR, Germany DE). | 60 | Tests cross-border domain generalization and country schema independence. |
| **TOTAL** | | | **1,240** | **Comprehensive stress-test suite** |

---

## 4. Positive and Hard-Negative Generation Strategy

### Ground Truth Integrity
- **Positives**: Categories A–J, N map directly to their corresponding `master_entity_id` in `master.tsv`. Ground truth pairs are explicitly recorded in `ground_truth.tsv`.
- **Hard Negatives**: Categories K, L, M represent difficult distractor pairs generated by pairing existing entity names with different entity addresses (and vice versa). They serve as negative evaluation candidates.
- **Zero-Match External Records**: Categories O, P have `master_entity_id = NULL` in metadata and no entry in `ground_truth.tsv`.

---

## 5. Prevention of Data Leakage & Research Validity

1. **Deterministic Random Generation**: All corruption scripts will use fixed random seeds (`seed=42`).
2. **Complete Separation**: `data/stress_test/` files will remain isolated from any future training code.
3. **No Model-Driven Data Synthesis**: Corruption rules use standard edit distances, string operations, and dictionary swaps—never synthetic outputs from candidate models.
4. **Global Country Support**: Rule templates apply generically across US, IN, FR, DE, JP, GB, CA, AU without hardcoding single-country assumptions.

---

## 6. Open Architecture Aspects (Undecided in Stage 1)

Per project guidelines, the following system decisions remain **open and undecided**:
- Candidate blocking / indexing algorithms (e.g., MinHash LSH, Q-gram blocking, TF-IDF nearest neighbors, vector ANN indexing)
- Feature extraction pipelines (e.g., Jaro-Winkler, Monge-Elkan, Soft-TFIDF, Sentence-Transformers)
- Final classification models (LightGBM, XGBoost, CatBoost, Logistic Regression, Fine-tuned Transformer)
- Clustering and graph-resolution threshold tuning

Stage 1 focuses strictly on **data audit and stress-test benchmark design**.
