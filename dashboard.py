import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# --- PAGE SETUP ---
st.set_page_config(page_title="Market Intelligence Pro", layout="wide")
st.title("💰 Market Intelligence: Pricing Strategy Engine")

# --- DATABASE CONNECTION ---
def get_db_connection():
    """
    1. Tries to load from local config.py (Laptop)
    2. If that fails, loads from Streamlit Secrets (Cloud)
    3. Fixes 'postgres://' typo automatically
    """
    db_url = ""
    try:
        import config
        db_url = config.DB_URL
    except ImportError:
        db_url = st.secrets["DB_URL"]

    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    return db_url

# --- LOAD DATA ---
try:
    db_url = get_db_connection()
    engine = create_engine(db_url)
    
    # Read the live table
    df = pd.read_sql("SELECT * FROM book_prices", engine)

    # Timezone Adjustment (UTC -> IST)
    time_col = 'created_at' if 'created_at' in df.columns else 'scraped_at'
    if time_col in df.columns:
        df[time_col] = pd.to_datetime(df[time_col])
        df[time_col] = df[time_col] + pd.Timedelta(hours=5, minutes=30)

    # --- 🧠 BUSINESS LOGIC SECTION (NEW) ---
    
    # 1. SIDEBAR: Strategy Controls
    st.sidebar.header("🛠️ Strategy Settings")
    
    # User inputs their Cost Price (Default £10)
    my_cost = st.sidebar.number_input("My Unit Cost (£)", value=10.0, step=0.5)
    
    # User inputs their Target Margin (Default 20%)
    target_margin = st.sidebar.slider("Minimum Profit Margin Target (%)", 0, 50, 20)

    # 2. CALCULATION: Apply Business Rules
    # Formula: Margin % = ((Price - Cost) / Price) * 100
    df['margin_pct'] = ((df['price'] - my_cost) / df['price']) * 100
    
    # Round to 1 decimal place
    df['margin_pct'] = df['margin_pct'].round(1)

    # 3. RECOMMENDATION ENGINE
    def get_recommendation(row):
        if row['margin_pct'] < 0:
            return "🛑 CRITICAL LOSS (Do Not Match)"
        elif row['margin_pct'] < target_margin:
            return "⚠️ LOW MARGIN (Proceed with Caution)"
        else:
            return "✅ GREEN LIGHT (Safe to Price Match)"

    df['recommendation'] = df.apply(get_recommendation, axis=1)

    # --- DASHBOARD VISUALS ---

    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    avg_price = df['price'].mean()
    safe_opportunities = len(df[df['recommendation'].str.contains("GREEN")])
    
    col1.metric("Avg Market Price", f"£{avg_price:.2f}")
    col2.metric("My Unit Cost", f"£{my_cost:.2f}")
    col3.metric("Safe Opportunities", f"{safe_opportunities} Products")
    col4.metric("Target Margin", f"{target_margin}%")

    st.divider()

    # Split Layout: Chart vs Strategy Table
    c1, c2 = st.columns([1, 2])

    with c1:
        st.subheader("📉 Margin Analysis")
        # Pie chart showing how many products are Safe vs Unsafe
        fig = px.pie(df, names='recommendation', title="Profitability Breakdown", hole=0.4,
                     color='recommendation',
                     color_discrete_map={
                         "✅ GREEN LIGHT (Safe to Price Match)": "green",
                         "⚠️ LOW MARGIN (Proceed with Caution)": "orange",
                         "🛑 CRITICAL LOSS (Do Not Match)": "red"
                     })
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("📋 Strategic Pricing Report")
        
        # Reorder columns to put the most important stuff first
        display_df = df[['title', 'price', 'margin_pct', 'recommendation']]
        
        # Style the dataframe (Highlight Rows)
        def color_recommendations(val):
            color = 'black'
            if 'CRITICAL' in val: color = 'red'
            elif 'LOW' in val: color = 'orange'
            elif 'GREEN' in val: color = 'green'
            return f'color: {color}; font-weight: bold'

        st.dataframe(
            display_df.style.map(color_recommendations, subset=['recommendation']),
            use_container_width=True,
            height=400
        )

    # --- DOWNLOAD REPORT ---
    st.sidebar.markdown("---")
    csv = df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="📥 Download Strategy Report (CSV)",
        data=csv,
        file_name='pricing_strategy_report.csv',
        mime='text/csv',
    )

except Exception as e:
    st.error(f"System Error: {e}")