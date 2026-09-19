import sys
import asyncio
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.messages import SystemMessage, ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

PERSIST_DIR = "./chroma_db"

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2-preview")
vector_store = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 4})

@tool
def search_travel_knowledge_base(query: str) -> str:
    """Searches the destination knowledge base for attractions, food, family activities, transport, culture, and sample itineraries."""
    docs = retriever.invoke(query)
    if not docs:
        return "NO_DATA_FOUND: The knowledge base does not contain sufficient information on this topic."

    results = []
    for doc in docs:
        title = doc.metadata.get("source_title", "Official Singapore Guide")
        url = doc.metadata.get("source_url", "#")
        results.append(f"[Source: {title} | Link: {url}]\n{doc.page_content}")
    return "\n\n".join(results)

SYSTEM_PROMPT = """You are an AI Travel Planning Assistant for Singapore.
Adhere to the following grounding, source attribution, and architectural rules:

1. Destination Facts: Rely on content retrieved from `search_travel_knowledge_base`. Always provide the exact source citation (e.g., `[Source: Title](URL)`) alongside destination facts.
2. Current Information: Use `get_live_weather_forecast` for forecasts and `convert_live_currency` for financial conversions.
3. Explicit Grounding & Sectioning: Every response involving recommendations or combined queries must distinctly separate information into three labeled sections:
   - ### Destination Facts (Knowledge Base)
     (All factual details about Singapore attractions, food, transport, or culture, with citations)
   - ### Current Data (MCP Tools)
     (Live weather metrics, rain chances, or currency conversions retrieved via MCP)
   - ### AI-Generated Recommendations
     (The day-wise synthesized itinerary, indoor/outdoor adjustments, or personalized suggestions)
4. Out-of-Scope & Unknowns: If the knowledge base does not contain enough information to answer a question, state: "The knowledge base does not contain sufficient information on this topic." Do not fabricate destinations or travel policies.
5. Tool Failure: If an MCP tool returns an error, state that current live data is unavailable without fabricating forecasts or conversion rates.
6. Context Retention: Retain previous conversational context (such as traveler preferences, budget amounts, and dates) across turns.
"""

class TravelAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.6-flash",
            temperature=0.2
        )

    async def _run_conversation_async(self, messages: list):
        connections = {
            "travel_mcp": {
                "command": sys.executable,
                "args": ["mcp_server.py"],
                "transport": "stdio"
            }
        }

        client = MultiServerMCPClient(connections)
        mcp_tools = await client.get_tools()
        
        all_tools = [search_travel_knowledge_base] + mcp_tools
        tool_map = {t.name: t for t in all_tools}
        
        agent_llm = self.llm.bind_tools(all_tools)
        convo = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        
        while True:
            response = await agent_llm.ainvoke(convo)
            convo.append(response)

            if not response.tool_calls:
                return response.content, convo[1:]

            for tool_call in response.tool_calls:
                name = tool_call["name"]
                args = tool_call["args"]
                tool_fn = tool_map.get(name)
                
                try:
                    if tool_fn:
                        if name == "search_travel_knowledge_base":
                            tool_output = tool_fn.invoke(args)
                        else:
                            tool_output = await tool_fn.ainvoke(args)
                    else:
                        tool_output = f"Tool {name} not found."
                except Exception as e:
                    tool_output = f"Error executing tool {name}: {str(e)}"
                    
                convo.append(ToolMessage(
                    content=str(tool_output),
                    tool_call_id=tool_call["id"],
                    name=name
                ))

    def run_conversation(self, messages: list):
        return asyncio.run(self._run_conversation_async(messages))
