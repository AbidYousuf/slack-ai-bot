# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama


from langchain.messages import SystemMessage, HumanMessage

# llm = ChatOllama(model="gemma:2b")
llm = ChatOllama(
    model="gemma:2b", #gemma:2b  
    temperature=0,
    streaming=False
)

def generate_sql(question):

    system_prompt = """
You are a PostgreSQL expert.

There is only ONE table:

Table name: sales_daily

Columns:
- date (date)
- region (text)
- category (text)
- revenue (numeric)
- orders (integer)

Rules:
- Return ONLY one valid PostgreSQL SELECT statement.
- Do not explain anything.
- Do not use markdown.
- Do not add comments.
- Only return SQL.
"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=question)
    ]

    response = llm.invoke(messages)

    return response.content.strip()