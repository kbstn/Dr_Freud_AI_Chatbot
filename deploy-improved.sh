#!/bin/bash

# Dr. Freud AI Chatbot - Improved Deployment Script
# This script preserves user data across deployments

# Exit on error
set -e

# Set project directories
PROJECT_DIR="/opt/containers/Dr_Freud_AI_Chatbot"
DATA_DIR="/opt/containers/Dr_Freud_AI_Chatbot_data"

echo "🧠 Dr. Freud AI Chatbot - Improved Deployment"
echo "============================================="

# Create directories if they don't exist
sudo mkdir -p /opt/containers
sudo mkdir -p "$DATA_DIR"

# Navigate to containers directory
cd /opt/containers/

# Backup existing user data if project exists
if [ -d "$PROJECT_DIR" ]; then
    echo "📦 Backing up user data..."
    
    # Backup presets if they exist
    if [ -d "$PROJECT_DIR/presets" ]; then
        sudo cp -r "$PROJECT_DIR/presets" "$DATA_DIR/" 2>/dev/null || true
        echo "   ✅ Presets backed up"
    fi
    
    # Backup .env file if it exists
    if [ -f "$PROJECT_DIR/.env" ]; then
        sudo cp "$PROJECT_DIR/.env" "$DATA_DIR/" 2>/dev/null || true
        echo "   ✅ Environment config backed up"
    fi
    
    # Stop running containers gracefully
    echo "🛑 Stopping existing containers..."
    cd "$PROJECT_DIR"
    sudo docker compose down 2>/dev/null || true
    cd /opt/containers/
    
    # Remove old project directory
    echo "🗑️  Removing old project files..."
    sudo rm -rf "$PROJECT_DIR"
fi

# Clone the repository
echo "📥 Cloning latest repository..."
sudo git clone https://github.com/kbstn/Dr_Freud_AI_Chatbot.git

# Navigate to project directory
cd "$PROJECT_DIR"

# Restore user data
echo "📂 Restoring user data..."

# Restore .env file
if [ -f "$DATA_DIR/.env" ]; then
    sudo cp "$DATA_DIR/.env" "$PROJECT_DIR/"
    echo "   ✅ Environment config restored"
else
    # Create .env file if it doesn't exist
    echo "⚙️  Setting up environment configuration..."
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
    
    echo "   ✅ .env file configured with your settings"
fi

# Restore presets
if [ -d "$DATA_DIR/presets" ]; then
    sudo cp -r "$DATA_DIR/presets" "$PROJECT_DIR/"
    echo "   ✅ Personality presets restored"
fi

# Set proper permissions
sudo chown -R $(whoami):$(whoami) "$PROJECT_DIR" 2>/dev/null || true

# Make sure the script has execute permissions
chmod +x deploy.sh
chmod +x deploy-improved.sh

# Build and start the containers
echo "🚀 Starting Docker Compose..."
sudo docker compose up -d --build

echo ""
echo "✅ Deployment complete!"
echo "🧠 Dr. Freud AI Chatbot is available at:"
echo "   Local: http://localhost:$(grep STREAMLIT_SERVER_PORT .env | cut -d '=' -f2)"
echo "   Public: https://$(grep TRAEFIK_HOST .env | cut -d '=' -f2) (if Traefik is configured)"
echo ""
echo "📊 User data is now persistent across deployments!"
echo "📁 Data backup location: $DATA_DIR"
echo ""

# Ask if user wants to see logs
read -p "Show container logs? (y/N): " SHOW_LOGS
if [[ $SHOW_LOGS =~ ^[Yy]$ ]]; then
    echo "📋 Showing logs (press Ctrl+C to exit):"
    sudo docker compose logs -f
fi