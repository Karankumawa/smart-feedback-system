import os
from dotenv import load_dotenv
from pymongo import MongoClient
import sys

# Load environment variables
load_dotenv()

# Get MongoDB URI
mongo_uri = os.getenv('MONGODB_URI')

if not mongo_uri:
    print("❌ Error: MONGODB_URI not found in .env file")
    sys.exit(1)

print(f"Checking connection to: {mongo_uri.split('@')[-1] if '@' in mongo_uri else 'Localhost'}")

try:
    # Attempt connection
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("[OK] Connection Successful!")
    
    # List databases to verify permissions
    dbs = client.list_database_names()
    print(f"[OK] Databases Found: {', '.join(dbs)}")
    
except Exception as e:
    print(f"[FAIL] Connection Failed: {e}")
    sys.exit(1)
finally:
    if 'client' in locals():
        client.close()
