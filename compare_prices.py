import sqlite3
import pandas as pd

conn = sqlite3.connect("market_analyzer.db")

# THE MONEY QUERY: Comparing Site A vs Site B
# We join the table to ITSELF (Self Join) matching on product_name
query = """
SELECT 
    T1.product_name,
    T1.price as Price_BooksToScrape,
    T2.price as Price_BookWorld,
    (T1.price - T2.price) as price_difference
FROM book_prices T1
JOIN book_prices T2 ON T1.product_name = T2.product_name
WHERE T1.source = 'BooksToScrape' 
  AND T2.source = 'BookWorld'
  AND T1.scraped_at = T2.scraped_at
ORDER BY price_difference DESC;
"""

df = pd.read_sql(query, conn)
print(df.head(10)) # Show top 10 price differences
conn.close()