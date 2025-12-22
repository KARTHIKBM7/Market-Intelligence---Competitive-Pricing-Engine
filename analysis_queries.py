import sqlite3
import pandas as pd

# Connect to your database
conn = sqlite3.connect("market_analyzer.db")

print("--- ANALYST REPORT ---\n")

# Question 1: What is the average price of all books?
# LOGIC: Uses Aggregate function AVG()
q1 = "SELECT AVG(price) as average_price FROM book_prices;"
print("1. Average Book Price:")
print(pd.read_sql(q1, conn))
print("-" * 30)

# Question 2: How many books are 'In Stock' vs other statuses?
# LOGIC: Uses GROUP BY to categorize data
q2 = """
SELECT availability, COUNT(*) as count 
FROM book_prices 
GROUP BY availability;
"""
print("2. Inventory Count:")
print(pd.read_sql(q2, conn))
print("-" * 30)

# Question 3: What are the top 3 most expensive books?
# LOGIC: Uses ORDER BY and LIMIT (Crucial for ranking)
q3 = """
SELECT product_name, price 
FROM book_prices 
ORDER BY price DESC 
LIMIT 3;
"""
print("3. Most Expensive Books:")
print(pd.read_sql(q3, conn))

conn.close()