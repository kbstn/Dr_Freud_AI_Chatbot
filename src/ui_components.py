"""
UI components for Dr. Freud AI Chatbot.
Contains reusable UI elements and layouts.
"""

import streamlit as st
from .config import AVAILABLE_MODELS, DEFAULT_MODEL_SETTINGS, UI_CONFIG, TEXT_CONTENT
from .session_manager import add_message, get_conversation_history
from .agent_manager import get_agent, get_agent_response

def show_settings():
    """Show settings in the sidebar and return the values."""
    st.sidebar.title(TEXT_CONTENT["settings_title"])
    
    model_name = st.sidebar.selectbox(
        "Choose a model",
        AVAILABLE_MODELS,
        index=0
    )
    
    temperature = st.sidebar.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=DEFAULT_MODEL_SETTINGS["temperature"],
        step=0.1,
        help="Higher values make output more random, lower values more deterministic"
    )
    
    enable_web_search = st.sidebar.toggle(
        "Enable Web Search", 
        value=DEFAULT_MODEL_SETTINGS["enable_web_search"]
    )
    
    return model_name, temperature, enable_web_search

def show_header():
    """Show the application header with images and title."""
    headercol1, headercol2, headercol3 = st.columns([1, 5, 1])
    
    with headercol1:
        st.image(UI_CONFIG["header_images"]["left"], width=UI_CONFIG["image_width"])
    
    with headercol2:
        st.markdown(f"""
        <h1 style='text-align: center;'>{TEXT_CONTENT["app_title"]}</h1>
        """, unsafe_allow_html=True)
    
    with headercol3:
        st.image(UI_CONFIG["header_images"]["right"], width=UI_CONFIG["image_width"])

def show_chat_interface():
    """Show the main chat interface with a fixed layout."""
    # Display chat messages from history
    message_container = st.container(height=UI_CONFIG["chat_container_height"])
    
    # Show chat history
    for message in st.session_state.messages:
        with message_container.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input(TEXT_CONTENT["chat_placeholder"]):
        # Add user message to chat history
        add_message("user", prompt)
        
        # Display user message
        with message_container.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with message_container.chat_message("assistant"):
            with st.spinner(TEXT_CONTENT["thinking_message"]):
                # Format conversation history for context
                conversation_history = get_conversation_history()
                
                # Get agent with full system prompt (including conversation history)
                agent = get_agent(
                    st.session_state.model_name,
                    st.session_state.temperature,
                    st.session_state.enable_web_search,
                    f"{st.session_state.current_prompt}\n\nPrevious conversation:\n{conversation_history}"
                )
                
                # Get response
                full_response = get_agent_response(agent, prompt)
                st.markdown(full_response)
        
        # Add assistant response to chat history
        add_message("assistant", full_response)

def show_header_toggle():
    """Show the header visibility toggle control."""
    st.write("\n")  # Add some space
    show_header = st.radio(
        "Show Streamlit Header",
        ["No", "Yes"],
        index=0,  # Default to "No"
        horizontal=True,
        key="header_toggle"
    )
    return show_header == "Yes"