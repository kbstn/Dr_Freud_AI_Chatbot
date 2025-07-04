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

# Cache only the base agent (without conversation history)
@st.cache_resource(ttl=CACHE_CONFIG["agent_ttl"], show_spinner=TEXT_CONTENT["agent_init_message"])
def _get_base_agent(model_name, temperature, enable_web_search):
    """Create and cache base agent without conversation history."""
    try:
        # Initialize model with settings
        model = OpenAIResponsesModel(model_name)
        model_settings = OpenAIResponsesModelSettings(
            temperature=temperature,
            max_tokens=DEFAULT_MODEL_SETTINGS["max_tokens"]
        )
        
        # Initialize base agent without system prompt
        agent = Agent(
            model=model,
            model_settings=model_settings,
            system_prompt="You are a helpful assistant."  # Temporary prompt
        )
        
        # Add web search if enabled
        if enable_web_search:
            agent.model.model_settings.openai_builtin_tools = [
                WebSearchToolParam(type='web_search_preview')
            ]
        
        return agent
    except Exception as e:
        st.error(f"Error initializing base agent: {str(e)}")
        return None

def get_agent_with_context(model_name, temperature, enable_web_search, base_prompt, conversation_history=""):
    """Get agent and run with conversation context."""
    # Get cached base agent
    base_agent = _get_base_agent(model_name, temperature, enable_web_search)
    
    if base_agent is None:
        return None
    
    # Create full context for this specific request
    if conversation_history.strip():
        full_context = f"{base_prompt}\n\nPrevious conversation:\n{conversation_history}"
    else:
        full_context = base_prompt
    
    print(f"[DEBUG] Agent context hash: {hash(full_context)}")
    print(f"[DEBUG] Context ends with: ...{full_context[-100:]}")
    
    return base_agent, full_context

def clear_agent_cache():
    """Clear the agent cache to force recreation."""
    _get_base_agent.clear()

def get_agent_response_with_context(model_name, temperature, enable_web_search, base_prompt, user_prompt, conversation_history=""):
    """Get response from agent with conversation context."""
    try:
        # Get agent and context
        agent, full_context = get_agent_with_context(model_name, temperature, enable_web_search, base_prompt, conversation_history)
        
        if agent is None:
            return "Entschuldigung, ich kann im Moment nicht antworten."
        
        # Create a new agent instance with the full context as system prompt
        # This ensures the conversation history is properly included
        agent_with_context = Agent(
            model=agent.model,
            model_settings=agent.model_settings,
            system_prompt=full_context
        )
        
        # Add web search if enabled
        if enable_web_search:
            agent_with_context.model.model_settings.openai_builtin_tools = [
                WebSearchToolParam(type='web_search_preview')
            ]
        
        print(f"[DEBUG] Sending prompt to agent: '{user_prompt}'")
        response = agent_with_context.run_sync(user_prompt)
        
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

# Legacy function for backward compatibility
def get_agent_response(agent, prompt):
    """Legacy function for backward compatibility."""
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