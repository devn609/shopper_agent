from app.data import get_product
from app.pricing import calculate_dynamic_price
def test_price_is_bounded():
    p=get_product("p001"); r=calculate_dynamic_price(p)
    assert .85*p["price"] <= r["dynamic_price"] <= 1.15*p["price"]
def test_pricing_is_business_signal_based():
    r=calculate_dynamic_price(get_product("p002")); assert set(r["pricing_basis"])=={"inventory","demand_index","competitor_price"}
