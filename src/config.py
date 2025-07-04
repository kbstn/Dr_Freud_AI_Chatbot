"""
Configuration module for Dr. Freud AI Chatbot.
Contains all application constants and default settings.
"""

# Page Configuration
PAGE_CONFIG = {
    "page_title": "Dr. Freud der komische Vogel 🦜",
    "page_icon": "🧠",
    "layout": "wide",
    "initial_sidebar_state": "collapsed"
}

# Model Configuration
DEFAULT_MODEL_SETTINGS = {
    "model_name": "gpt-4o-mini",
    "temperature": 0.35,
    "max_tokens": 1000,
    "enable_web_search": False
}

# Available Models
AVAILABLE_MODELS = [
    "gpt-4o-mini",
    "gpt-4.1-nano", 
    "gpt-4o",
    "gpt-4-turbo",
    "gpt-3.5-turbo"
]

# UI Configuration
UI_CONFIG = {
    "chat_container_height": 500,
    "prompt_editor_height": 350,
    "header_images": {
        "left": "files/drfreud.png",
        "right": "files/drfreud2.png",
        "background": "files/drfreud_bg.jpeg"
    },
    "image_width": 200
}

# Text Content
TEXT_CONTENT = {
    "app_title": "Besprechen Sie das bitte mit Dr. Freud!",
    "chat_placeholder": "Stören Sie Dr. Freud beim Nachdenken!",
    "thinking_message": "Dr. Freud denkt nach...",
    "psyche_title": "🧠 Dr. Freuds Psyche",
    "editor_subtitle": "Hier können Sie Einfluss auf Dr. Freuds Persönlichkeit nehmen",
    "settings_title": "⚙️ Settings",
    "personality_updated": "Dr. Freud's personality has been updated. The conversation is reset.",
    "agent_init_message": "Initializing Dr. Freud's brain..."
}

# Cache Configuration
CACHE_CONFIG = {
    "agent_ttl": 3600  # 1 hour in seconds
}

# File Paths
PATHS = {
    "presets_dir": "presets",
    "assets_dir": "files"
}