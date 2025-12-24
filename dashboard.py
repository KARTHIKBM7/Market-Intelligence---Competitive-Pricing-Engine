import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# --- 1. PAGE SETUP (Must be the first Streamlit command) ---
st.set_page_config(page_title="Market Intelligence Dashboard", layout="wide")

# --- 2. SECURE DATABASE CONNECTION ---
# This block fixes the "No module named config" error
try:
    # Option A: Local Development (Laptop)
    import config
    db_url = config.DB_URL
except ImportError:
    # Option B: Cloud Deployment (Streamlit Cloud)
    if "DB_URL" in st.secrets:
        db_url = st.secrets["DB_URL"]
    else:
        st.error("🚨 Critical Error: Database URL not found!")
        st.info("If you are on Streamlit Cloud, go to Settings > Secrets and add your DB_URL.")
        st.stop()

# --- 3. DATA LOADING FUNCTION ---
# We cache this so the app doesn't reload the database every time you click a button
@st.cache_data(ttl=60)  # Refresh cache every 60 seconds
def load_data():
    engine = create_engine(db_url)
    query = "SELECT * FROM books;"  # Fetch all data
    df = pd.read_sql(query, engine)
    
    # Clean up data types if needed
    df['price'] = pd.to_numeric(df['price'])
    df['date'] = pd.to_datetime(df['created_at'])
    return df

# --- 4. DASHBOARD LAYOUT ---
st.title("📊 Market Intelligence & Pricing Engine")
st.markdown("Real-time competitor tracking and price analysis.")

# Load the data
try:
    df = load_data()
    
    # -- KPI METRICS ROW --
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Products Tracked", len(df))
    with col2:
        avg_price = df['price'].mean()
        st.metric("Average Market Price", f"£{avg_price:.2f}")
    with col3:
        lowest_price = df['price'].min()
        st.metric("Lowest Price Found", f"£{lowest_price:.2f}")

    st.markdown("---")

    # -- VISUALIZATION ROW --
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("💰 Price Distribution")
        # Histogram showing how many books are at each price point
        fig_hist = px.histogram(df, x="price", nbins=20, title="Price Ranges of Products")
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_right:
        st.subheader("🏆 Top 5 Cheapest Books")
        # Bar chart of the 5 lowest priced items
        cheapest_books = df.nsmallest(5, 'price')
        fig_bar = px.bar(cheapest_books, x='price', y='title', orientation='h', 
                         title="Lowest Priced Assets", color='price')
        # Invert y-axis so the #