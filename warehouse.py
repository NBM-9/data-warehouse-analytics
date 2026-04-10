import pandas as pd
import sqlite3

# =========================
# STEP 1: CREATE RAW DATA
# =========================
data = {
    "order_id": [1, 2, 3, 4, 5],
    "customer": ["A", "B", "A", "C", "B"],
    "product": ["Laptop", "Phone", "Mouse", "Laptop", "Phone"],
    "price": [1000, 500, 50, 1200, 600],
    "quantity": [1, 2, 3, 1, 1]
}

df = pd.DataFrame(data)

print("Original Data:")
print(df)

# =========================
# STEP 2: TRANSFORMATION
# =========================
df["revenue"] = df["price"] * df["quantity"]
df = df.drop_duplicates()

print("\nTransformed Data:")
print(df)

# =========================
# STEP 3: LOAD INTO DATABASE
# =========================
conn = sqlite3.connect("sales.db")

df.to_sql("sales", conn, if_exists="replace", index=False)

print("\nData loaded into SQLite database (sales.db)")

# =========================
# STEP 4: SQL ANALYTICS
# =========================

print("\n--- BUSINESS INSIGHTS ---")

# 1. Total revenue
query1 = "SELECT SUM(revenue) as total_revenue FROM sales"
print("\nTotal Revenue:")
print(pd.read_sql(query1, conn))

# 2. Revenue by product
query2 = """
SELECT product, SUM(revenue) as revenue
FROM sales
GROUP BY product
ORDER BY revenue DESC
"""
print("\nRevenue by Product:")
print(pd.read_sql(query2, conn))

# 3. Top customer
query3 = """
SELECT customer, SUM(revenue) as revenue
FROM sales
GROUP BY customer
ORDER BY revenue DESC
"""
print("\nTop Customers:")
print(pd.read_sql(query3, conn))

conn.close()