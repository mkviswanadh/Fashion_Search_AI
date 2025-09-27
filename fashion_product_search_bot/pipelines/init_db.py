# db/init_db.py

import pandas as pd
from sqlalchemy import create_engine
import os
from config.settings import CLEANED_DATA_PATH,SQLITE_DB_PATH

def init_db(parquet_path=CLEANED_DATA_PATH, sqlite_db_path=SQLITE_DB_PATH):
    # Ensure the DB directory exists
    os.makedirs("db", exist_ok=True)

    # Full DB file path
    db_path = os.path.abspath(SQLITE_DB_PATH)
    db_uri = f"sqlite:///{db_path}"

    # Load cleaned parquet data
    df = pd.read_parquet(parquet_path)

    # Create SQLite engine and write to DB
    engine = create_engine(db_uri)
    df.to_sql("products", con=engine, if_exists="replace", index=False)

    print(f"Database created at {db_uri}")
    print(f"Table 'products' loaded with {len(df)} rows.")

if __name__ == "__main__":
    init_db()
