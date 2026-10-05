from collections import Counter
from .data import all_customers, all_products, get_customer, customer_events

def customer_insights(customer_id: str) -> dict:
    customer = get_customer(customer_id)
    if not customer:
        return {"error": "customer not found"}
    products = {p["id"]: p for p in all_products()}
    purchase_names = []
    for event in customer_events(customer_id, "purchase"):
        product = products.get(event["product_id"])
        if product:
            purchase_names.append(product["name"])
    return {
        "customer_id": customer["id"],
        "preferred_categories": customer["preferred_categories"],
        "recent_interest": [e["product_id"] for e in customer_events(customer_id, "view")[:5]],
        "average_order_value": customer["avg_order_value"],
        "purchase_history": purchase_names,
        "recommendation_notes": [
            f"Prioritize {', '.join(customer['preferred_categories'])} products.",
            "Use recent viewed categories as a relevance signal.",
            "Keep recommendations within the customer's typical order-value range when possible."
        ]
    }

def aggregate_business_insights() -> dict:
    customers = all_customers()
    categories = Counter()
    for c in customers:
        categories.update(c["preferred_categories"])
    return {
        "customers_analyzed": len(customers),
        "top_interest_categories": categories.most_common(),
        "average_order_value": round(sum(c["avg_order_value"] for c in customers) / len(customers), 2) if customers else 0
    }
