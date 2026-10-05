from .db import init_db, get_connection

init_db()

def _product(row):
    if not row:
        return None
    d = dict(row)
    d["tags"] = d["tags"].split("|")
    return d

def _customer(row):
    if not row:
        return None
    d = dict(row)
    d["preferred_categories"] = d["preferred_categories"].split("|")
    return d

def get_product(product_id: str):
    with get_connection() as conn:
        return _product(conn.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone())

def get_customer(customer_id: str):
    with get_connection() as conn:
        return _customer(conn.execute("SELECT * FROM customers WHERE id=?", (customer_id,)).fetchone())

def all_products():
    with get_connection() as conn:
        return [_product(r) for r in conn.execute("SELECT * FROM products").fetchall()]

def all_customers():
    with get_connection() as conn:
        return [_customer(r) for r in conn.execute("SELECT * FROM customers").fetchall()]

def customer_events(customer_id: str, event_type: str | None = None):
    query = "SELECT * FROM customer_events WHERE customer_id=?"
    params = [customer_id]
    if event_type:
        query += " AND event_type=?"
        params.append(event_type)
    query += " ORDER BY event_time DESC"
    with get_connection() as conn:
        return [dict(r) for r in conn.execute(query, params).fetchall()]
