from langchain_core.tools import tool
from .recommender import recommend
from .pricing import calculate_dynamic_price
from .insights import customer_insights, aggregate_business_insights
from .data import get_product
@tool
def search_products(query: str, customer_id: str | None = None):
    """Search and rank products using shopper intent and optional preference signals."""
    return recommend(query, customer_id)
@tool
def get_product_price(product_id: str):
    """Get the current business-rule-constrained price for a product."""
    p=get_product(product_id)
    return calculate_dynamic_price(p) if p else {"error":"product not found"}
@tool
def get_customer_profile(customer_id: str):
    """Get non-sensitive preference and purchase signals for recommendations."""
    return customer_insights(customer_id)
@tool
def get_customer_insights():
    """Get aggregated customer behavior insights for merchandising."""
    return aggregate_business_insights()
