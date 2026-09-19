import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from agent import TravelAgent

def get_text(content):
    if isinstance(content, list):
        return "".join([block.get("text", "") for block in content if isinstance(block, dict) and block.get("type") == "text"])
    return str(content)

st.set_page_config(page_title="Singapore AI Travel Planning Assistant", page_icon="✈️", layout="wide")

st.title("🇸🇬 AI Travel Planning Assistant (Singapore)")
st.caption("RAG Destination Knowledge Base + Real-time MCP Weather & Currency Tools")

if "agent" not in st.session_state:
    st.session_state.agent = TravelAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Assignment Test Scenarios")
    
    st.subheader("1. Core RAG Destination Queries")
    if st.button("Must-visit Attractions"):
        st.session_state.user_prompt = "What are the must-visit attractions in Singapore?"
    if st.button("Cultural Enclaves"):
        st.session_state.user_prompt = "Which neighbourhoods are suitable for cultural experiences and how do I travel between them?"
    if st.button("Family with Children"):
        st.session_state.user_prompt = "Suggest activities for a family with children."
    if st.button("Food & Local Experiences"):
        st.session_state.user_prompt = "What are the must-try local dishes and food centres in Singapore?"
    if st.button("Indoor Attractions"):
        st.session_state.user_prompt = "What indoor attractions can I visit to avoid rain or heat?"

    st.subheader("2. Standalone MCP Tools")
    if st.button("Check Weather"):
        st.session_state.user_prompt = "What is the weather forecast for the next 3 days in Singapore?"
    if st.button("Convert Currency (50k INR)"):
        st.session_state.user_prompt = "Convert INR 50,000 to SGD."

    st.subheader("3. Combined RAG + MCP Scenarios")
    if st.button("Required 3-Day Weather Itinerary"):
        st.session_state.user_prompt = "Create a three-day trip to Singapore and adjust the activities based on the weather forecast."
    if st.button("Bonus: Budget + Family Trip"):
        st.session_state.user_prompt = "I have a budget of INR 60,000. Convert it to SGD, and suggest a 3-day family itinerary adjusted for the weather forecast."

    st.subheader("4. Unknown/Out-of-Scope Handling")
    if st.button("Out of Scope Query"):
        st.session_state.user_prompt = "What are the best ski resorts in Singapore?"

    st.divider()
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(get_text(msg.content))
    elif isinstance(msg, AIMessage) and msg.content:
        with st.chat_message("assistant"):
            st.markdown(get_text(msg.content))

active_input = st.chat_input("Ask a travel question or plan an itinerary...")
if "user_prompt" in st.session_state and st.session_state.user_prompt:
    active_input = st.session_state.user_prompt
    st.session_state.user_prompt = None

if active_input:
    with st.chat_message("user"):
        st.markdown(active_input)
    st.session_state.messages.append(HumanMessage(content=active_input))

    with st.chat_message("assistant"):
        with st.spinner("Retrieving knowledge base and querying MCP tools..."):
            answer, updated_history = st.session_state.agent.run_conversation(st.session_state.messages)
            st.markdown(get_text(answer))
            st.session_state.messages = updated_history
