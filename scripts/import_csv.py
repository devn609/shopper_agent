import csv
import sqlite3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.db import init_db, get_connection

CSV_DIR = ROOT / "data" / "csv"


def import_products(conn):
    with open(CSV_DIR / "products.csv", newline="", encoding="utf-8") as f:
        rows = csv.DictReader(f)
        conn.executemany("""
            INSERT INTO products
            (id,name,category,price,rating,inventory,demand_index,competitor_price,tags)
            VALUES (:id,:name,:category,:price,:rating,:inventory,:demand_index,:competitor_price,:tags)
            ON CONFLICT(id) DO UPDATE SET
              name=excluded.name, category=excluded.category, price=excluded.price,
              rating=excluded.rating, inventory=excluded.inventory,
              demand_index=excluded.demand_index, competitor_price=excluded.competitor_price,
              tags=excluded.tags
        """, rows)


def import_customers(conn):
    with open(CSV_DIR / "customers.csv", newline="", encoding="utf-8") as f:
        rows = csv.DictReader(f)
        conn.executemany("""
            INSERT INTO customers
            (id,name,preferred_categories,avg_order_value,price_sensitivity)
            VALUES (:id,:name,:preferred_categories,:avg_order_value,:price_sensitivity)
            ON CONFLICT(id) DO UPDATE SET
              name=excluded.name, preferred_categories=excluded.preferred_categories,
              avg_order_value=excluded.avg_order_value,
              price_sensitivity=excluded.price_sensitivity
        """, rows)


def import_events(conn):
    with open(CSV_DIR / "customer_events.csv", newline="", encoding="utf-8") as f:
        rows = csv.DictReader(f)
        conn.executemany("""
            INSERT OR REPLACE INTO customer_events
            (id,customer_id,event_type,product_id,event_time)
            VALUES (:id,:customer_id,:event_type,:product_id,:event_time)
        """, rows)


if __name__ == "__main__":
    init_db()
    with get_connection() as conn:
        import_products(conn)
        import_customers(conn)
        import_events(conn)
    print(f"Imported CSV data into {ROOT / 'data' / 'shopper.db'}")
