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
        # Display user message
        with message_container.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with message_container.chat_message("assistant"):
            with st.spinner(TEXT_CONTENT["thinking_message"]):
                # Format conversation history for context (BEFORE adding current message)
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
        
        # Add BOTH user message and assistant response to chat history AFTER getting response
        add_message("user", prompt)
        add_message("assistant", full_response)

def show_agent_memory_log():
    """Show the agent's current memory in an expandable debug section."""
    from .session_manager import get_conversation_history
    
    with st.expander("🔍 Agent Memory Debug Log", expanded=False):
        st.subheader("Current Session State")
        
        # Show current messages count
        message_count = len(st.session_state.messages)
        st.metric("Total Messages", message_count)
        
        # Show conversation history
        conversation_history = get_conversation_history()
        st.subheader("Conversation History (sent to agent)")
        if conversation_history:
            st.text_area(
                "Formatted History:", 
                conversation_history, 
                height=200,
                disabled=True,
                key="debug_history"
            )
        else:
            st.info("No conversation history yet")
        
        # Show current system prompt
        st.subheader("Base System Prompt")
        st.text_area(
            "Current Prompt:", 
            st.session_state.current_prompt, 
            height=150,
            disabled=True,
            key="debug_prompt"
        )
        
        # Show what would be sent to agent for next message
        if conversation_history:
            full_system_prompt = f"{st.session_state.current_prompt}\n\nPrevious conversation:\n{conversation_history}"
            st.subheader("Full System Prompt (next agent call)")
            st.text_area(
                "Complete Prompt:", 
                full_system_prompt, 
                height=300,
                disabled=True,
                key="debug_full_prompt"
            )
        
        # Show model settings
        st.subheader("Model Settings")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Model", st.session_state.model_name)
        with col2:
            st.metric("Temperature", st.session_state.temperature)
        with col3:
            st.metric("Web Search", st.session_state.enable_web_search)

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