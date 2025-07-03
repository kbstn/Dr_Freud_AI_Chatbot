# app.py
import streamlit as st
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIResponsesModel, OpenAIResponsesModelSettings
from openai.types.responses import WebSearchToolParam
import os
from dotenv import load_dotenv

import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent))

# Local imports
from src.prompts import SYSTEM_PROMPT

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="AI Assistant 🤖",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for settings
with st.sidebar:
    st.title("⚙️ Settings")
    model_name = st.selectbox(
        "Choose a model",
        ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
        index=0
    )
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Higher values make output more random, lower values more deterministic"
    )
    enable_web_search = st.toggle("Enable Web Search", value=False)

# Initialize the agent
@st.cache_resource
def get_agent(model_name, temperature, enable_web_search):
    # Print the system prompt for debugging
    print("\n=== SYSTEM PROMPT ===")
    print(SYSTEM_PROMPT)
    print("==================\n")
    
    # Initialize model
    model = OpenAIResponsesModel(model_name)
    
    # Create model settings with temperature
    model_settings = OpenAIResponsesModelSettings(temperature=temperature)
    
    # Initialize agent with model, settings, and system prompt
    agent = Agent(
        model=model,
        model_settings=model_settings,
        system_prompt=SYSTEM_PROMPT
    )
    
    # Enable web search if needed
    if enable_web_search:
        agent.model.model_settings.openai_builtin_tools = [
            WebSearchToolParam(type='web_search_preview')
        ]
    
    return agent

# Main chat interface
st.title("🤖 Dr. Freud")
st.caption("Powered by pydantic-ai and Streamlit")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What's on your mind?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Get agent instance
        agent = get_agent(model_name, temperature, enable_web_search)
        
        # Get response
        response = agent.run_sync(prompt)
        
        # Display response
        message_placeholder.markdown(response.output)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.output})