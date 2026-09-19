# 🇸🇬 AI Travel Planning Assistant (Singapore)

## Overview
This project is a context-aware AI travel planning assistant that seamlessly integrates document-grounded Retrieval-Augmented Generation (RAG) with live Model Context Protocol (MCP) tools. By combining verified, static destination knowledge with real-time weather forecasts and currency exchange rates, the application generates highly customized, weather-adaptive itineraries while strictly guarding against AI hallucinations.

## Architecture
- **Framework:** LangChain and Streamlit
- **Knowledge Base (RAG):** ChromaDB using `gemini-embedding-2-preview` embeddings.
- **LLM:** Google Gemini (`gemini-3.6-flash`).
- **External Tools (MCP):** A standalone MCP Server running Open-Meteo for live weather and Frankfurter for live currency exchange.

## Project Structure
```text
NagpAIAssignment/
├── data/                                    # Raw knowledge base text files
│   ├── wikivoyage_singapore.txt             # Districts, cultural enclaves, and public transit
│   ├── visitsingapore_essentials.txt        # Local laws, climate, drinking water, etiquette
│   ├── visitsingapore_things_to_do.txt      # Hawker culture, family sights, indoor vs outdoor
│   └── visitsingapore_itineraries.txt       # Multi-day sample itineraries and blueprints
├── chroma_db/                               # Persisted ChromaDB vector storage (generated on ingest)
├── mcp_server.py                            # FastMCP server exposing weather and currency tools
├── ingest.py                                # Document chunking, metadata tagging, and vector ingestion
├── agent.py                                 # LangChain orchestrator, MCP client binding, and prompt engine
├── app.py                                   # Streamlit frontend with multi-turn chat and test triggers
├── requirements.txt                         # Application package dependencies
├── SAMPLE_QNA.md                            # Comprehensive audit of queries and application responses
├── .gitignore
└── README.md                                # Project architecture and operational documentation
```

## Knowledge Base Sources
The RAG pipeline relies on chunked data extracted from three public resources:
1. **Wikivoyage Singapore Travel Guide:** Neighborhoods and transportation.
2. **Visit Singapore Essential Travel Information:** Practical guidance, tipping, laws, and connectivity.
3. **Visit Singapore Sample Itineraries & Things to Do:** Food, family activities, and indoor/outdoor attraction categorization.

## Prompt & Context Strategy
To ensure the LLM strictly adheres to facts without hallucinating external information, the application uses a highly structured System Prompt. The prompt strategy includes:
- **Strict Boundary Guardrails:** The LLM is instructed to explicitly refuse questions if the semantic search returns `NO_DATA_FOUND`. 
- **Tool Segregation:** The prompt mandates which tool to use for specific intents (RAG for static facts, MCP for live data).
- **Output Structuring:** The LLM is forced to format its response into three distinct Markdown sections: Destination Facts (requiring source citations), Current Data (tagged as MCP data), and AI Recommendations (for subjective itinerary synthesis).
- **Conversational Memory:** The system passes the entire history of user prompts, AI responses, and intermediate tool executions back to the model on every turn to preserve budget, dates, and preferences.


## Data Licensing & Reuse Terms
In accordance with the assignment requirements, the reuse terms of the knowledge base sources have been reviewed:
*   **Wikivoyage Content:** Distributed under the Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0) license. The source URLs and titles are retained and cited in the app's output to satisfy attribution requirements.
*   **Visit Singapore Content:** The official Visit Singapore portal restricts commercial redistribution of its copyrighted text. For the purpose of this non-commercial academic assignment, limited excerpts have been extracted into plain text to simulate RAG ingestion under Fair Use. All outputs properly cite the official Visit Singapore URLs.

## Setup Instructions

### Prerequisites

Ensure you have Python 3.10+ installed on your Linux machine.

```bash
# 1. clone / unzip, then from the project root:
sudo apt update && sudo apt install -y python3-venv python3-pip git
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 2. install dependencies
pip install -r requirements.txt
```

### Export your LLM's api_key

Export the api_key of your selected LLM model:

```bash
export GOOGLE_API_KEY="your-gemini-api-key-here"
```

### Build the vector database

Initialize and populate the ChromaDB vector store.

```bash
python ingest.py
```

### Run the application

The application will automatically launch the MCP server in the background and connect to it.

```bash
streamlit run app.py
```

## Application Demonstration Script & Workflow

### Step 1: Initialization 
* Run `streamlit run app.py` to launch the application interface.

### Step 2: RAG & Factual Retrieval
* Click the "Family with Children" button in the sidebar.
* The model will show the `Destination Facts` section with direct citations to the Knowledge Base (e.g., S.E.A. Aquarium, Mandai Wildlife Reserve).

### Step 3: MCP Tool Execution
* Click the "Check Weather" button.
* The model successfully routes the query to the independent `mcp_server.py` and returns the `Current Data` section with real-time temperature and rain probabilities without hallucinating.

### Step 4: Combined Scenario & Context
* Click the "Required 3-Day Weather Itinerary" button.
* The model will executes both the knowledge base search and the MCP weather query concurrently. Show how the `AI-Generated Recommendations` section swaps outdoor activities for indoor ones (like the Cloud Forest) on days where the MCP tool indicated a high rain probability.
* Type a follow-up question: *"Change the Day 2 itinerary to focus on food instead."*
* The model remembers it is a 3-day Singapore trip, respects the weather forecast from the previous turn, and retrieves hawker centers (Maxwell, Lau Pa Sat) for Day 2.

### Step 5: Guardrails
* Click the "Out of Scope Query" button.
* The model explicitly refuses to answer rather than hallucinate, fulfilling the strict prompt engineering instructions.

## Github repo link

https://github.com/115Shubham1992/AITravelAssistant

## One drive demo video link

https://nagarro-my.sharepoint.com/my?id=/personal/shubham_vijay_nagarro_com/Documents/NAGPAIAssignment&viewid=d14422e4-1c69-4f65-8b3e-53730d53e468



