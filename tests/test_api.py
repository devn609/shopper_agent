from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health(): assert client.get("/health").status_code==200
def test_price(): assert "dynamic_price" in client.get("/api/products/p001/price").json()
def test_insights(): assert client.get("/api/insights").json()["customers_analyzed"]>0
