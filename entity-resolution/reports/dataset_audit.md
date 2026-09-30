# Stage 1: Official Dataset Audit Report

## 1. Executive Summary & File Inventory

This dataset audit provides a quantitative analysis of the official challenge dataset for Business Entity Resolution (ER). The dataset consists of three tabular source files (`source1.tsv`, `source2.tsv`, `source3.tsv`) and one ground-truth mapping file (`ground_truth.tsv`), formatted as tab-separated values (`sep="\t"`).

### Official File Inventory & Dataset Dimensions

| File Name | Role / Description | Row Count | Column Count | Tab-Separated (`sep="\t"`) |
| :--- | :--- | :--- | :--- | :--- |
| `data/official/source1.tsv` | Master / Reference Entities (S1) | 500 | 4 | Yes |
| `data/official/source2.tsv` | External Records Source 2 (S2) | 540 | 4 | Yes |
| `data/official/source3.tsv` | External Records Source 3 (S3) | 506 | 4 | Yes |
| `data/official/ground_truth.tsv` | Ground-Truth Pairings (S1 to S2/S3) | 946 | 3 | Yes |

### Canonical Column Schema

All entity record files (`source1.tsv`, `source2.tsv`, `source3.tsv`) strictly follow the 4-column canonical schema:
1. `entity_id`: Unique identifier string per record (e.g., `S1_0001`, `S2_0001`, `S3_0001`)
2. `business_name`: Text string representing the organization name
3. `business_address`: Text string representing physical location/address
4. `country`: ISO 3166-1 alpha-2 country code string (e.g., `US`, `IN`, `FR`, `DE`)

---

## 2. Field-Level Completeness & Missing Value Analysis

Missing value audit across all three sources demonstrates varying completeness, particularly for `business_address` in external sources:

| Field Name | Source 1 (Master) Missing | Source 2 Missing | Source 3 Missing | Overall Completeness % |
| :--- | :--- | :--- | :--- | :--- |
| `entity_id` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 100.0% |
| `business_name` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 100.0% |
| `business_address` | 7 (1.4%) | 59 (10.9%) | 7 (1.4%) | 95.3% |
| `country` | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 100.0% |

> [!NOTE]
> `Source 2` exhibits a high missing address rate (10.9%), requiring entity resolution models to handle missing feature imputation or text similarity when only business names are present.

---

## 3. Geographical & Country Distribution

The dataset represents an international business entity domain covering 8 distinct jurisdictions, with high concentration in the US, India, and France.

| Country Code | Country Name | Source 1 Count (%) | Source 2 Count (%) | Source 3 Count (%) | Combined Total |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **US** | United States | 133 (26.6%) | 135 (25.0%) | 126 (24.9%) | 394 |
| **IN** | India | 119 (23.8%) | 119 (22.0%) | 116 (22.9%) | 354 |
| **FR** | France | 75 (15.0%) | 86 (15.9%) | 75 (14.8%) | 236 |
| **GB** | United Kingdom | 52 (10.4%) | 52 (9.6%) | 55 (10.9%) | 159 |
| **DE** | Germany | 50 (10.0%) | 53 (9.8%) | 43 (8.5%) | 146 |
| **CA** | Canada | 26 (5.2%) | 31 (5.7%) | 36 (7.1%) | 93 |
| **AU** | Australia | 26 (5.2%) | 36 (6.7%) | 30 (5.9%) | 92 |
| **JP** | Japan | 19 (3.8%) | 28 (5.2%) | 25 (4.9%) | 72 |

---

## 4. Name & Address Duplication & Overlap

Audit of duplicate names and addresses reveals recurring synthetic entity templates (e.g. repeated company prefixes like *Apex Solutions*, *Tata Services*, *Société Dufour*):

| Feature & Metric | Source 1 (Master) | Source 2 | Source 3 |
| :--- | :--- | :--- | :--- |
| **Exact Duplicate Names** | 229 | 127 | 168 |
| **Normalized Duplicate Names** (lowercase, no punctuation) | 229 | 157 | 168 |
| **Exact Duplicate Addresses** | 6 | 42 | 43 |
| **Normalized Duplicate Addresses** | 6 | 42 | 43 |

> [!WARNING]
> Duplicate business names across distinct master entities mean that **business_name alone is insufficient** for entity resolution; address and country context are required for disambiguation.

---

## 5. Length Distributions

Character length and word count statistics across names and addresses:

### Business Name Length Statistics

| Source | Min Chars | Max Chars | Mean Chars | Median Chars | Min Words | Max Words | Mean Words | Median Words |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Source 1** | 9 | 26 | 17.93 | 18.0 | 2 | 4 | 2.56 | 2.0 |
| **Source 2** | 9 | 26 | 18.53 | 19.0 | 2 | 4 | 2.70 | 3.0 |
| **Source 3** | 4 | 26 | 17.12 | 18.0 | 1 | 4 | 2.55 | 2.0 |

### Business Address Length Statistics

| Source | Min Chars | Max Chars | Mean Chars | Median Chars | Min Words | Max Words | Mean Words | Median Words |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Source 1** | 16 | 45 | 30.76 | 32.0 | 3 | 7 | 5.24 | 6.0 |
| **Source 2** | 16 | 45 | 30.06 | 30.0 | 3 | 7 | 5.11 | 5.0 |
| **Source 3** | 16 | 45 | 30.45 | 31.0 | 3 | 7 | 5.15 | 6.0 |

---

## 6. Ground-Truth Match-Count Distribution

The ground-truth file (`ground_truth.tsv`) links master entities (`s1_entity_id`) to external records (`target_entity_id`) across `Source2` and `Source3`.

### S1 Entity Ground-Truth Match Distribution

| Match Count per S1 Entity | S1-to-S2 Count (%) | S1-to-S3 Count (%) | Combined S1-to-(S2+S3) Count (%) |
| :--- | :--- | :--- | :--- |
| **0 Matches (Zero-match entities)** | 66 (13.2%) | 96 (19.2%) | 14 (2.8%) |
| **1 Match (Unique 1-to-1)** | 378 (75.6%) | 352 (70.4%) | 116 (23.2%) |
| **2 Matches (1-to-many)** | 56 (11.2%) | 52 (10.4%) | 284 (56.8%) |
| **3 Matches** | N/A | N/A | 82 (16.4%) |
| **4 Matches** | N/A | N/A | 4 (0.8%) |

### External Unmapped Records (Hard Negatives in External Sources)
- **Source 2 Unmapped External Records**: 50 records (out of 540) have zero match in S1 master entities.
- **Source 3 Unmapped External Records**: 50 records (out of 506) have zero match in S1 master entities.

---

## 7. Observed Entity Resolution Noise & Failure Patterns

Based on the empirical audit, four major difficulty patterns dominate the official challenge dataset:

1. **High Name Ambiguity / Homonymy**: 229 duplicate business names exist in S1 for different addresses, meaning models relying solely on name similarity will produce high false positive rates.
2. **Missing Address Context**: 10.9% of S2 records lack street addresses completely.
3. **Legal Suffix & Street Abbreviation Variations**: Differences between *Corporation* vs *Corp*, *Limited* vs *Ltd*, *Street* vs *St.*, *Road* vs *Rd*.
4. **Word Order Perturbations**: Token swaps in company names and address strings (e.g. *Services Tata* vs *Tata Services*).
