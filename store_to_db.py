import sqlite3
import pandas as pd

# 1. Load the CSV we just created
print("Reading CSV data...")
df = pd.read_csv("competitor_data.csv")

# 2. Connect to the database (This creates the file if it doesn't exist)
# In a real company, this would be a connection string to AWS/Azure
conn = sqlite3.connect("market_analyzer.db")
cursor = conn.cursor()

# 3. Define the SQL Schema
# We use 'IF NOT EXISTS' so we can run this script multiple times without crashing
create_table_query = """
CREATE TABLE IF NOT EXISTS book_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    price REAL,
    availability TEXT,
    scraped_at TIMESTAMP
);
"""

cursor.execute(create_table_query)
print("SQL Table 'book_prices' checked/created.")

# 4. Load Data into SQL
# 'if_exists="append"' means if we run the scraper tomorrow, it ADDS rows, doesn't delete old ones.
# This allows us to track price history over time!
df.to_sql("book_prices", conn, if_exists="append", index=False)

print(f"Successfully loaded {len(df)} rows into the Database.")

# 5. Verification: Let's run a SQL Query to prove it works
print("\n--- Verifying Data with SQL ---")
query = "SELECT product_name, price FROM book_prices WHERE price < 20 LIMIT 5;"
results = pd.read_sql(query, conn)

print("Books under £20 (Fetched via SQL):")
print(results)

# Close connection
conn.close()