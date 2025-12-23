import requests
from notifications import send_email_alert
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import datetime
import random
import os  # <--- NEW IMPORT

# --- CONFIGURATION ---
try:
    # Try to import from the file (Laptop Mode)
    import config
    DATABASE_URL = config.DB_URL
except ImportError:
    # If file is missing, get from Environment (Cloud Mode)
    DATABASE_URL = os.getenv("DB_URL")

# (The rest of your code stays exactly the same...)
def extract_data_site_a():
    """Scrapes real data from BooksToScrape."""
    print("Scraping Site A...")
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get("http://books.toscrape.com/", headers=headers)
    
    if response.status_code != 200:
        return pd.DataFrame()

    soup = BeautifulSoup(response.content, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    
    data = []
    for book in books:
        title = book.h3.a["title"]
        price = float(book.find("p", class_="price_color").text.replace("£", ""))
        # --- NEW: WATCHDOG LOGIC ---
        # Alert me if a book is cheaper than £15
        if price < 35.0:
            print(f"🔥 Found a deal: {title} (£{price})")
            send_email_alert(title, price, "http://books.toscrape.com") 
        # ---------------------------
        collected_at = datetime.datetime.now()
        
        data.append({
            "product_name": title,
            "price": price,
            "source": "BooksToScrape",
            "scraped_at": collected_at
        })
    
    return pd.DataFrame(data)

def generate_competitor_data(df_site_a):
    """Generates simulated Competitor data."""
    print("Simulating Competitor (Site B)...")
    df_site_b = df_site_a.copy()
    df_site_b["source"] = "BookWorld"
    df_site_b["price"] = df_site_b["price"].apply(lambda x: round(x * random.uniform(0.9, 1.1), 2))
    return df_site_b

def load_data_to_cloud(df):
    """Uploads DataFrame to Cloud Database (PostgreSQL)."""
    if df.empty:
        print("No data to load.")
        return

    try:
        print(f"Connecting to Cloud Database...")
        # create_engine handles the connection to Postgres
        engine = create_engine(DATABASE_URL)
        
        # 'if_exists="append"' adds new rows without deleting old ones
        df.to_sql("book_prices", engine, if_exists="append", index=False)
        print(f"✅ SUCCESS: Loaded {len(df)} rows to the Cloud!")
        
    except Exception as e:
        print(f"❌ ERROR: Could not upload to cloud. Details: {e}")

if __name__ == "__main__":
    print("--- CLOUD PIPELINE STARTED ---")
    
    # 1. Scrape & Generate
    df_a = extract_data_site_a()
    
    if not df_a.empty:
        df_b = generate_competitor_data(df_a)
        full_data = pd.concat([df_a, df_b])
        
        # 2. Upload to Cloud
        load_data_to_cloud(full_data)
        
    print("--- PIPELINE FINISHED ---")