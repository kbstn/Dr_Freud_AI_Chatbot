"""
CSS styles for Dr. Freud AI Chatbot application.
"""

def get_main_styles():
    """Get the main CSS styles for the application."""
    return """
    <style>
    /* Main app container */
    [data-testid="stAppViewContainer"] > .main {
        background-image: url("files/drfreud_bg.jpeg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* Header and toolbar */
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0) !important;
    }
    
    [data-testid="stToolbar"] {
        right: 1rem;
        top: 0.5rem;
    }

    /* Chat container */
    .stChatMessageContainer {
        background-color: rgba(30, 30, 30, 0.9);
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 100px;
    }

    /* Message bubbles */
    [data-testid="stChatMessage"] {
        background-color: #2D2D2D;
        color: #F0F0F0;
        border-radius: 10px;
        padding: 0.8rem 1.2rem;
        margin: 0.5rem 0;
        border: 1px solid #444444;
    }

    [data-testid="stChatMessage"][data-message-author-role="user"] {
        background-color: #3A3A3A;
    }

    [data-testid="stChatMessage"][data-message-author-role="assistant"] {
        background-color: #2D2D2D;
    }

    /* Input area */
    .stChatFloatingInputContainer {
        bottom: 20px;
        background: rgba(30, 30, 30, 0.9);
        padding: 1rem;
        border-radius: 10px;
    }

    .stChatInputContainer > div > div > div > div > div > div > div > div > div > textarea {
        background-color: #3A3A3A !important;
        color: #FFFFFF !important;
        border-radius: 20px !important;
        padding: 1rem !important;
        border: 1px solid #444444 !important;
    }

    .stChatInputContainer > div > div > div > div > div > div > div > div > div > textarea::placeholder {
        color: #AAAAAA !important;
    }

    /* Typography */
    .stMarkdown p, .stMarkdown ul, .stMarkdown ol, .stMarkdown li {
        color: #F0F0F0 !important;
    }

    /* Mobile styles */
    @media (max-width: 768px) {
        .stChatFloatingInputContainer {
            width: 95% !important;
            left: 2.5% !important;
            right: auto !important;
            transform: none !important;
        }
        
        .main .block-container {
            padding: 0.5rem 0.5rem 120px 0.5rem;
        }
        
        h1 {
            font-size: 1.5rem !important;
            margin: 0.5rem 0 !important;
            text-align: center;
            color: #FFFFFF;
        }
        
        /* Style the chat input */
        .stTextInput > div > div > input {
            color: #FFFFFF !important;
            background-color: #3A3A3A !important;
            border: 1px solid #444444 !important;
        }
        
        /* Style the placeholder text */
        .stTextInput > div > div > input::placeholder {
            color: #AAAAAA !important;
        }
        
        /* Hide header images on mobile to save space */
        @media (max-width: 768px) {
            div[data-testid="stHorizontalBlock"] div[data-testid="stImage"] {
                display: none;
            }
        }
    }
    </style>
    """

def get_header_visibility_styles():
    """Get CSS styles for hiding the Streamlit header."""
    return """
    <style>
        .block-container {
            padding-top: 1rem;
        }
        header {
            visibility: hidden;
        }
    </style>
    """

def get_apply_button_styles():
    """Get CSS styles for the apply button in the prompt editor."""
    return """
    <style>
    .apply-button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
        border: none;
        width: 100%;
    }
    .apply-button:hover {
        background-color: #45a049;
    }
    </style>
    """