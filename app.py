# app.py
import streamlit as st
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIResponsesModel, OpenAIResponsesModelSettings
from openai.types.responses import WebSearchToolParam
import os
from dotenv import load_dotenv
import base64
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
        value=0.35,
        step=0.1,
        help="Higher values make output more random, lower values more deterministic"
    )
    enable_web_search = st.sidebar.toggle("Enable Web Search", value=False)
    return model_name, temperature, enable_web_search

def show_chat_interface():
    """Show the main chat interface with a fixed layout."""
    # We use a container with a fixed height to ensure the chat input stays at the bottom.
    message_container = st.container(height=550)

    # Display chat messages from history
    for message in st.session_state.messages:
        with message_container.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Stören Sie Dr. Freud beim Nachdenken!"):
        # Add user message to chat history and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with message_container.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with message_container.chat_message("assistant"):
            with st.spinner("Dr. Freud denkt nach..."):
                agent = get_agent(
                    st.session_state.model_name,
                    st.session_state.temperature,
                    st.session_state.enable_web_search,
                    st.session_state.current_prompt
                )
                response = agent.run_sync(prompt)
                
                # Handle different response formats
                if hasattr(response, 'output'):
                    full_response = response.output
                elif hasattr(response, 'content'):
                    full_response = response.content
                else:
                    full_response = str(response)
                
                st.markdown(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

def get_image_as_base64(path: str) -> str:
    """Reads an image file and returns it as a base64 encoded string."""
    try:
        img_path = Path(path)
        if not img_path.is_file():
            return ""
        with open(img_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception as e:
        print(f"Error reading image {path}: {e}")
        return ""


@st.cache_resource(hash_funcs={Agent: lambda _: None}, show_spinner="Initializing Dr. Freud's brain...")
def get_agent(model_name, temperature, enable_web_search, system_prompt):
    """Initializes and returns the Pydantic-AI Agent based on current settings."""
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
    # Set page config first to prevent layout shift
    st.set_page_config(
        page_title="Dr. Freud der komische Vogel 🦜",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    # Remove invisible Streamlit header
#    st.markdown("""
#    <style>
#        .block-container {
#            padding-top: 1rem;  /* Reduce top padding */
#        }

#        header {
#            visibility: hidden;  /* Optionally hide Streamlit header */
#        }
#    </style>
#""", unsafe_allow_html=True)

    # Prepare CSS for background image
    img_base64 = get_image_as_base64("files/drfreud_bg.jpeg")
    background_image_style = f"""
    background-image: url(data:image/jpeg;base64,{img_base64});
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    """ if img_base64 else ""

    # Inject custom CSS for responsive design
    st.markdown(f"""
    <style>
    /* Base styles for all screen sizes */
    .main .block-container {{
        padding-top: 1rem;
        padding-bottom: 1rem;
        background-color: #1E1E1E;  /* Dark background for the main container */
        color: #FFFFFF;  /* Default text color */
    }}
    
    /* Chat container styles */
    .stChatFloatingInputContainer {{
        position: fixed;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 800px;
        background: #2D2D2D;  /* Darker background for input */
        border-radius: 20px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 999;
    }}
    
    /* Chat message area */
    [data-testid="stChatMessage"] {{
        background-color: #2D2D2D;  /* Dark background for messages */
        color: #FFFFFF;  /* White text */
        border-radius: 10px;
        padding: 0.8rem 1.2rem;
        margin: 0.5rem 0;
        border: 1px solid #444444;
    }}
    
    /* Style for user messages */
    [data-testid="stChatMessage"][data-message-author-role="user"] {{
        background-color: #3A3A3A;  /* Slightly different background for user messages */
    }}
    
    /* Style for assistant messages */
    [data-testid="stChatMessage"][data-message-author-role="assistant"] {{
        background-color: #2D2D2D;  /* Dark background for assistant */
    }}
    
    /* Adjust text color for better contrast */
    .stMarkdown p, .stMarkdown ul, .stMarkdown ol, .stMarkdown li {{
        color: #F0F0F0 !important;
    }}
    
    /* Mobile-specific styles */
    @media (max-width: 768px) {{
        .main .block-container {{
            padding-top: 0.5rem;
            padding-bottom: 120px;
        }}
        
        h1 {{
            font-size: 1.5rem !important;
            margin-top: 0.5rem !important;
            text-align: center;
            color: #FFFFFF;  /* Ensure title is white */
        }}
        
        /* Chat container with background */
        [data-testid="stChatMessageContainer"] {{
            {background_image_style}
            padding: 1rem;
            margin-bottom: 100px;
            background-color: rgba(30, 30, 30, 0.9);  /* Semi-transparent dark background */
        }}
        
        /* Hide header images on mobile to save space */
        div[data-testid="stHorizontalBlock"] div[data-testid="stImage"] {{
            display: none;
        }}
    }}
    
    /* Desktop-specific styles */
    @media (min-width: 769px) {{
        [data-testid="stChatMessageContainer"] {{
            {background_image_style}
            min-height: 60vh;
            padding: 2rem;
            background-color: rgba(30, 30, 30, 0.9);  /* Semi-transparent dark background */
        }}
    }}
    
    /* Style the chat input */
    .stTextInput > div > div > input {{
        color: #FFFFFF !important;
        background-color: #3A3A3A !important;
        border: 1px solid #444444 !important;
    }}
    
    /* Style the placeholder text */
    .stTextInput > div > div > input::placeholder {{
        color: #AAAAAA !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "model_name" not in st.session_state:
        st.session_state.model_name = "gpt-4o-mini"
    if "temperature" not in st.session_state:
        st.session_state.temperature = 0.35
    if "enable_web_search" not in st.session_state:
        st.session_state.enable_web_search = False
    if "current_prompt" not in st.session_state:
        st.session_state.current_prompt = SYSTEM_PROMPT
    if "last_prompt" not in st.session_state:
        st.session_state.last_prompt = st.session_state.current_prompt

    # Create columns for chat and prompt editor
    col1, col2 = st.columns([2, 1])

    with st.sidebar:
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
        
        # Initialize prompt_editor in session state if it doesn't exist
        if 'prompt_editor' not in st.session_state:
            st.session_state.prompt_editor = st.session_state.current_prompt
            
        # Get the updated prompt from the editor
        updated_prompt = show_prompt_editor()
        
        # Update the current prompt only if it's different
        if updated_prompt != st.session_state.current_prompt:
            st.session_state.current_prompt = updated_prompt

            # If the prompt has changed, clear the agent cache and chat history
            if st.session_state.last_prompt != st.session_state.current_prompt:
                get_agent.clear() # Invalidate the cached agent
                st.session_state.messages = []
                st.session_state.last_prompt = st.session_state.current_prompt
                st.toast("Dr. Freud's personality has been updated. The conversation is reset.")
                st.rerun()

if __name__ == "__main__":
    main()