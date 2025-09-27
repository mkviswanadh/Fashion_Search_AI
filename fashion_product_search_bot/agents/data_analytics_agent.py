# agents/data_analytics_agent.py
import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
import re
from config.settings import OPENAI_API_KEY, LLM_MODEL, RAW_DATA_PATH
from utils.common_utils import format_agent_response

# --- Create LangChain agent for Pandas DataFrame
def get_analytics_agent(df):
    llm = ChatOpenAI(
        temperature=0,
        model=LLM_MODEL,
        api_key=OPENAI_API_KEY
    )
    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        verbose=True,
        agent_type="openai-tools",  
        handle_parsing_errors=True,
        allow_dangerous_code=True
    )
    return agent



# --- Wrap query execution with formatting
def run_analytics_query(nl_query: str) -> str:
    try:
        raw_response = pandas_agent.run(nl_query)
        return format_agent_response(raw_response)
    except Exception as e:
        return f"⚠️ Error: {e}"

if __name__ == "__main__":
    
    df = pd.read_csv(RAW_DATA_PATH).fillna("")
    pandas_agent = get_analytics_agent(df)
   
    # Agent natural language interface
    nl_response = pandas_agent.run("List the top 5 product categories by number of purchases")
    print("\n Agent Response:")
    print(format_agent_response(nl_response))
