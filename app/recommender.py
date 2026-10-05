import re
from .data import all_products, get_customer
from .pricing import calculate_dynamic_price
def _tokens(s): return set(re.findall(r"[a-z0-9]+", s.lower()))
def recommend(query, customer_id=None, limit=5):
    q = _tokens(query); customer = get_customer(customer_id)
    preferred = set(customer["preferred_categories"]) if customer else set()
    scored = []
    for p in all_products():
        tags = set(p["tags"]) | {p["category"], p["name"].lower()}
        score = len(q & tags) * 3 + (2 if p["category"] in preferred else 0) + p["rating"]
        scored.append((score, p))
    scored.sort(key=lambda x: x[0], reverse=True)
    out=[]
    for score,p in scored[:limit]:
        pr=calculate_dynamic_price(p)
        out.append({**p,"recommendation_score":round(score,2),"current_price":pr["dynamic_price"],
                    "price_change_pct":round((pr["dynamic_price"]/p["price"]-1)*100,2)})
    return out
