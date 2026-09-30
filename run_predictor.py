import os
import argparse
import pandas as pd
from ml.predict import predict_pairs

def run_csv_uploader_predictor(input_csv_path: str, output_csv_path: str = "prediction_output.csv", model_dir: str = "models/final/"):
    """
    Reads an uploaded CSV feature table, runs the saved LightGBM model at optimal threshold 0.05,
    and exports the full prediction result CSV.
    """
    if not os.path.exists(input_csv_path):
        raise FileNotFoundError(f"Input CSV file not found at: {input_csv_path}")

    print(f"[1/3] Reading input CSV: {input_csv_path}")
    df_input = pd.read_csv(input_csv_path)
    print(f"      - Loaded {len(df_input):,} rows and {len(df_input.columns)} columns.")

    print(f"[2/3] Executing LightGBM inference & threshold prediction...")
    output_df = predict_pairs(df_input, model_dir=model_dir)

    print(f"[3/3] Exporting prediction results to: {output_csv_path}")
    output_df.to_csv(output_csv_path, index=False)
    
    match_count = (output_df["is_match_prediction"] == 1).sum()
    unmatched_count = len(output_df) - match_count
    
    print("\n==================================================")
    print("         ENTITY RESOLUTION PREDICTION OUTPUT       ")
    print("==================================================")
    print(f"Total Rows Processed   : {len(output_df):,}")
    print(f"Predicted Entity Matches: {match_count:,}")
    print(f"Predicted Unmatched    : {unmatched_count:,}")
    print(f"Output File Location   : {os.path.abspath(output_csv_path)}")
    print("==================================================\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload CSV and Predict Entity Linkages")
    parser.add_argument("--input", type=str, required=True, help="Path to input CSV feature table to upload")
    parser.add_argument("--output", type=str, default="prediction_output.csv", help="Path to save output prediction CSV")
    args = parser.parse_args()

    run_csv_uploader_predictor(input_csv_path=args.input, output_csv_path=args.output)
