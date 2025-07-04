"""
Session state management for Dr. Freud AI Chatbot.
"""

import streamlit as st
from .config import DEFAULT_MODEL_SETTINGS
from .prompts import SYSTEM_PROMPT

def initialize_session_state():
    """Initialize all session state variables with default values."""
    
    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Model settings
    if "model_name" not in st.session_state:
        st.session_state.model_name = DEFAULT_MODEL_SETTINGS["model_name"]
    
    if "temperature" not in st.session_state:
        st.session_state.temperature = DEFAULT_MODEL_SETTINGS["temperature"]
    
    if "enable_web_search" not in st.session_state:
        st.session_state.enable_web_search = DEFAULT_MODEL_SETTINGS["enable_web_search"]
    
    # Prompt management
    if "current_prompt" not in st.session_state:
        st.session_state.current_prompt = SYSTEM_PROMPT
    
    if "last_prompt" not in st.session_state:
        st.session_state.last_prompt = st.session_state.current_prompt
    
    # Prompt editor
    if "prompt_editor" not in st.session_state:
        st.session_state.prompt_editor = st.session_state.current_prompt

def update_model_settings(model_name, temperature, enable_web_search):
    """Update model settings in session state."""
    st.session_state.model_name = model_name
    st.session_state.temperature = temperature
    st.session_state.enable_web_search = enable_web_search

def update_prompt(new_prompt):
    """Update the current prompt and handle related state changes."""
    if new_prompt != st.session_state.current_prompt:
        st.session_state.current_prompt = new_prompt
        
        # If prompt has changed, clear cache and reset conversation
        if st.session_state.last_prompt != st.session_state.current_prompt:
            from .agent_manager import clear_agent_cache
            clear_agent_cache()
            st.session_state.messages = []
            st.session_state.last_prompt = st.session_state.current_prompt
            return True
    return False

def add_message(role, content):
    """Add a message to the chat history."""
    st.session_state.messages.append({"role": role, "content": content})

def get_conversation_history():
    """Get formatted conversation history."""
    return "\n".join(
        f"{msg['role'].capitalize()}: {msg['content']}" 
        for msg in st.session_state.messages
    )

def clear_conversation():
    """Clear the conversation history."""
    st.session_state.messages = []