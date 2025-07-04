"""
Dr. Freud AI Chatbot - Main Application
A Streamlit-based AI chatbot that simulates conversations with Dr. Sigmund Freud 
in a post-apocalyptic setting.
"""

import streamlit as st
import os
from dotenv import load_dotenv
import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent))

# Local imports
from src.config import PAGE_CONFIG, TEXT_CONTENT
from src.styles import get_main_styles, get_header_visibility_styles
from src.session_manager import (
    initialize_session_state, 
    update_model_settings, 
    update_prompt
)
from src.ui_components import (
    show_settings, 
    show_header, 
    show_chat_interface, 
    show_header_toggle
)
from src.edit_system_prompt import show_prompt_editor

# Load environment variables
load_dotenv()

def main():
    """Main application function."""
    # Set page config first to prevent layout shift
    st.set_page_config(**PAGE_CONFIG)

    # Apply main styles
    st.markdown(get_main_styles(), unsafe_allow_html=True)

    # Initialize session state
    initialize_session_state()

    # Create columns for chat and prompt editor
    col1, col2 = st.columns([2, 1])

    # Settings sidebar
    with st.sidebar:
        model_name, temperature, enable_web_search = show_settings()
        update_model_settings(model_name, temperature, enable_web_search)

    # Main chat interface
    with col1:
        show_header()
        show_chat_interface()

    # Prompt editor sidebar
    with col2:
        st.title(TEXT_CONTENT["psyche_title"])
        
        # Get the updated prompt from the editor
        updated_prompt = show_prompt_editor()
        
        # Update the current prompt and handle changes
        if update_prompt(updated_prompt):
            st.toast(TEXT_CONTENT["personality_updated"])
            st.rerun()
        
        # Header visibility toggle
        show_header_flag = show_header_toggle()
        
        # Apply header visibility styles
        if not show_header_flag:
            st.markdown(get_header_visibility_styles(), unsafe_allow_html=True)

if __name__ == "__main__":
    main()