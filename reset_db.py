import psycopg2
import os
import config # Import your local config file

def reset_database():
    print("🗑️ connecting to database to wipe old table...")
    
    # Connect using the URL in your config.py
    conn = psycopg2.connect(config.DB_URL)
    cursor = conn.cursor()
    
    try:
        # 1. DROP the existing table (Delete it completely)
        cursor.execute("DROP TABLE IF EXISTS book_prices;")
        print("✅ Old table 'book_prices' deleted.")
        
        # 2. COMMIT the change
        conn.commit()
        print("✨ Database is clean. Run main.py now to rebuild it.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    reset_database()