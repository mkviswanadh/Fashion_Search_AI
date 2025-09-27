# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

# Read key from text file
with open("openai_key.txt", "r") as f:
    api_key = f.read().strip()

OPENAI_API_KEY = api_key
DB_URI = "sqlite:///db/sql_db/myntra_products.db"
LLM_MODEL = "gpt-3.5-turbo"
FAISS_INDEX_PATH = "embeddings/faiss_index"
RAW_DATA_PATH  = "data/raw/fashion_dataset_v2.csv"
CLEANED_DATA_PATH  = "data/cleaned/myntra_cleaned_fashion_products.parquet"
SQLITE_DB_PATH = "db/sql_db/myntra_products.db"
