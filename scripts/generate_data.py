"""
Generate synthetic e-commerce CSV files using Faker.
Creates 5 CSV files in the /data directory.
"""

import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
random.seed(42)  # For reproducibility

# Create data directory if it doesn't exist
import os
os.makedirs('data', exist_ok=True)

# ============================================================================
# 1. USERS.CSV
# ============================================================================
print("Generating users.csv...")
users = []
for i in range(1, 101):
    created_at = fake.date_time_between(start_date='-2y', end_date='now').isoformat()
    users.append({
        'user_id': i,
        'name': fake.name(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'created_at': created_at,
        'address_line': fake.street_address(),
        'city': fake.city(),
        'state': fake.state_abbr(),
        'postal_code': fake.zipcode()
    })

with open('data/users.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['user_id', 'name', 'email', 'phone', 'created_at', 'address_line', 'city', 'state', 'postal_code'])
    writer.writeheader()
    writer.writerows(users)
print(f"Generated {len(users)} users")

# ============================================================================
# 2. PRODUCTS.CSV
# ============================================================================
print("Generating products.csv...")
categories = ['electronics', 'fashion', 'home', 'sports', 'beauty', 'toys']
products = []
for i in range(1, 81):
    name = fake.catch_phrase()
    slug = name.lower().replace(' ', '-').replace(',', '').replace('.', '')
    created_at = fake.date_time_between(start_date='-1y', end_date='now').isoformat()
    products.append({
        'product_id': i,
        'name': name,
        'slug': slug,
        'description': fake.text(max_nb_chars=200),
        'category': random.choice(categories),
        'price': round(random.uniform(5.99, 499.99), 2),
        'stock_qty': random.randint(0, 500),
        'image': f"https://example.com/images/{slug}.jpg",
        'created_at': created_at
    })

with open('data/products.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['product_id', 'name', 'slug', 'description', 'category', 'price', 'stock_qty', 'image', 'created_at'])
    writer.writeheader()
    writer.writerows(products)
print(f"Generated {len(products)} products")

# ============================================================================
# 3. ORDERS.CSV
# ============================================================================
print("Generating orders.csv...")
orders = []
order_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
user_ids = list(range(1, 101))
product_ids = list(range(1, 81))

for i in range(1, 251):
    user_id = random.choice(user_ids)
    order_date = fake.date_time_between(start_date='-1y', end_date='now').isoformat()
    status = random.choice(order_statuses)
    # Total amount will be calculated from order_items, but we'll generate a placeholder
    total_amount = round(random.uniform(10.00, 2000.00), 2)
    orders.append({
        'order_id': i,
        'user_id': user_id,
        'order_date': order_date,
        'status': status,
        'total_amount': total_amount
    })

with open('data/orders.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['order_id', 'user_id', 'order_date', 'status', 'total_amount'])
    writer.writeheader()
    writer.writerows(orders)
print(f"Generated {len(orders)} orders")

# ============================================================================
# 4. ORDER_ITEMS.CSV
# ============================================================================
print("Generating order_items.csv...")
order_items = []
item_id = 1

# Read orders to get order dates for consistency
order_dict = {o['order_id']: o for o in orders}

for order in orders:
    order_id = order['order_id']
    num_items = random.randint(1, 5)
    selected_products = random.sample(product_ids, min(num_items, len(product_ids)))
    
    for product_id in selected_products:
        # Get product price from products list
        product = next((p for p in products if p['product_id'] == product_id), None)
        unit_price = product['price'] if product else round(random.uniform(5.99, 499.99), 2)
        quantity = random.randint(1, 5)
        
        order_items.append({
            'item_id': item_id,
            'order_id': order_id,
            'product_id': product_id,
            'quantity': quantity,
            'unit_price': unit_price
        })
        item_id += 1

# Recalculate order totals based on order_items
order_totals = {}
for item in order_items:
    order_id = item['order_id']
    if order_id not in order_totals:
        order_totals[order_id] = 0
    order_totals[order_id] += item['quantity'] * item['unit_price']

# Update orders.csv with correct totals
for order in orders:
    order_id = order['order_id']
    if order_id in order_totals:
        order['total_amount'] = round(order_totals[order_id], 2)

# Rewrite orders.csv with correct totals
with open('data/orders.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['order_id', 'user_id', 'order_date', 'status', 'total_amount'])
    writer.writeheader()
    writer.writerows(orders)

with open('data/order_items.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['item_id', 'order_id', 'product_id', 'quantity', 'unit_price'])
    writer.writeheader()
    writer.writerows(order_items)
print(f"Generated {len(order_items)} order items")

# ============================================================================
# 5. PAYMENTS.CSV
# ============================================================================
print("Generating payments.csv...")
payments = []
payment_methods = ['credit_card', 'debit_card', 'paypal', 'bank_transfer', 'cash_on_delivery']
payment_statuses = ['completed', 'pending', 'failed', 'refunded']

for order in orders:
    order_id = order['order_id']
    order_date = datetime.fromisoformat(order['order_date'])
    # Payment happens after order, but within a few days
    paid_at = (order_date + timedelta(days=random.randint(0, 3))).isoformat()
    amount = order['total_amount']
    method = random.choice(payment_methods)
    status = random.choice(payment_statuses)
    txn_id = fake.uuid4()
    
    payments.append({
        'payment_id': order_id,  # One payment per order
        'order_id': order_id,
        'paid_at': paid_at,
        'amount': amount,
        'method': method,
        'status': status,
        'txn_id': txn_id
    })

with open('data/payments.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['payment_id', 'order_id', 'paid_at', 'amount', 'method', 'status', 'txn_id'])
    writer.writeheader()
    writer.writerows(payments)
print(f"Generated {len(payments)} payments")

print("\nAll CSV files generated successfully in /data directory!")

