import sqlite3
import pandas as pd
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from config.settings import OPENAI_API_KEY, SQLITE_DB_PATH, FAISS_INDEX_PATH

#from config import SQLITE_DB_PATH

def load_vectorstore():
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = FAISS.load_local(
                                        FAISS_INDEX_PATH,
                                        embeddings,
                                        allow_dangerous_deserialization=True
                                    )

    return vectorstore

def search_products(user_query: str, filters: dict, top_k=3) -> pd.DataFrame:
    # Connect to SQLite DB
    conn = sqlite3.connect(SQLITE_DB_PATH)

    # Base SQL query
    sql = "SELECT * FROM products WHERE 1=1"

    params = []

    # Apply filters
    if filters.get("product_type"):
        sql += " AND products LIKE ?"
        params.append(f"%{filters['product_type']}%")
    if filters.get("brand"):
        sql += " AND brand LIKE ?"
        params.append(f"%{filters['brand']}%")
    if filters.get("colour"):
        sql += " AND colour LIKE ?"
        params.append(f"%{filters['colour']}%")
    if filters.get("max_price"):
        sql += " AND price <= ?"
        params.append(filters["max_price"])
    if filters.get("min_rating"):
        sql += " AND avg_rating >= ?"
        params.append(filters["min_rating"])

    df = pd.read_sql(sql, conn, params=params)
    conn.close()

    if df.empty:
        return df

    # Semantic rerank using vector store if available
    vectorstore = load_vectorstore()
    docs_and_scores = vectorstore.similarity_search_with_score(user_query, k=min(top_k, len(df)))

    # Filter results by p_id matching db results (intersection)
    p_ids = df["p_id"].astype(str).tolist()
    filtered = []
    for doc, score in docs_and_scores:
        metadata = doc.metadata
        if metadata.get("p_id") in p_ids:
            filtered.append(metadata)
        if len(filtered) >= top_k:
            break

    if not filtered:
        return df.head(top_k)  # fallback: return filtered DB results

    return pd.DataFrame(filtered).head(top_k)

