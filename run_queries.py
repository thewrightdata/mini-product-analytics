"""
Mini product analytics runner.

Loads event data into DuckDB and executes all SQL queries in the analytics
directory. This mirrors a simplified warehouse-first analytics workflow.
"""

import duckdb
import pandas as pd
from pathlib import Path
import sys

DATA_FILE = Path("data/events.csv")
ANALYTICS_DIR = Path("analytics")

def load_events():
    if not DATA_FILE.exists():
        print(f"Error: dataset not found at {DATA_FILE}")
        sys.exit(1)

    try:
        df = pd.read_csv(DATA_FILE)
        return df
    except Exception as e:
        print(f"Failed to load dataset: {e}")
        sys.exit(1)


def run_queries():
    if not ANALYTICS_DIR.exists():
        print("Error: analytics directory not found.")
        sys.exit(1)

    con = duckdb.connect("analytics.db")

    df = load_events()
    con.execute("CREATE OR REPLACE TABLE events AS SELECT * FROM df")

    sql_files = list(ANALYTICS_DIR.glob("*.sql"))

    if not sql_files:
        print("No SQL queries found in analytics folder.")
        return

    print("\nRunning analytics queries...\n")

    for sql_file in sql_files:
        print(f"--- {sql_file.name} ---")

        try:
            query = sql_file.read_text()
            result = con.execute(query).fetchdf()
            print(result)
            print()
        except Exception as e:
            print(f"Query failed: {e}\n")


if __name__ == "__main__":
    run_queries()
