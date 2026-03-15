import duckdb
import pandas as pd
import os
from openai import OpenAI

# Load data
df = pd.read_csv("data/events.csv")

con = duckdb.connect("analytics.db")
con.execute("CREATE OR REPLACE TABLE events AS SELECT * FROM df")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("\nAsk a question about the product data.\n")

question = input("Question: ")

prompt = f"""
You are a data analyst.

Table schema:
events(user_id INTEGER, event TEXT, timestamp TIMESTAMP)

Write a SQL query that answers the question.

Question:
{question}

Return SQL only.
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": prompt}]
)

sql_query = response.choices[0].message.content.strip()

print("\nGenerated SQL:\n")
print(sql_query)

try:
    result = con.execute(sql_query).fetchdf()
    print("\nResult:\n")
    print(result)
except Exception as e:
    print("\nQuery failed:", e)
