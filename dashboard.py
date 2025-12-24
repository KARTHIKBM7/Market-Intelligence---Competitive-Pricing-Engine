import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# 1. PAGE SETUP
st.set_page_config(page_title="Market Intelligence Dashboard", layout="wide")

# 2. SECURE DATABASE CONNECTION
try:
    import config
    db_url = config.DB_URL
except ImportError:
    if "DB_URL" in st.secrets:
        db_url = st.secrets["DB_URL"]
    else:
        st.error("Database URL not found. Please check secrets.")
        st.stop()

# 3. DATA LOADING
@st.cache_data(ttl=60)
def load_data():
    engine = create_engine(db_url)
    df = pd.read_sql("SELECT * FROM books;", engine)
    df['price'] = pd.to_numeric(df['price'])
    df['date'] = pd.to_datetime(df['created_at'])
    return df

# 4. DASHBOARD LAYOUT
st.title("📊 Market Intelligence Dashboard")

try:
    df = load_data()
    
    # METRICS
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Products", len(df))
    col1.metric("Avg Price", f"£{df['price'].mean():.2f}")
    col1.metric("Lowest Price", f"£{df['price'].min():.2f}")

    st.markdown("---")

    # CHARTS
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Price Distribution")
        fig_hist = px.histogram(df, x="price", nbins=20)
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_right:
        st.subheader("Top 5 Cheapest Books")
        cheapest_books = df.nsmallest(5, 'price')
        fig_bar = px.bar(cheapest_books, x='price', y='title', orientation='h')
        fig_bar.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_bar, use_container_width=True)

    # REFRESH BUTTON
    if st.button('🔄 Refresh Data'):
        st.cache_data.clear()
        st.rerun()

except Exception as e:
    st.error(f"Error loading data: {e}")