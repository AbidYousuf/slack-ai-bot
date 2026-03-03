from ask_engine import ask_database

question = "show revenue by region for 2025-09-01"

sql, rows = ask_database(question)

print("\nFinal Result:")
print("SQL:", sql)
print("Rows:", rows)