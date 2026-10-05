from dataclasses import dataclass
@dataclass
class PricePolicy:
    min_multiplier: float = 0.85
    max_multiplier: float = 1.15

def calculate_dynamic_price(product, policy=None):
    # Business signals only; never use customer identity or sensitive traits for price.
    policy = policy or PricePolicy()
    inventory = product["inventory"]
    demand = product["demand_index"]
    base = product["price"]
    competitor = product["competitor_price"]
    inventory_factor = 1.08 if inventory <= 10 else 1.03 if inventory <= 25 else 0.98
    demand_factor = 1.0 + (demand - 0.5) * 0.10
    competitor_factor = max(0.96, min(1.04, competitor / base))
    raw = inventory_factor * demand_factor * competitor_factor
    multiplier = max(policy.min_multiplier, min(policy.max_multiplier, raw))
    return {"product_id": product["id"], "base_price": base, "dynamic_price": round(base * multiplier, 2),
            "multiplier": round(multiplier, 4), "inventory_factor": inventory_factor,
            "demand_factor": round(demand_factor, 4), "competitor_factor": round(competitor_factor, 4),
            "pricing_basis": ["inventory", "demand_index", "competitor_price"]}
