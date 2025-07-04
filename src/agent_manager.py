"""
Agent management for Dr. Freud AI Chatbot.
Handles Pydantic AI agent creation and caching.
"""

import streamlit as st
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIResponsesModel, OpenAIResponsesModelSettings
from openai.types.responses import WebSearchToolParam
from .config import DEFAULT_MODEL_SETTINGS, CACHE_CONFIG, TEXT_CONTENT

# Global cache for agent - will be cleared when needed
_agent_cache = {}

@st.cache_resource(ttl=CACHE_CONFIG["agent_ttl"], show_spinner=TEXT_CONTENT["agent_init_message"])
def get_agent(model_name, temperature, enable_web_search, system_prompt):
    """Initializes and returns the Pydantic-AI Agent with current settings."""
    # Debug: Print system prompt info for troubleshooting
    print(f"[DEBUG] Creating agent with system prompt hash: {hash(system_prompt)}")
    print(f"[DEBUG] System prompt ends with: ...{system_prompt[-100:]}")
    
    try:
        # Initialize model with settings
        model = OpenAIResponsesModel(model_name)
        model_settings = OpenAIResponsesModelSettings(
            temperature=temperature,
            max_tokens=DEFAULT_MODEL_SETTINGS["max_tokens"]
        )
        
        # Initialize agent
        agent = Agent(
            model=model,
            model_settings=model_settings,
            system_prompt=system_prompt
        )
        
        # Add web search if enabled
        if enable_web_search:
            agent.model.model_settings.openai_builtin_tools = [
                WebSearchToolParam(type='web_search_preview')
            ]
        
        return agent
    except Exception as e:
        st.error(f"Error initializing agent: {str(e)}")
        return None

def clear_agent_cache():
    """Clear the agent cache to force recreation."""
    get_agent.clear()

def get_agent_response(agent, prompt):
    """Get response from the agent and handle different response formats."""
    try:
        response = agent.run_sync(prompt)
        
        # Handle different response formats
        if hasattr(response, 'output'):
            return response.output
        elif hasattr(response, 'content'):
            return response.content
        else:
            return str(response)
    except Exception as e:
        st.error(f"Error getting agent response: {str(e)}")
        return "Entschuldigung, ich kann im Moment nicht antworten."