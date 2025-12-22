import streamlit as st
import sqlite3
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="Market Intelligence", layout="wide")
st.title("📊 Market Competitor Analyzer")

# 2. Connect to DB
conn = sqlite3.connect("market_analyzer.db")

# 3. The "Analyst" Query (The same logic you just ran)
query = """
SELECT 
    T1.product_name,
    T1.price as Price_Site_A,
    T2.price as Price_Site_B,
    (T1.price - T2.price) as diff,
    CASE 
        WHEN T1.price < T2.price THEN 'Site A is Cheaper'
        ELSE 'Site B is Cheaper'
    END as recommendation
FROM book_prices T1
JOIN book_prices T2 ON T1.product_name = T2.product_name
WHERE T1.source = 'BooksToScrape' 
  AND T2.source = 'BookWorld'
  AND T1.scraped_at = T2.scraped_at
ORDER BY diff DESC;
"""

df = pd.read_sql(query, conn)
conn.close()

# 4. KPI Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Products Tracked", len(df))
col2.metric("Cheaper at Site A", len(df[df['recommendation'] == 'Site A is Cheaper']))
col3.metric("Cheaper at Site B", len(df[df['recommendation'] == 'Site B is Cheaper']))

st.divider()

# 5. The "Deal Hunter" Table
st.subheader("🏆 Best Deals Found Today")

# Highlight logic: Green if Site A is cheaper, Red if Site B is cheaper
def highlight_recommendation(val):
    color = 'green' if val == 'Site A is Cheaper' else 'red'
    return f'color: {color}; font-weight: bold'

st.dataframe(df.style.applymap(highlight_recommendation, subset=['recommendation']))

# 6. Scatter Plot: Price Comparison
st.subheader("Price War: Site A vs Site B")
st.scatter_chart(
    df,
    x='Price_Site_A',
    y='Price_Site_B',
    color='recommendation',
    size='diff' 
)