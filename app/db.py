import sqlite3
from pathlib import Path
from contextlib import contextmanager

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "shopper.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    rating REAL NOT NULL,
    inventory INTEGER NOT NULL,
    demand_index REAL NOT NULL,
    competitor_price REAL NOT NULL,
    tags TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS customers (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    preferred_categories TEXT NOT NULL,
    avg_order_value REAL NOT NULL,
    price_sensitivity REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS customer_events (
    id INTEGER PRIMARY KEY,
    customer_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    product_id TEXT,
    event_time TEXT NOT NULL,
    FOREIGN KEY(customer_id) REFERENCES customers(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
);
CREATE INDEX IF NOT EXISTS idx_events_customer ON customer_events(customer_id);
CREATE INDEX IF NOT EXISTS idx_events_product ON customer_events(product_id);
"""

@contextmanager
def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with get_connection() as conn:
        conn.executescript(SCHEMA)
