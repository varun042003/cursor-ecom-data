# E-Commerce Data Pipeline

A simple data pipeline project that generates synthetic e-commerce data, ingests it into SQLite, and provides SQL reporting capabilities.

## Project Structure

```
diligent/
├── data/              # CSV files (generated)
├── backend/           # SQLite database (generated)
├── scripts/
│   ├── generate_data.py   # Generate synthetic CSV files
│   ├── ingest.py          # Ingest CSV files into SQLite
│   └── query.sql          # SQL reporting queries
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Setup

### 1. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Generate CSV Files

Generate synthetic e-commerce data (users, products, orders, order_items, payments):

```bash
python scripts/generate_data.py
```

This creates 5 CSV files in the `/data` directory:
- `users.csv` (100 rows)
- `products.csv` (80 rows)
- `orders.csv` (~250 rows)
- `order_items.csv` (1-5 items per order)
- `payments.csv` (one per order)

### Step 2: Ingest Data into SQLite

Load CSV files into SQLite database:

```bash
python scripts/ingest.py
```

This creates `backend/ecommerce.db` with all tables populated and displays validation counts.

### Step 3: Run SQL Queries

Execute the SQL reporting queries:

```bash
sqlite3 backend/ecommerce.db < scripts/query.sql
```

## Expected Output

### After generate_data.py:
- 5 CSV files created in `/data` directory
- Console output showing generation progress and row counts

### After ingest.py:
- Database file `backend/ecommerce.db` created
- Console output showing:
  - Table creation confirmation
  - Row counts for each table
  - Validation counts (users, products, orders)

### After query.sql:
Three query result sets:

1. **Full Order Report** (200 rows)
   - User name, order details, product list, quantities, totals, payment status
   - Ordered by most recent orders first

2. **Top 10 Best Selling Products**
   - Product details with total quantity sold and revenue
   - Ordered by quantity sold (descending)

3. **Monthly Sales Summary** (24 months)
   - Monthly aggregates: order count, total revenue, average order value
   - Ordered by most recent month first

## Database Schema

- **users**: Customer information
- **products**: Product catalog with categories
- **orders**: Order headers with totals
- **order_items**: Order line items (products and quantities)
- **payments**: Payment transactions linked to orders

All foreign key relationships are properly maintained.

