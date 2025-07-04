#!/bin/bash

# Exit on error
set -e

# Work in the current directory (where the script is run from)
echo "Working in current directory: $(pwd)"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: This script must be run from the Dr_Freud_AI_Chatbot git repository"
    echo "Please cd to your repository directory and run the script"
    exit 1
fi

# Pull latest changes instead of cloning
echo "📥 Pulling latest changes..."
git fetch origin
git reset --hard origin/main

echo "📁 Files in directory:"
ls -la

# Copy .env.example to .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    
    # Set default values from .env.example if they exist
    DEFAULT_PORT=$(grep -E '^STREAMLIT_SERVER_PORT=' .env.example | cut -d '=' -f2- || echo "8501")
    DEFAULT_ADDRESS=$(grep -E '^STREAMLIT_SERVER_ADDRESS=' .env.example | cut -d '=' -f2- || echo "0.0.0.0")
    DEFAULT_TRAEFIK_HOST=$(grep -E '^TRAEFIK_HOST=' .env.example | cut -d '=' -f2- || echo "your-domain.com")
    DEFAULT_OPENAI_API_KEY=$(grep -E '^OPENAI_API_KEY=' .env.example | cut -d '=' -f2- || echo "your-openai-api-key")
    
    # Prompt user for values
    read -p "Enter Streamlit server port [$DEFAULT_PORT]: " PORT
    PORT=${PORT:-$DEFAULT_PORT}
    
    read -p "Enter Streamlit server address [$DEFAULT_ADDRESS]: " ADDRESS
    ADDRESS=${ADDRESS:-$DEFAULT_ADDRESS}
    
    read -p "Enter Traefik host [$DEFAULT_TRAEFIK_HOST]: " TRAEFIK_HOST
    TRAEFIK_HOST=${TRAEFIK_HOST:-$DEFAULT_TRAEFIK_HOST}
    
    read -p "Enter your OpenAI API key [$DEFAULT_OPENAI_API_KEY]: " OPENAI_API_KEY
    OPENAI_API_KEY=${OPENAI_API_KEY:-$DEFAULT_OPENAI_API_KEY}
    
    # Update .env file with user values
    cat > .env << EOL
# Application settings
STREAMLIT_SERVER_PORT=$PORT
STREAMLIT_SERVER_ADDRESS=$ADDRESS
OPENAI_API_KEY=$OPENAI_API_KEY

# Traefik settings - update with your domain for deploying it in traefik environment
TRAEFIK_HOST=$TRAEFIK_HOST
EOL
    
    echo ".env file has been configured with your settings."
fi

# Make sure the script has execute permissions
chmod +x deploy.sh

# Build and start the containers
echo "Starting Docker Compose..."
sudo docker compose up -d --build

echo -e "\nContainer is starting up..."
PORT=$(grep STREAMLIT_SERVER_PORT .env | cut -d= -f2 2>/dev/null || echo "8501")
echo "Dr. Freud AI Chatbot will be available at http://localhost:$PORT"

# Show logs
echo -e "\nShowing logs (press Ctrl+C to exit):"
sudo docker compose logs -f
