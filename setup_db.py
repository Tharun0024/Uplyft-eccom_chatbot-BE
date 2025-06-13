import pandas as pd
import sqlite3
import os

print("🚀 Starting database creation...")

# Load dataset
try:
    df = pd.read_csv("data/ecommerce-data.csv", encoding="ISO-8859-1")
    print("✅ CSV loaded:", len(df), "rows")
except Exception as e:
    print("❌ Failed to load CSV:", e)
    exit()

# Clean data
df = df[['Description', 'UnitPrice']]
df.dropna(inplace=True)
df = df[df['UnitPrice'] > 0]
df = df[df['Description'].str.strip() != '']
df['Description'] = df['Description'].str.replace(r'[^\w\s]', '', regex=True)
df.columns = ['name', 'price']
df.drop_duplicates(inplace=True)

print("✅ Cleaned rows:", len(df))

# Sample 200 products
sample_df = df.sample(min(200, len(df)), random_state=42)

# Save to DB
os.makedirs("database", exist_ok=True)
conn = sqlite3.connect("database/products.db")
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS products")
cursor.execute("CREATE TABLE products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL)")
sample_df.to_sql("products", conn, if_exists="append", index=False)
conn.commit()
conn.close()

print("✅ Database created at database/products.db with", len(sample_df), "products.")
