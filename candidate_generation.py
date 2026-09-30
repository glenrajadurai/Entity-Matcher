from typing import List, Dict, Tuple, Set, Union, Optional
import pandas as pd
from collections import defaultdict
from blocking import BaseBlocker


class CandidateGenerator:
    """
    Generates candidate pair comparisons between Dataset A and Dataset B
    (or within Dataset A for deduplication) using specified blocking rules.
    """

    def __init__(
        self,
        blockers: Union[BaseBlocker, List[BaseBlocker]],
        id_col: str = "id",
        max_block_size: Optional[int] = 500
    ):
        """
        Args:
            blockers: A single blocker instance or list of blockers for multi-pass blocking.
            id_col: Column name representing unique record IDs.
            max_block_size: Maximum allowed records per block key (caps combinatorial explosion).
        """
        if isinstance(blockers, BaseBlocker):
            self.blockers = [blockers]
        else:
            self.blockers = blockers

        self.id_col = id_col
        self.max_block_size = max_block_size

    def generate_candidate_pairs(
        self,
        df_a: pd.DataFrame,
        df_b: Optional[pd.DataFrame] = None
    ) -> pd.DataFrame:
        """
        Generates unique candidate pairs (id_a, id_b) across all blocking passes.

        Args:
            df_a: First DataFrame.
            df_b: Optional second DataFrame. If None, performs intra-dataset deduplication on df_a.

        Returns:
            pd.DataFrame with columns ['id_a', 'id_b', 'block_key', 'pass_name']
        """
        is_dedup = df_b is None
        if is_dedup:
            df_b = df_a

        candidate_pairs: Set[Tuple[str, str]] = set()
        pair_details: List[Dict[str, str]] = []

        records_a = df_a.to_dict(orient="records")
        records_b = df_b.to_dict(orient="records")

        for pass_idx, blocker in enumerate(self.blockers):
            # Index records by blocking key
            blocks_a = defaultdict(list)
            blocks_b = defaultdict(list)

            for rec in records_a:
                key = blocker.get_key(rec)
                if key:  # Ignore empty blocking keys
                    blocks_a[key].append(str(rec[self.id_col]))

            if not is_dedup:
                for rec in records_b:
                    key = blocker.get_key(rec)
                    if key:
                        blocks_b[key].append(str(rec[self.id_col]))
            else:
                blocks_b = blocks_a

            # Intersect keys present in both datasets
            common_keys = set(blocks_a.keys()).intersection(set(blocks_b.keys()))

            pass_pairs_count = 0
            for key in common_keys:
                list_a = blocks_a[key]
                list_b = blocks_b[key]

                # Block size capping
                if self.max_block_size and (len(list_a) > self.max_block_size or len(list_b) > self.max_block_size):
                    continue

                if is_dedup:
                    # Intra-dataset deduplication: unique pairs id_a < id_b
                    for i in range(len(list_a)):
                        for j in range(i + 1, len(list_a)):
                            id_1, id_2 = list_a[i], list_a[j]
                            if id_1 > id_2:
                                id_1, id_2 = id_2, id_1
                            pair = (id_1, id_2)
                            if pair not in candidate_pairs:
                                candidate_pairs.add(pair)
                                pair_details.append({
                                    "id_a": id_1,
                                    "id_b": id_2,
                                    "block_key": key,
                                    "blocker": blocker.name
                                })
                                pass_pairs_count += 1
                else:
                    # Cross-dataset matching
                    for id_1 in list_a:
                        for id_2 in list_b:
                            pair = (id_1, id_2)
                            if pair not in candidate_pairs:
                                candidate_pairs.add(pair)
                                pair_details.append({
                                    "id_a": id_1,
                                    "id_b": id_2,
                                    "block_key": key,
                                    "blocker": blocker.name
                                })
                                pass_pairs_count += 1

            print(f"[Candidate Generator] Pass {pass_idx + 1} ({blocker.name}): "
                  f"{len(common_keys)} blocks, {pass_pairs_count} new candidate pairs added.")

        candidates_df = pd.DataFrame(pair_details)
        print(f"[Candidate Generator] Total Unique Candidate Pairs: {len(candidates_df)}")
        return candidates_df
