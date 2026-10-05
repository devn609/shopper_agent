from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from .config import OPENAI_API_KEY, OPENAI_MODEL
from .tools import search_products, get_product_price, get_customer_profile, get_customer_insights
TOOLS=[search_products,get_product_price,get_customer_profile,get_customer_insights]
SYSTEM="""You are an ecommerce personal shopper agent. Understand intent, retrieve products, rank options, and explain recommendations. Use customer profile only for recommendation relevance. Use the pricing tool for current prices. Never invent product facts or customer facts. Pricing is based only on inventory, demand, and competitor signals, never personal identity or sensitive traits. Use business insights for aggregate merchandising questions. For recommendations, call tools before answering and provide a concise ranked list with current price and rationale."""
class State(TypedDict):
    messages: Annotated[list[BaseMessage], lambda a,b:a+b]
def build_agent():
    if not OPENAI_API_KEY: return None
    model=ChatOpenAI(model=OPENAI_MODEL,temperature=0).bind_tools(TOOLS)
    tools=ToolNode(TOOLS)
    def call(state): return {"messages":[model.invoke([SystemMessage(content=SYSTEM)]+state["messages"])]}
    def route(state): return "tools" if getattr(state["messages"][-1],"tool_calls",None) else END
    g=StateGraph(State); g.add_node("agent",call); g.add_node("tools",tools); g.add_edge(START,"agent"); g.add_conditional_edges("agent",route,{"tools":"tools",END:END}); g.add_edge("tools","agent")
    return g.compile()
AGENT=build_agent()
def shop(message, customer_id=None):
    if AGENT is None:
        products=search_products.invoke({"query":message,"customer_id":customer_id})
        return {"answer":"Configure OPENAI_API_KEY for agentic responses. Deterministic recommendations are shown below.","products":products,"mode":"fallback"}
    prompt=f"Customer ID: {customer_id}\nShopper request: {message}" if customer_id else message
    result=AGENT.invoke({"messages":[HumanMessage(content=prompt)]})
    return {"answer":result["messages"][-1].content,"mode":"agentic"}
