# agents/sql_agent.py
# src/agents/sql_agent.py
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent
from langchain_openai import ChatOpenAI
from config.settings import OPENAI_API_KEY,LLM_MODEL,SQLITE_DB_PATH
from utils.common_utils import format_agent_response

class SQLAgent:
    def __init__(self, db_path=SQLITE_DB_PATH):
        self.db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
        self.llm = ChatOpenAI(
            temperature=0,
            model=LLM_MODEL,
            api_key=OPENAI_API_KEY
        )
        toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
        self.agent = create_sql_agent(llm=self.llm, toolkit=toolkit, verbose=True)

    def run_query(self, query: str):
        # Run the query through SQLDatabase directly for structured output
        result = self.db.run(query)
        return result

if __name__ == "__main__":
    sql_agent = SQLAgent()

    # Agent natural language interface
    nl_response = sql_agent.agent.run("List the top 3 products with the highest average rating")
    print("\n Agent Response:")
    print(format_agent_response(nl_response))

