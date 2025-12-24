import pandas as pd
import random

def create_messy_competitor_data():
    """
    Generates a CSV file representing a 'messy' data feed from a competitor.
    Contains:
    - Inconsistent capitalization
    - Currency symbols that need cleaning
    - Duplicate rows
    """
    data = [
        {"book_name": "The Requiem Red", "raw_price": "$ 22.65", "url": "http://bookworld.com/item1"},
        {"book_name": "the requiem red", "raw_price": "USD 22.00", "url": "http://bookworld.com/item1-promo"}, # Duplicate with lower price
        {"book_name": "STARVING HEARTS (TRIANGULAR TRADE TRILOGY, #1)", "raw_price": "£14.00", "url": "http://bookworld.com/item2"},
        {"book_name": "Olio", "raw_price": "23.88 GBP", "url": "http://bookworld.com/item3"},
        {"book_name": "set me free", "raw_price": "17.00", "url": "http://bookworld.com/item4"},
        {"book_name": "SHAKESPEARE'S SONNETS", "raw_price": "$20.00", "url": "http://bookworld.com/item5"},
        {"book_name": "The Black Maria", "raw_price": "18.50", "url": "http://bookworld.com/item6"}, # New book not in our top list
    ]
    
    # Create a DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    filename = "competitor_prices_messy.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Generated messy data file: {filename}")
    print("Preview of the mess:")
    print(df.head(10))

if __name__ == "__main__":
    create_messy_competitor_data()