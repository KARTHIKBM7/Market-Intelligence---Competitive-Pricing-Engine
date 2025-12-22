import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import datetime
import random

# --- CONFIGURATION ---
DATABASE_NAME = "market_analyzer.db"
URL = "http://books.toscrape.com/"

def extract_data_site_a():
    """Scrapes real data from BooksToScrape (Site A)."""
    print(f"Scraping Site A ({URL})...")
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    
    if response.status_code != 200:
        return pd.DataFrame()

    soup = BeautifulSoup(response.content, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    
    data = []
    for book in books:
        title = book.h3.a["title"]
        price = float(book.find("p", class_="price_color").text.replace("£", ""))
        stock = book.find("p", class_="instock availability").text.strip()
        collected_at = datetime.datetime.now()
        
        data.append({
            "product_name": title,
            "price": price,
            "availability": stock,
            "source": "BooksToScrape",  # <--- NEW COLUMN
            "scraped_at": collected_at
        })
    
    return pd.DataFrame(data)

def generate_competitor_data(df_site_a):
    """Generates simulated data for 'BookWorld' (Site B) for comparison."""
    print("Simulating Competitor (Site B) data...")
    
    # We copy the Site A data but change the source and price
    df_site_b = df_site_a.copy()
    df_site_b["source"] = "BookWorld" # <--- DIFFERENT SOURCE
    
    # Randomly adjust price by -10% to +10% to simulate competition
    # Logic: New Price = Old Price * Random Factor (0.90 to 1.10)
    df_site_b["price"] = df_site_b["price"].apply(lambda x: round(x * random.uniform(0.9, 1.1), 2))
    
    return df_site_b

def load_data(df):
    """Takes a DataFrame and saves it to SQLite Database."""
    if df.empty:
        return

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Updated Schema with 'source' column
    create_table_query = """
    CREATE TABLE IF NOT EXISTS book_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT,
        price REAL,
        availability TEXT,
        source TEXT,
        scraped_at TIMESTAMP
    );
    """
    cursor.execute(create_table_query)
    
    df.to_sql("book_prices", conn, if_exists="append", index=False)
    conn.close()
    print(f"Loaded {len(df)} rows into Database.")

if __name__ == "__main__":
    print("--- PIPELINE STARTED ---")
    
    # 1. Get Data from Site A
    df_a = extract_data_site_a()
    
    # 2. Generate Data for Site B (Competitor)
    if not df_a.empty:
        df_b = generate_competitor_data(df_a)
        
        # 3. Combine both datasets
        full_data = pd.concat([df_a, df_b])
        
        # 4. Load everything
        load_data(full_data)
        
    print("--- PIPELINE FINISHED ---")