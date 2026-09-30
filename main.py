import os
import argparse
import pandas as pd

from generate_data import generate_dummy_datasets
from blocking import ExactBlocker, SoundexBlocker, PrefixBlocker, YearBlocker, CompoundBlocker
from candidate_generation import CandidateGenerator
from features import FeatureExtractor
from recall import CandidateEvaluator
from ml.compare_models import run_model_comparison
from ml.error_analysis import analyze_model_errors


def run_candidate_generation_pipeline():
    print("\n==================================================")
    print(" STEP 1: RECORD LINKAGE & CANDIDATE GENERATION   ")
    print("==================================================\n")

    data_dir = "."
    if not (os.path.exists("dataset_a.csv") and os.path.exists("dataset_b.csv") and os.path.exists("ground_truth.csv")):
        print("[Pipeline] Generating dummy datasets...")
        df_a, df_b, df_gt = generate_dummy_datasets(output_dir=data_dir, n_a=500, n_b=400, seed=42)
    else:
        print("[Pipeline] Loading existing datasets...")
        df_a = pd.read_csv("dataset_a.csv")
        df_b = pd.read_csv("dataset_b.csv")
        df_gt = pd.read_csv("ground_truth.csv")

    print(f"Dataset A records: {len(df_a)}")
    print(f"Dataset B records: {len(df_b)}")
    print(f"Ground Truth pairs: {len(df_gt)}")

    print("\n[Pipeline] Configuring Multi-Pass Blocking rules...")
    blockers = [
        ExactBlocker("zip_code"),
        SoundexBlocker("last_name"),
        PrefixBlocker("first_name", n_chars=3),
        YearBlocker("dob"),
        CompoundBlocker([PrefixBlocker("last_name", n_chars=2), ExactBlocker("state")])
    ]

    print("\n[Pipeline] Generating Candidate Pairs...")
    generator = CandidateGenerator(blockers=blockers, id_col="id", max_block_size=500)
    candidates_df = generator.generate_candidate_pairs(df_a, df_b)

    print("\n[Pipeline] Evaluating Blocking & Recall Metrics...")
    metrics, fn_set = CandidateEvaluator.evaluate(
        candidates_df=candidates_df,
        ground_truth_df=df_gt,
        n_records_a=len(df_a),
        n_records_b=len(df_b)
    )
    CandidateEvaluator.print_report(metrics)

    print("\n[Pipeline] Extracting Similarity Features...")
    extractor = FeatureExtractor(text_fields=["first_name", "last_name", "city", "email"])
    features_df = extractor.extract_features(candidates_df, df_a, df_b)

    candidates_df.to_csv("candidate_pairs.csv", index=False)
    features_df.to_csv("extracted_features.csv", index=False)
    print("Candidate pairs saved to candidate_pairs.csv")
    print("Extracted features saved to extracted_features.csv")
    return "extracted_features.csv"


def run_ml_pipeline(data_path="extracted_features.csv", config_path="configs/model_config.yaml"):
    print("\n==================================================")
    print(" STEP 2: ML MODEL COMPARISON & EVALUATION        ")
    print("==================================================")

    if not os.path.exists(data_path):
        print(f"Data path {data_path} not found. Running candidate generation first...")
        data_path = run_candidate_generation_pipeline()

    print(f"\n1. Loading pairwise feature table from: {data_path}")
    print(f"2. Running model comparison & threshold tuning...")

    results = run_model_comparison(data_path=data_path, config_path=config_path)

    print("\n--------------------------------------------------")
    print("               MODEL COMPARISON TABLE             ")
    print("--------------------------------------------------")
    print(results["comparison_table"].to_string(index=False))

    winner_name = results["winner_name"]
    opt_threshold = results["winner_metadata"]["best_threshold"]

    print(f"\n>>> Selected Best Model: {winner_name} (Threshold: {opt_threshold:.2f})")

    print("\n3. Performing Error Analysis on Validation Set...")
    analyze_model_errors(
        val_df=results["val_df"],
        y_pred_proba=results["val_probs"],
        threshold=opt_threshold,
        feature_cols=results["feature_cols"],
        output_report_path="reports/error_analysis.md"
    )

    print("\n[SUCCESS] Pipeline Execution Complete!")
    print(f"  - Comparison Report saved to: reports/model_comparison.md")
    print(f"  - Error Analysis saved to: reports/error_analysis.md")
    print(f"  - Model Artifacts saved to: models/final/")


def main():
    parser = argparse.ArgumentParser(description="Entity Resolution End-to-End Pipeline")
    parser.add_argument("--mode", type=str, choices=["all", "linkage", "ml"], default="all",
                        help="Mode to run: 'all' (end-to-end), 'linkage' (candidate generation & features), 'ml' (model training & eval)")
    parser.add_argument("--data_path", type=str, default="extracted_features.csv", help="Path to input feature table CSV")
    parser.add_argument("--config_path", type=str, default="configs/model_config.yaml", help="Path to yaml config")
    args = parser.parse_args()

    if args.mode == "linkage":
        run_candidate_generation_pipeline()
    elif args.mode == "ml":
        run_ml_pipeline(data_path=args.data_path, config_path=args.config_path)
    else:
        run_candidate_generation_pipeline()
        run_ml_pipeline(data_path=args.data_path, config_path=args.config_path)


if __name__ == "__main__":
    main()

