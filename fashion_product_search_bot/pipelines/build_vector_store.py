import pandas as pd
import sqlite3
from config.settings import OPENAI_API_KEY, CLEANED_DATA_PATH, SQLITE_DB_PATH, FAISS_INDEX_PATH
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

def ingest_data():
    print(f"Loading cleaned data from {CLEANED_DATA_PATH}...")
    df = pd.read_parquet(CLEANED_DATA_PATH)

    print(f"Writing data to SQLite DB at {SQLITE_DB_PATH}...")
    conn = sqlite3.connect(SQLITE_DB_PATH)
    df.to_sql("products", conn, if_exists="replace", index=False)
    conn.close()

    print("Creating vector store for semantic search...")
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    texts = df["combined_text"].tolist()
    vectorstore = FAISS.from_texts(texts, embeddings)

    # Save vectorstore to disk
    vectorstore.save_local(FAISS_INDEX_PATH)
    print("Ingestion complete.")

if __name__ == "__main__":
    ingest_data()
