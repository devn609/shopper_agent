from fastapi import FastAPI
from pydantic import BaseModel, Field
from .agent import shop
from .recommender import recommend
from .pricing import calculate_dynamic_price
from .data import get_product
from .insights import customer_insights, aggregate_business_insights
app=FastAPI(title="Ecommerce Shopper AI Agent",version="1.0.0")
class ShopRequest(BaseModel):
    message:str=Field(min_length=2)
    customer_id:str|None=None
@app.get("/health")
def health(): return {"status":"ok"}
@app.post("/api/shop")
def shopping_agent(req:ShopRequest): return shop(req.message,req.customer_id)
@app.get("/api/products/recommend")
def recommendations(query:str,customer_id:str|None=None,limit:int=5): return {"products":recommend(query,customer_id,min(limit,20))}
@app.get("/api/products/{product_id}/price")
def product_price(product_id:str):
    p=get_product(product_id); return calculate_dynamic_price(p) if p else {"error":"product not found"}
@app.get("/api/customers/{customer_id}/insights")
def customer_profile(customer_id:str): return customer_insights(customer_id)
@app.get("/api/insights")
def business_insights(): return aggregate_business_insights()
