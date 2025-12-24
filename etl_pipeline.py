import pandas as pd
import re

def clean_currency(price_str):
    """
    Extracts the numeric value from a messy string like '$ 22.65' or '23.88 GBP'.
    """
    if pd.isna(price_str):
        return 0.0
    
    # Convert to string just in case
    price_str = str(price_str)
    
    # Regex Magic: Find a pattern that looks like a number (digits + optional dot)
    # This looks for: one or more digits (\d+), optionally followed by a dot and more digits (\.?\d*)
    match = re.search(r"(\d+\.?\d*)", price_str)
    
    if match:
        return float(match.group(1))
    return 0.0

def run_etl_process(csv_file):
    print("--- STARTING ETL PIPELINE ---")
    
    # 1. EXTRACT (Read the raw file)
    print(f"📥 Loading raw data from {csv_file}...")
    df = pd.read_csv(csv_file)
    print(f"   Raw Rows: {len(df)}")
    
    # 2. TRANSFORM (Clean the mess)
    print("🧹 Cleaning data...")
    
    # A. Standardize Titles (The Requiem Red == the requiem red)
    df['clean_title'] = df['book_name'].str.strip().str.title()
    
    # B. clean Prices (Remove $, USD, GBP)
    df['price'] = df['raw_price'].apply(clean_currency)
    
    # C. Remove Duplicates (Keep the lowest price if we have duplicates)
    # Sort by price ascending, then drop duplicates based on title, keeping the first (cheapest)
    df = df.sort_values('price', ascending=True)
    df = df.drop_duplicates(subset=['clean_title'], keep='first')
    
    # 3. Validation
    print("✨ Transformation Complete!")
    print(df[['clean_title', 'price', 'raw_price']].head(10))
    
    return df

if __name__ == "__main__":
    # Test the pipeline immediately
    cleaned_data = run_etl_process("competitor_prices_messy.csv")