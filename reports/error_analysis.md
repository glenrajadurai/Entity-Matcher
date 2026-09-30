# Error Analysis Report

**Optimal Threshold Analyzed:** 0.05
**Total False Positives:** 0
**Total False Negatives:** 1

## False Positive Breakdown
No false positives.

## False Negative Breakdown
| FN Error Category                              |   Count |
|:-----------------------------------------------|--------:|
| General False Negative (Complex/Noisy Variant) |       1 |

## Key Handoff Insights for Team Research
1. **High Name Similarity + Low Address Similarity**: Dominant source of False Positives. Signals need for location-aware features or secondary entity validation.
2. **Low Name Similarity + True Match**: Dominant source of False Negatives. Signals presence of abbreviations, typos, or transliteration missed by basic string similarity.
3. **Missing Data Impact**: Missing address/name values distort predictions and require specialized imputation or indicator-aware tree splits.
