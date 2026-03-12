"""
Script to load reduced_dataset.csv into MongoDB
"""
import pandas as pd
from pymongo import MongoClient

# Read the CSV file
print("Reading CSV file...")
df = pd.read_csv("reduced_dataset.csv")

print(f"Loaded {len(df)} records from CSV")
print(f"Columns: {df.columns.tolist()}")
print(f"\nFirst few rows:")
print(df.head())

# Connect to MongoDB
print("\nConnecting to MongoDB...")
client = MongoClient("mongodb://localhost:27017/")
db = client["agricultureDB"]
collection = db["prices2025"]

# Clear existing data
print("\nClearing existing data...")
collection.delete_many({})

# Convert DataFrame to dictionary records
records = df.to_dict('records')

# Insert into MongoDB
print(f"\nInserting {len(records)} records into MongoDB...")
collection.insert_many(records)

print("\n✓ Data loaded successfully!")

# Display some statistics
commodities = collection.distinct("Commodity")
print(f"\nTotal commodities in database: {len(commodities)}")
print(f"Commodities: {sorted(commodities)[:10]}...")  # Show first 10

print("\nYou can now access the application at: http://127.0.0.1:8000")
