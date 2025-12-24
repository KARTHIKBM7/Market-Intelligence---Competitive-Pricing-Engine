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
    1. Tries to load from local config.py (Laptop)
    2. If that fails, loads from Streamlit Secrets (Cloud)
    3. Fixes 'postgres://' typo automatically
    """
    db_url = ""
    
    try:
        # Try importing local config file
        import config
        db_url = config.DB_URL
    except ImportError:
        # If config.py doesn't exist, look in Streamlit Secrets
        db_url = st.secrets["DB_URL"]

    # FIX: SQLAlchemy requires 'postgresql://', but some hosts give 'postgres://'
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    return db_url

# --- LOAD DATA ---
try:
    db_url = get_db_connection()
    engine = create_engine(db_url)
    
    # Read the live table from the Cloud
    df = pd.read_sql("SELECT * FROM book_prices", engine)

    # Convert to datetime and adjust for India Time (UTC + 5:30)
    # We check if the column exists first to be safe
    time_col = 'created_at' if 'created_at' in df.columns else 'scraped_at'
    
    if time_col in df.columns:
        df[time_col] = pd.to_datetime(df[time_col])
        df[time_col] = df[time_col] + pd.Timedelta(hours=5, minutes=30)
        latest_scan = df[time_col].max()
    else:
        latest_scan = "Unknown"

    # --- METRICS ---
    col1, col2, col3 = st.columns(3)
    
    avg_price = df['price'].mean()
    total_products = df['title'].nunique()

    col1.metric("Avg Market Price", f"£{avg_price:.2f}")
    col2.metric("Products Tracked", total_products)
    col3.metric("Last Update (IST)", str(latest_scan)[:19])

    # --- SIDEBAR DOWNLOAD ---
    st.sidebar.header("Options")
    csv = df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name='market_intelligence_report.csv',
        mime='text/csv',
    )

    # --- VISUALS ---
    st.subheader("Price Distribution")
    fig = px.histogram(df, x="price", title="Competitor Price Spread", hover_data=["title"])
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Raw Data Feed")
    st.dataframe(df.sort_values(by="price", ascending=False))

except Exception as e:
    st.error(f"Something went wrong: {e}")