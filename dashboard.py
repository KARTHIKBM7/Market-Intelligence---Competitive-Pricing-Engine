import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# --- PAGE SETUP ---
st.set_page_config(page_title="Market Intelligence", layout="wide")
st.title("📊 Live Market Intelligence Dashboard")

# --- DATABASE CONNECTION ---
def get_db_connection():
    """
    Intelligent Connection:
    1. Checks if we are on your laptop (uses config.py)
    2. Checks if we are on the Cloud (uses st.secrets)
    """
    try:
        import config
        return config.DB_URL
    except ImportError:
        # If config.py is missing, we are likely on Streamlit Cloud
        return st.secrets["DB_URL"]

# --- LOAD DATA ---
try:
    db_url = get_db_connection()
    engine = create_engine(db_url)
    
    # Read the live table from the Cloud
    df = pd.read_sql("SELECT * FROM book_prices", engine)
    
    # --- METRICS ---
    col1, col2, col3 = st.columns(3)
    avg_price = df['price'].mean()
    total_products = df['product_name'].nunique()
    latest_scan = df['scraped_at'].max()

    col1.metric("Avg Market Price", f"£{avg_price:.2f}")
    col2.metric("Products Tracked", total_products)
    col3.metric("Last Update", str(latest_scan)[:16])

    # --- VISUALS ---
    st.subheader("Price Distribution")
    fig = px.histogram(df, x="price", color="source", nbins=20, title="Competitor Price Spread")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Raw Data Feed")
    st.dataframe(df.sort_values(by="scraped_at", ascending=False))

except Exception as e:
    st.error(f"Database Connection Error: {e}")