import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from config.settings import LLM_MODEL, OPENAI_API_KEY

def extract_filters(user_query: str) -> dict:
    prompt_template = """
                        You are a product search assistant. Extract from the user's query relevant filters and parameters in JSON format.

                        Available filters:
                        - product_type (string, optional)
                        - brand (string, optional)
                        - colour (string, optional)
                        - max_price (number, optional, INR)
                        - min_rating (number, optional, 0-5 scale)

                        User Query: {query}

                        Return only a valid JSON with these keys (use null or omit keys if not present). Example:

                        {{
                        "product_type": "kurta",
                        "brand": "Khushal K",
                        "colour": "Black",
                        "max_price": 5000,
                        "min_rating": 4
                        }}

                        Do NOT return any extra text.
                        """
    prompt = PromptTemplate(template=prompt_template.strip(), input_variables=["query"])
    llm = ChatOpenAI(model=LLM_MODEL, openai_api_key=OPENAI_API_KEY, temperature=0)
    chain = prompt | llm
    response = chain.invoke({"query": user_query})
    
    try:
        filters = json.loads(response.content)
    except json.JSONDecodeError:
        filters = {}
        print("Could not parse filters from LLM response:", response.content)

    return filters
