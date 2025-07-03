#!/bin/bash

# Exit on error
set -e

# Set project directory
PROJECT_DIR="/opt/containers/Dr_Freud_AI_Chatbot"

# Create directory if it doesn't exist
sudo mkdir -p /opt/containers

# Navigate to containers directory
cd /opt/containers/

# Remove existing directory if it exists
if [ -d "$PROJECT_DIR" ]; then
    echo "Removing existing project directory..."
    sudo rm -rf "$PROJECT_DIR"
fi

# Clone the repository
echo "Cloning repository..."
sudo git clone https://github.com/kbstn/Dr_Freud_AI_Chatbot.git

# Navigate to project directory
cd "$PROJECT_DIR"

# Copy .env.example to .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from example..."
    sudo cp .env.example .env
    
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
    sudo sh -c "cat > .env << EOL
# Application settings
STREAMLIT_SERVER_PORT=$PORT
STREAMLIT_SERVER_ADDRESS=$ADDRESS
OPENAI_API_KEY=$OPENAI_API_KEY

# Traefik settings - update with your domain for deploying it in traefik environment
TRAEFIK_HOST=$TRAEFIK_HOST
EOL"
    
    echo ".env file has been configured with your settings."
fi

# Make sure the script has execute permissions
chmod +x deploy.sh

# Build and start the containers
echo "Starting Docker Compose..."
sudo docker compose up -d --build

echo -e "\nContainer is starting up..."
echo "Dr. Freud AI Chatbot will be available at http://localhost:$PORT"

# Show logs
echo -e "\nShowing logs (press Ctrl+C to exit):"
sudo docker compose logs -f
