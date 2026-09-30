from typing import Dict, Set, Tuple, Any, Optional
import pandas as pd


class CandidateEvaluator:
    """
    Evaluates Candidate Generation and Blocking quality against Ground Truth.
    """

    @staticmethod
    def evaluate(
        candidates_df: pd.DataFrame,
        ground_truth_df: pd.DataFrame,
        n_records_a: int,
        n_records_b: Optional[int] = None,
        col_a: str = "id_a",
        col_b: str = "id_b"
    ) -> Dict[str, Any]:
        """
        Computes Reduction Ratio, Pair Completeness (Recall), Pair Quality (Precision), and F1.

        Args:
            candidates_df: DataFrame containing candidate pairs [col_a, col_b].
            ground_truth_df: DataFrame containing ground truth pairs [col_a, col_b].
            n_records_a: Total count of records in dataset A.
            n_records_b: Total count of records in dataset B (None if deduplication).
            col_a: Column name for dataset A record IDs.
            col_b: Column name for dataset B record IDs.

        Returns:
            Dictionary of metrics and breakdown.
        """
        is_dedup = n_records_b is None

        # Calculate search space size
        if is_dedup:
            total_possible_pairs = (n_records_a * (n_records_a - 1)) // 2
        else:
            total_possible_pairs = n_records_a * n_records_b

        # Standardize pair tuple sets (id_a, id_b)
        candidate_set: Set[Tuple[str, str]] = set(
            zip(candidates_df[col_a].astype(str), candidates_df[col_b].astype(str))
        )
        ground_truth_set: Set[Tuple[str, str]] = set(
            zip(ground_truth_df[col_a].astype(str), ground_truth_df[col_b].astype(str))
        )

        n_candidates = len(candidate_set)
        n_ground_truth = len(ground_truth_set)

        # True Positives: Ground truth pairs captured in candidates
        tp_set = candidate_set.intersection(ground_truth_set)
        tp = len(tp_set)

        # False Negatives: Ground truth pairs missed by blocking
        fn_set = ground_truth_set - candidate_set
        fn = len(fn_set)

        # False Positives: Candidate pairs that are not true matches
        fp = n_candidates - tp

        # Metric calculations
        reduction_ratio = 1.0 - (n_candidates / total_possible_pairs) if total_possible_pairs > 0 else 0.0
        recall = tp / n_ground_truth if n_ground_truth > 0 else 0.0
        precision = tp / n_candidates if n_candidates > 0 else 0.0
        f1_score = (2 * recall * precision) / (recall + precision) if (recall + precision) > 0 else 0.0

        metrics = {
            "Total Search Space Pairs": total_possible_pairs,
            "Candidate Pairs Generated": n_candidates,
            "Total Ground Truth Matches": n_ground_truth,
            "True Positive Matches Captured": tp,
            "Missed Ground Truth Matches (FN)": fn,
            "Reduction Ratio (RR)": round(reduction_ratio, 6),
            "Pair Completeness / Recall (PC)": round(recall, 6),
            "Pair Quality / Precision (PQ)": round(precision, 6),
            "Candidate F1 Score": round(f1_score, 6)
        }

        return metrics, fn_set

    @staticmethod
    def print_report(metrics: Dict[str, Any]):
        """Prints formatted candidate generation metric evaluation report."""
        print("\n" + "=" * 60)
        print(" CANDIDATE GENERATION & BLOCKING EVALUATION REPORT ")
        print("=" * 60)
        for key, value in metrics.items():
            if isinstance(value, float):
                print(f"  {key:<35}: {value:.4%}" if "Ratio" in key or "Recall" in key or "Precision" in key or "Score" in key else f"  {key:<35}: {value:.6f}")
            else:
                print(f"  {key:<35}: {value:,}")
        print("=" * 60 + "\n")
