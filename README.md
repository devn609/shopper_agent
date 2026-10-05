# Ecommerce Personal Shopper AI Agent

Portfolio-grade Agentic AI application for conversational product discovery, semantic-style recommendation ranking, business-signal dynamic pricing, and customer insights.

## Architecture

User -> FastAPI -> LangGraph Shopper Agent -> tools:

- Product Search / Recommendation
- Customer Profile
- Dynamic Pricing
- Aggregate Customer Insights

The LLM orchestrates tools; deterministic Python code owns recommendation scoring and pricing constraints. Pricing uses inventory, demand, and competitor price only—not customer identity or sensitive attributes.

## Sqlite Data

SQLite tables

- products
- customers
- customer_events

CSV import
Run:

```bash
python scripts/import_csv.py
```

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# add OPENAI_API_KEY to .env for agentic mode
uvicorn app.main:app --reload
```

API docs: http://127.0.0.1:8000/docs

Example:

```bash
curl -X POST http://127.0.0.1:8000/api/shop -H 'Content-Type: application/json' -d '{"customer_id":"c001","message":"I need road running shoes under $150. Show me the best options."}'
```

## Production extensions

- PostgreSQL + pgvector for large catalogs
- Redis for caching
- Kafka for click/cart/order events
- Feature store for recommendation features
- Offline ranking metrics and A/B tests
- LangSmith/OpenTelemetry tracing
- Authentication and RBAC
- Human approval for pricing-policy changes
