import requests
from bs4 import BeautifulSoup
import psycopg2
import os
import pandas as pd  # Import Pandas for the merging
from datetime import datetime
from notifications import send_email_alert
from etl_pipeline import run_etl_process  # <--- IMPORT YOUR NEW MODULE

# --- CONFIGURATION ---
URL = "http://books.toscrape.com/"

# --- DATABASE CONNECTION ---
def get_db_connection():
    try:
        db_url = os.getenv("DB_URL")
        # Fallback for local testing if secrets aren't set
        if not db_url:
            import config
            db_url = config.DB_URL
        conn = psycopg2.connect(db_url)
        return conn
    except Exception as e:
        print(f"❌ Database Connection Error: {e}")
        return None

# --- SCRAPER FUNCTION (SITE A) ---
def scrape_books():
    print("🌍 Scraping Books to Scrape (Site A)...")
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.select(".product_pod")
        
        data = []
        for book in books:
            title = book.select_one("h3 a")["title"]
            price_text = book.select_one(".price_color").text
            price = float(price_text.replace("£", "").replace("Â", ""))
            link = URL + book.select_one("h3 a")["href"]

            # WATCHDOG LOGIC (Alerts)
            if price < 33.0:
                print(f"🔥 Found a deal: {title} (£{price})")
                send_email_alert(title, price, link)
            
            data.append((title, price, link))
            
        print(f"✅ Scraped {len(data)} books from Site A.")
        return data
    except Exception as e:
        print(f"❌ Scraping Error: {e}")
        return []

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # 1. Get Real Data (Site A)
    site_a_data = scrape_books()
    
    # 2. Get Competitor Data (Site B) - NEW STEP!
    print("\n🔄 Running ETL Pipeline for Competitor Data (Site B)...")
    try:
        # Run the cleaning script we wrote
        df_competitor = run_etl_process("competitor_prices_messy.csv")
        
        # Convert DataFrame to a list of tuples so it matches Site A format
        # We ensure the columns match: (Title, Price, Link)
        site_b_data = list(df_competitor[['clean_title', 'price', 'url']].itertuples(index=False, name=None))
        
        print(f"✅ ETL Complete. Merging {len(site_b_data)} competitor rows.")
        
    except Exception as e:
        print(f"⚠️ ETL Failed (Skipping Competitor Data): {e}")
        site_b_data = []

    # 3. MERGE THE DATASETS
    all_data = site_a_data + site_b_data
    print(f"\n📊 Total Market Data Points: {len(all_data)}")

    # 4. UPLOAD TO DATABASE
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Create Table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS book_prices (
                    id SERIAL PRIMARY KEY,
                    title TEXT,
                    price DECIMAL,
                    link TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Insert Data
            insert_query = "INSERT INTO book_prices (title, price, link) VALUES (%s, %s, %s)"
            cursor.executemany(insert_query, all_data)
            
            conn.commit()
            print(f"🚀 SUCCESS: Uploaded {len(all_data)} rows to the Cloud Database!")
            
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"❌ Database Upload Failed: {e}")