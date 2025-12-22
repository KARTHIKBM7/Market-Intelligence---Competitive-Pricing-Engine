import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

# 1. Define the URL we want to scrape
url = "http://books.toscrape.com/"

# 2. Pretend to be a browser (User-Agent) so we don't look like a bot
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

print("Step 1: Requesting data from website...")
response = requests.get(url, headers=headers)

# Check if request was successful (Status Code 200)
if response.status_code == 200:
    print("Success! Connection established.")
    
    # 3. Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    
    # 4. Find all product containers (This is specific to the website structure)
    # On this site, every book is inside an <article> tag with class "product_pod"
    books = soup.find_all("article", class_="product_pod")
    
    data = []

    # 5. Loop through each book and extract details
    for book in books:
        # Extract Title (It's in an <h3> tag, inside an <a> tag)
        title = book.h3.a["title"]
        
        # Extract Price (It's in a <p> tag with class "price_color")
        price_text = book.find("p", class_="price_color").text
        # Clean the price (Remove the £ symbol)
        price = float(price_text.replace("£", ""))
        
        # Extract Availability
        stock = book.find("p", class_="instock availability").text.strip()
        
        # Add a timestamp so we know when we scraped this
        collected_at = datetime.datetime.now()
        
        # Append to our list
        data.append({
            "product_name": title,
            "price": price,
            "availability": stock,
            "scraped_at": collected_at
        })

    # 6. Save to a DataFrame (Table format)
    df = pd.DataFrame(data)
    
    print(f"\nStep 2: Scraped {len(df)} books successfully.")
    print(df.head()) # Show first 5 rows
    
    # 7. Export to CSV (Temporary storage until we set up SQL)
    df.to_csv("competitor_data.csv", index=False)
    print("\nStep 3: Data saved to 'competitor_data.csv'")

else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")