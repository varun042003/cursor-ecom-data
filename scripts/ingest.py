"""
Ingest CSV files from /data into SQLite database.
Creates backend/ecommerce.db with all tables and data.
"""

import os
import sqlite3
import pandas as pd

# Create backend directory if it doesn't exist
os.makedirs('backend', exist_ok=True)

# Remove existing database if it exists
db_path = 'backend/ecommerce.db'
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Removed existing database: {db_path}")

# Create SQLite connection
conn = sqlite3.connect(db_path)
print(f"Created database: {db_path}")

# ============================================================================
# CREATE TABLES
# ============================================================================
print("\nCreating tables...")

conn.execute('''
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    created_at TEXT,
    address_line TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT
)
''')

conn.execute('''
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    slug TEXT,
    description TEXT,
    category TEXT,
    price REAL,
    stock_qty INTEGER,
    image TEXT,
    created_at TEXT
)
''')

conn.execute('''
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    order_date TEXT,
    status TEXT,
    total_amount REAL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
''')

conn.execute('''
CREATE TABLE order_items (
    item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price REAL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
''')

conn.execute('''
CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    paid_at TEXT,
    amount REAL,
    method TEXT,
    status TEXT,
    txn_id TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
)
''')

print("Tables created successfully")

# ============================================================================
# INGEST CSV FILES
# ============================================================================
print("\nIngesting CSV files...")

# Read and insert users
print("  - Reading users.csv...")
df_users = pd.read_csv('data/users.csv')
df_users.to_sql('users', conn, if_exists='append', index=False)
print(f"    Inserted {len(df_users)} users")

# Read and insert products
print("  - Reading products.csv...")
df_products = pd.read_csv('data/products.csv')
df_products.to_sql('products', conn, if_exists='append', index=False)
print(f"    Inserted {len(df_products)} products")

# Read and insert orders
print("  - Reading orders.csv...")
df_orders = pd.read_csv('data/orders.csv')
df_orders.to_sql('orders', conn, if_exists='append', index=False)
print(f"    Inserted {len(df_orders)} orders")

# Read and insert order_items
print("  - Reading order_items.csv...")
df_order_items = pd.read_csv('data/order_items.csv')
df_order_items.to_sql('order_items', conn, if_exists='append', index=False)
print(f"    Inserted {len(df_order_items)} order items")

# Read and insert payments
print("  - Reading payments.csv...")
df_payments = pd.read_csv('data/payments.csv')
df_payments.to_sql('payments', conn, if_exists='append', index=False)
print(f"    Inserted {len(df_payments)} payments")

# Commit changes
conn.commit()

# ============================================================================
# VALIDATION COUNTS
# ============================================================================
print("\n" + "="*50)
print("VALIDATION COUNTS")
print("="*50)

# Row counts
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM users")
user_count = cursor.fetchone()[0]
print(f"Users in database: {user_count}")

cursor.execute("SELECT COUNT(*) FROM products")
product_count = cursor.fetchone()[0]
print(f"Products in database: {product_count}")

cursor.execute("SELECT COUNT(*) FROM orders")
order_count = cursor.fetchone()[0]
print(f"Orders in database: {order_count}")

cursor.execute("SELECT COUNT(*) FROM order_items")
item_count = cursor.fetchone()[0]
print(f"Order items in database: {item_count}")

cursor.execute("SELECT COUNT(*) FROM payments")
payment_count = cursor.fetchone()[0]
print(f"Payments in database: {payment_count}")

conn.close()
print("\nDatabase ingestion completed successfully!")

