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
# Add this import at the top with other imports
from src.edit_system_prompt import show_prompt_editor

# Load environment variables
load_dotenv()



def show_settings():
    """Show settings in the sidebar and return the values"""
    st.sidebar.title("⚙️ Settings")
    model_name = st.sidebar.selectbox(
        "Choose a model",
        ["gpt-4.1-nano", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-4o-mini"],
        index=0
    )
    temperature = st.sidebar.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Higher values make output more random, lower values more deterministic"
    )
    enable_web_search = st.sidebar.toggle("Enable Web Search", value=False)
    return model_name, temperature, enable_web_search

def show_chat_interface():
    """Show the main chat interface"""
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Wer stört mich bei der Arbeit?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get agent response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Get agent instance
            agent = get_agent(
                st.session_state.model_name,
                st.session_state.temperature,
                st.session_state.enable_web_search,
                st.session_state.current_prompt
            )
            
            # Get response
            response = agent.run_sync(prompt)
            # Handle different response formats
            if hasattr(response, 'output'):
                full_response = response.output
            elif hasattr(response, 'content'):
                full_response = response.content
            else:
                full_response = str(response)
            
            # Display response
            message_placeholder.markdown(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Initialize the agent
@st.cache_resource
def get_agent(model_name, temperature, enable_web_search, system_prompt):
    print("\n=== SYSTEM PROMPT ===")
    print(system_prompt)
    print("==================\n")
    
    # Initialize model
    model = OpenAIResponsesModel(model_name)
    
    # Create model settings with temperature
    model_settings = OpenAIResponsesModelSettings(temperature=temperature)
    
    # Initialize agent with model, settings, and system prompt
    agent = Agent(
        model=model,
        model_settings=model_settings,
        system_prompt=system_prompt
    )
    
    # Enable web search if needed
    if enable_web_search:
        agent.model.model_settings.openai_builtin_tools = [
            WebSearchToolParam(type='web_search_preview')
        ]
    
    return agent

def main():
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "model_name" not in st.session_state:
        st.session_state.model_name = "gpt-4o-mini"
    if "temperature" not in st.session_state:
        st.session_state.temperature = 0.7
    if "enable_web_search" not in st.session_state:
        st.session_state.enable_web_search = False
    if "current_prompt" not in st.session_state:
        st.session_state.current_prompt = SYSTEM_PROMPT

    # Set page config
    st.set_page_config(
        page_title="Dr. Freud der komische Vogel 🦜",
        page_icon="🦜",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Create columns for chat and prompt editor
    col1, col2 = st.columns([2, 1])

    with st.sidebar:
        # hide sidebar when loading page
        
        # Show settings
        model_name, temperature, enable_web_search = show_settings()
        
        # Update session state
        st.session_state.model_name = model_name
        st.session_state.temperature = temperature
        st.session_state.enable_web_search = enable_web_search

    with col1:

        headercol1, headercol2, headercol3 = st.columns([1,5,1])
        with headercol1:
            st.image("files/drfreud.png", width=200)
        with headercol2:
            
            st.markdown("""
        <h1 style='text-align: center;'>    Besprechen Sie das bitte mit Dr. Freud!</h1>
    """, unsafe_allow_html=True)
        with headercol3:
            st.image("files/drfreud2.png", width=200)
        show_chat_interface()

    with col2:
        # Show prompt editor
        st.title("🧠 Dr. Freuds Psyche")
        st.session_state.current_prompt = show_prompt_editor(st.session_state.current_prompt)

if __name__ == "__main__":
    main()