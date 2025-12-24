import os
from typing import Optional
from fastapi import FastAPI
from sqlalchemy import create_engine
import pandas as pd

# 1. Create the App
app = FastAPI(
    title="Market Intelligence API",
    description="A live data feed for competitor book prices.",
    version="1.0"
)

# 2. Database Connection (Smart Version)
def get_db_connection():
    # A. First, try to get the URL from Render's Environment Variables
    db_url = os.getenv("DB_URL")
    
    # B. If that fails (meaning we are on Localhost), try importing config.py
    if not db_url:
        try:
            import config
            db_url = config.DB_URL
        except ImportError:
            # If neither works, we have a problem
            raise Exception("Database URL not found! Set DB_URL var or create config.py.")

    # C. Fix potential "postgres://" typo (common in cloud apps)
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    return create_engine(db_url)

# --- ENDPOINTS ---

@app.get("/")
def home():
    return {"message": "Welcome to the Market Intelligence API. Go to /docs to test it."}

@app.get("/prices")
def get_prices(max_price: Optional[float] = None):
    try:
        engine = get_db_connection()
        df = pd.read_sql("SELECT * FROM book_prices", engine)
        
        if max_price is not None:
            df = df[df['price'] <= max_price]
        
        data = df.to_dict(orient="records")
        return {"count": len(data), "limit_applied": max_price, "data": data}
    except Exception as e:
        return {"error": str(e)}

@app.get("/stats")
def get_stats():
    try:
        engine = get_db_connection()
        df = pd.read_sql("SELECT price FROM book_prices", engine)
        
        return {
            "average_price": round(df['price'].mean(), 2),
            "lowest_price": df['price'].min(),
            "highest_price": df['price'].max()
        }
    except Exception as e:
        return {"error": str(e)}