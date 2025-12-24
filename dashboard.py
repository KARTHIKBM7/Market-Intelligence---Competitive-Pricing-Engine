import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import config  # Import config to get DB_URL

# --- PAGE SETUP ---
st.set_page_config(page_title="Market Intelligence", layout="wide")
st.title("📊 Live Market Intelligence Dashboard")

# --- DATABASE CONNECTION ---
def get_db_connection():
    """
    Connects to the database using the URL from config.py
    """
    try:
        return config.DB_URL
    except AttributeError:
        # Fallback if config isn't found (for Streamlit Cloud later)
        return st.secrets["DB_URL"]

# --- LOAD DATA ---
try:
    db_url = get_db_connection()
    engine = create_engine(db_url)
    
    # Read the live table from the Cloud
    df = pd.read_sql("SELECT * FROM book_prices", engine)
    # Convert to datetime and adjust for India Time (UTC + 5:30)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['created_at'] = df['created_at'] + pd.Timedelta(hours=5, minutes=30)
    
    # --- METRICS ---
    col1, col2, col3 = st.columns(3)
    
    # 1. Calculate Average Price
    avg_price = df['price'].mean()
    
    # 2. Count Unique Books (Using 'title', not 'product_name')
    total_products = df['title'].nunique()
    
    # 3. Find Latest Scan Time (Using 'created_at', or fallback to 'scraped_at' if exists)
    if 'created_at' in df.columns:
        latest_scan = df['created_at'].max()
    elif 'scraped_at' in df.columns:
        latest_scan = df['scraped_at'].max()
    else:
        latest_scan = "Unknown"

    col1.metric("Avg Market Price", f"£{avg_price:.2f}")
    col2.metric("Products Tracked", total_products)
    col3.metric("Last Update", str(latest_scan)[:16])

    # --- VISUALS ---
    st.subheader("Price Distribution")
    # Using 'title' for hover data
    fig = px.histogram(df, x="price", title="Competitor Price Spread", hover_data=["title"])
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Raw Data Feed")
    # Sorting by price for better visibility (high to low)
    st.dataframe(df.sort_values(by="price", ascending=False))

except Exception as e:
    st.error(f"Database Connection Error: {e}")