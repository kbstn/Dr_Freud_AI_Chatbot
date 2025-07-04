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

@st.cache_resource(hash_funcs={Agent: lambda _: None}, show_spinner=TEXT_CONTENT["agent_init_message"])
@st.cache_resource(ttl=CACHE_CONFIG["agent_ttl"])
def _create_base_agent(model_name, temperature, enable_web_search):
    """Internal function to create and cache the base agent (without system prompt)."""
    try:
        # Initialize model with settings
        model = OpenAIResponsesModel(model_name)
        model_settings = OpenAIResponsesModelSettings(
            temperature=temperature,
            max_tokens=DEFAULT_MODEL_SETTINGS["max_tokens"]
        )
        
        # Create base agent structure without system prompt
        agent_data = {
            "model": model,
            "model_settings": model_settings,
            "enable_web_search": enable_web_search
        }
        
        return agent_data
    except Exception as e:
        st.error(f"Error initializing agent: {str(e)}")
        return None

def get_agent(model_name, temperature, enable_web_search, full_system_prompt):
    """Get the AI agent with current settings and full system prompt."""
    # Get cached base agent data
    agent_data = _create_base_agent(model_name, temperature, enable_web_search)
    
    if agent_data is None:
        return None
    
    try:
        # Create agent with full system prompt (including conversation history)
        agent = Agent(
            model=agent_data["model"],
            model_settings=agent_data["model_settings"],
            system_prompt=full_system_prompt
        )
        
        # Add web search if enabled
        if agent_data["enable_web_search"]:
            agent.model.model_settings.openai_builtin_tools = [
                WebSearchToolParam(type='web_search_preview')
            ]
        
        return agent
    except Exception as e:
        st.error(f"Error creating agent with system prompt: {str(e)}")
        return None

def clear_agent_cache():
    """Clear the agent cache to force recreation."""
    _create_base_agent.clear()

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