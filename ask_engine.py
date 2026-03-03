from db import get_connection
from nl_to_sql import generate_sql
cache = {}

def clean_sql(sql: str) -> str:
    """
    Removes markdown formatting like ```sql and ```
    """
    if not sql:
        return ""

    sql = sql.strip()

    # Remove ```sql or ``` wrappers
    if sql.startswith("```"):
        sql = sql.replace("```sql", "")
        sql = sql.replace("```", "")

    return sql.strip()


# def ask_database(question: str):
#     """
#     Full pipeline:
#     1. Generate SQL using LLM
#     2. Clean SQL
#     3. Execute SQL on Postgres
#     4. Return SQL + rows
#     """

#     # Step 1: Generate SQL
#     raw_sql = generate_sql(question)
#     print("\nRaw SQL from LLM:\n", raw_sql)

#     # Step 2: Clean SQL
#     sql = clean_sql(raw_sql)
#     print("\nCleaned SQL:\n", sql)

#     # Step 3: Execute SQL
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute(sql)
#     rows = cur.fetchall()

#     cur.close()
#     conn.close()

#     return sql, rows
def ask_database(question: str):

    # Check cache first
    if question in cache:
        print("Returning cached result")
        return cache[question]

    # Generate SQL
    raw_sql = generate_sql(question)
    print("\nRaw SQL from LLM:\n", raw_sql)

    sql = clean_sql(raw_sql)
    print("\nCleaned SQL:\n", sql)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(sql)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    # Store in cache
    cache[question] = (sql, rows)

    return sql, rows