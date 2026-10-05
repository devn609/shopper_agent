from app.data import get_product, get_customer, customer_events

def test_product_loaded_from_sqlite():
    product = get_product("p001")
    assert product["name"] == "AeroRun Road Shoe"
    assert "running" in product["tags"]

def test_customer_loaded_from_sqlite():
    customer = get_customer("c001")
    assert "running" in customer["preferred_categories"]

def test_events_loaded_from_sqlite():
    events = customer_events("c001")
    assert len(events) >= 2
