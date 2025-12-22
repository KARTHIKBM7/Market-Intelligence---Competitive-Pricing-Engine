import psycopg2

# PASTE YOUR CONNECTION STRING INSIDE THE QUOTES BELOW
# It should look like: "postgresql://postgres:password@db.project..."
DB_URL = "postgresql://postgres:System123$@db.tpnimoubppdpuxkndqco.supabase.co:5432/postgres"

try:
    print("Attempting to connect to Cloud Database...")
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    # Simple query to ask the database "Who are you?"
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    
    print("✅ SUCCESS! Connected to:")
    print(db_version[0])
    
    conn.close()

except Exception as e:
    print("❌ CONNECTION FAILED")
    print(e)