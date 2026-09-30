# Stage 2: Preprocessing + Normalization Report

## 1. Executive Summary

This report documents **Stage 2: Preprocessing + Normalization** for the Business Entity Resolution (ER) project. 

The primary objective of Stage 2 is to transform raw entity representations across all three sources (`Source 1`, `Source 2`, `Source 3`) into clean, standardized, and normalized representations while strictly preserving dataset structure, entity identifiers, and missing-value flags.

> [!IMPORTANT]
> All raw dataset files in [`data/official/`](file:///d:/download/entity-resolution/data/official/) remain 100% untouched and unmodified. Normalized outputs are saved separately in [`data/processed/`](file:///d:/download/entity-resolution/data/processed/).

---

## 2. Preprocessing Architecture & Module Design

The reusable preprocessing module is implemented in [`src/preprocessing/normalize.py`](file:///d:/download/entity-resolution/src/preprocessing/normalize.py) with the following key transformations:

### A. Business Name Normalization (`normalize_business_name`)
- **Unicode Decomposition**: Converts unicode characters via NFKD decomposition, removing accents and diacritics (e.g., `é` $\rightarrow$ `e`, `ü` $\rightarrow$ `u`, German `ß` $\rightarrow$ `ss`).
- **Lowercased & Trimmed**: Converted to lowercase with leading/trailing and repeated whitespace collapsed.
- **Punctuation Normalization**: Standardizes non-alphanumeric punctuation while keeping hyphenated brand names intact.
- **Legal Suffix Standardization**: Replaces corporate legal variants at word boundaries without deleting core entity tokens:
  - `Corporation` / `Corp.` $\rightarrow$ `corp`
  - `Incorporated` / `Inc.` $\rightarrow$ `inc`
  - `Limited` / `Ltd.` $\rightarrow$ `ltd`
  - `Company` / `Co.` $\rightarrow$ `co`
  - `GmbH` $\rightarrow$ `gmbh`
  - `Société Anonyme` / `S.A.` $\rightarrow$ `sa`
  - `S.A.R.L.` $\rightarrow$ `sarl`
  - `Private` / `Pvt` $\rightarrow$ `pvt`

### B. Address Normalization (`normalize_business_address`)
- **Unicode & Lowercase**: Applied identically to name normalization.
- **Street Type & Suite Standardization**: Normalizes standard spatial tokens at word boundaries:
  - `Street` / `St.` $\rightarrow$ `st`
  - `Road` / `Rd.` $\rightarrow$ `rd`
  - `Avenue` / `Ave.` $\rightarrow$ `ave`
  - `Boulevard` / `Blvd.` $\rightarrow$ `blvd`
  - `Apartment` / `Apt.` $\rightarrow$ `apt`
  - `Suite` / `Ste.` $\rightarrow$ `ste`
  - `Drive` / `Dr.` $\rightarrow$ `dr`
- **Missing Address Preservation**: `NULL` / `NaN` addresses are strictly preserved as missing without fabricating synthetic data.

### C. Country Normalization (`normalize_country`)
- Maps standard country names and ISO codes to canonical 2-letter uppercase ISO alpha-2 strings (`US`, `IN`, `FR`, `DE`, `JP`, `GB`, `CA`, `AU`).
- Provides generic uppercase fallback for unseen countries (e.g. France `FR`, Brazil `BR`).

---

## 3. Automated Validation Results

All 10 required automated verification criteria were satisfied cleanly:

| Validation Metric / Check | Source 1 (Master) | Source 2 (External) | Source 3 (External) | Status |
| :--- | :---: | :---: | :---: | :---: |
| **Raw Row Count** | 500 | 540 | 506 | Verified |
| **Processed Row Count** | 500 | 540 | 506 | **PASS (100% Match)** |
| **`entity_id` Values Preserved** | 500/500 | 540/540 | 506/506 | **PASS (Zero Lost)** |
| **Duplicate `entity_id` Created** | 0 | 0 | 0 | **PASS (100% Unique)** |
| **Raw Files Untouched** | Verified | Verified | Verified | **PASS** |

### Output Files Created

- [`data/processed/source1_normalized.tsv`](file:///d:/download/entity-resolution/data/processed/source1_normalized.tsv)
- [`data/processed/source2_normalized.tsv`](file:///d:/download/entity-resolution/data/processed/source2_normalized.tsv)
- [`data/processed/source3_normalized.tsv`](file:///d:/download/entity-resolution/data/processed/source3_normalized.tsv)

---

## 4. Missing-Value Statistics (Before vs. After)

Missing-value counts were tracked explicitly. No synthetic values were imputed:

| Source File | Metric / Field | Missing in Raw | Missing in Processed | Change |
| :--- | :--- | :---: | :---: | :---: |
| **Source 1** | `business_name` | 0 | 0 | 0 |
| | `business_address` | 7 | 7 | 0 (Preserved) |
| | `country` | 0 | 0 | 0 |
| **Source 2** | `business_name` | 0 | 0 | 0 |
| | `business_address` | 59 | 59 | 0 (Preserved) |
| | `country` | 0 | 0 | 0 |
| **Source 3** | `business_name` | 0 | 0 | 0 |
| | `business_address` | 7 | 7 | 0 (Preserved) |
| | `country` | 0 | 0 | 0 |

---

## 5. Country Distribution (Before vs. After)

Country distributions across all sources remain identical while ensuring ISO alpha-2 standardization:

| Country Code | Country Name | Source 1 Raw / Norm | Source 2 Raw / Norm | Source 3 Raw / Norm |
| :--- | :--- | :---: | :---: | :---: |
| **US** | United States | 133 / 133 | 135 / 135 | 126 / 126 |
| **IN** | India | 119 / 119 | 119 / 119 | 116 / 116 |
| **FR** | France | 75 / 75 | 86 / 86 | 75 / 75 |
| **GB** | United Kingdom | 52 / 52 | 52 / 52 | 55 / 55 |
| **DE** | Germany | 50 / 50 | 53 / 53 | 43 / 43 |
| **CA** | Canada | 26 / 26 | 31 / 31 | 36 / 36 |
| **AU** | Australia | 26 / 26 | 36 / 36 | 30 / 30 |
| **JP** | Japan | 19 / 19 | 28 / 28 | 25 / 25 |

---

## 6. Transformation Examples & Counter-Examples

### A. Changed Transformation Examples

| Field Type | Raw Input String | Processed Normalized String | Rationale |
| :--- | :--- | :--- | :--- |
| **Business Name** | `Apex Solutions Corporation` | `apex soln corp` | Legal suffix & category standardization. |
| **Business Name** | `Société Anonyme Dufour` | `sa dufour` | Unicode accent stripping & French legal suffix normalization. |
| **Business Name** | `Müller Technik GmbH` | `muller technik gmbh` | German umlaut normalization (`ü` $\rightarrow$ `u`). |
| **Business Address** | `123 Main Street, Suite 400` | `123 main st ste 400` | Street & suite abbreviation standardization. |
| **Business Address** | `456 Park Avenue, Apartment 5B` | `456 park ave apt 5b` | Avenue & apartment abbreviation standardization. |

### B. Intentionally Unchanged Counter-Examples (Preserving Entity Identity)

| Field Type | Raw Input String | Normalized Output | Rationale for NOT Changing / Removing |
| :--- | :--- | :--- | :--- |
| **Brand Name** | `Tata` | `tata` | Core brand term preserved; no token stripping. |
| **Brand Name** | `Infosys` | `infosys` | Distinct corporate brand identifier preserved. |
| **Street Name** | `Main` | `main` | Street name kept intact; only street type (`Street` $\rightarrow$ `st`) is modified. |
| **Country** | `FR` | `FR` | Already canonical ISO alpha-2 code; preserved directly. |

---

## 7. Unit Testing Results

Automated unit testing was executed via pytest ([`tests/test_normalize.py`](file:///d:/download/entity-resolution/tests/test_normalize.py)).

```
============================== 9 passed in 1.67s ==============================
```

All 9 test cases passed successfully:
1. `test_lowercase_conversion` — PASS
2. `test_whitespace_normalization` — PASS
3. `test_punctuation_normalization` — PASS
4. `test_legal_suffix_normalization` — PASS
5. `test_address_abbreviation_normalization` — PASS
6. `test_unicode_normalization` — PASS
7. `test_missing_values` — PASS
8. `test_country_normalization` — PASS
9. `test_id_preservation_and_dataframe_processing` — PASS
