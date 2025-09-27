import pandas as pd
import os
from config.settings import RAW_DATA_PATH, CLEANED_DATA_PATH

def load_raw(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    # Remove duplicates based on p_id and name (adjust if needed)
    df = df.drop_duplicates(subset=["p_id", "name"])
    # Fill missing brand with 'Unknown'
    df["brand"] = df["brand"].fillna("Unknown")
    # Convert price and ratings to numeric, coerce errors to NaN
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["ratingcount"] = pd.to_numeric(df["ratingcount"], errors="coerce")
    df["avg_rating"] = pd.to_numeric(df["avg_rating"], errors="coerce")
    # Drop rows with no price or name
    df = df.dropna(subset=["price", "name"])
    return df

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Combine text columns for semantic search
    text_cols = ["name", "products", "brand", "colour", "description"]
    df["combined_text"] = df[text_cols].fillna("").agg(" ".join, axis=1)
    return df

def run_cleaning_pipeline():
    print(f"Loading raw data from {RAW_DATA_PATH}...")
    raw = load_raw(RAW_DATA_PATH)
    print("Cleaning data...")
    cleaned = clean_dataframe(raw)
    print("Feature engineering...")
    featured = feature_engineering(cleaned)
    os.makedirs(os.path.dirname(CLEANED_DATA_PATH), exist_ok=True)
    print(f"Saving cleaned data to {CLEANED_DATA_PATH}...")
    featured.to_parquet(CLEANED_DATA_PATH, index=False)
    print("Cleaning pipeline complete.")

if __name__ == "__main__":
    run_cleaning_pipeline()
