from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
import pandas as pd
import config  # Importing your existing database passwords
from typing import Optional

# 1. Create the App (The "Restaurant")
app = FastAPI(
    title="Market Intelligence API",
    description="A live data feed for competitor book prices.",
    version="1.0"
)

# 2. Database Connection (The "Kitchen")
def get_db_connection():
    return create_engine(config.DB_URL)

# --- ENDPOINTS (The "Menu Items") ---

@app.get("/")
def home():
    """The Welcome Page"""
    return {"message": "Welcome to the Market Intelligence API. Go to /prices to see data."}

@app.get("/prices")
def get_prices(max_price: Optional[float] = None):
    """
    Fetch book prices. 
    Optional: Add ?max_price=20 to filter for cheap books.
    """
    try:
        engine = get_db_connection()
        df = pd.read_sql("SELECT * FROM book_prices", engine)
        
        # --- THE SMART FILTER LOGIC ---
        if max_price is not None:
            # Keep only rows where price is LESS than the user's limit
            df = df[df['price'] <= max_price]
        # ------------------------------
        
        # Convert to dictionary
        data = df.to_dict(orient="records")
        return {"count": len(data), "limit_applied": max_price, "data": data}
    except Exception as e:
        return {"error": str(e)}

@app.get("/stats")
def get_stats():
    """Get quick Key Performance Indicators (KPIs)"""
    try:
        engine = get_db_connection()
        df = pd.read_sql("SELECT price FROM book_prices", engine)
        
        avg_price = df['price'].mean()
        lowest_price = df['price'].min()
        highest_price = df['price'].max()
        
        return {
            "average_price": round(avg_price, 2),
            "lowest_price": lowest_price,
            "highest_price": highest_price
        }
    except Exception as e:
        return {"error": str(e)}