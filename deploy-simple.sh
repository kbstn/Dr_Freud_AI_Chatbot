#!/bin/bash

# Simple, reliable deployment script
set -e

echo "🧠 Dr. Freud AI Chatbot - Simple Deployment"
echo "==========================================="

# Set directories
PROJECT_DIR="/opt/containers/Dr_Freud_AI_Chatbot"
BACKUP_DIR="/opt/containers/backup_$(date +%Y%m%d_%H%M%S)"

echo "📁 Setting up directories..."
sudo mkdir -p /opt/containers

# Navigate to containers directory
cd /opt/containers

# If project exists, backup and stop it
if [ -d "$PROJECT_DIR" ]; then
    echo "📦 Backing up existing installation..."
    sudo cp -r "$PROJECT_DIR" "$BACKUP_DIR"
    
    echo "🛑 Stopping containers..."
    cd "$PROJECT_DIR"
    sudo docker compose down 2>/dev/null || true
    cd /opt/containers
    
    echo "🗑️  Removing old installation..."
    sudo rm -rf "$PROJECT_DIR"
fi

echo "📥 Cloning repository..."
git clone https://github.com/kbstn/Dr_Freud_AI_Chatbot.git

# Check if clone was successful
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ Git clone failed! Trying with sudo..."
    sudo git clone https://github.com/kbstn/Dr_Freud_AI_Chatbot.git
fi

# Verify directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ Failed to clone repository!"
    echo "Please check your internet connection and try again."
    exit 1
fi

echo "✅ Repository cloned successfully"
cd "$PROJECT_DIR"

# List files to verify
echo "📋 Files in project directory:"
ls -la

# Restore .env if backup exists
if [ -f "$BACKUP_DIR/.env" ]; then
    echo "📂 Restoring .env file..."
    sudo cp "$BACKUP_DIR/.env" .
else
    echo "⚙️  Creating new .env file..."
    cp .env.example .env
    
    echo "Please edit .env file with your settings:"
    echo "nano .env"
    echo ""
    echo "Required: Set your OPENAI_API_KEY"
    echo ""
    read -p "Press Enter when you've configured .env file..."
fi

# Restore presets if backup exists
if [ -d "$BACKUP_DIR/presets" ]; then
    echo "📂 Restoring presets..."
    sudo cp -r "$BACKUP_DIR/presets" .
fi

echo "🚀 Starting application..."
sudo docker compose up -d --build

echo ""
echo "✅ Deployment complete!"
echo "🌐 Application available at:"
echo "   http://localhost:$(grep STREAMLIT_SERVER_PORT .env | cut -d= -f2 2>/dev/null || echo '8501')"
echo ""
echo "📊 Check status with: sudo docker compose ps"
echo "📋 View logs with: sudo docker compose logs -f"

# Show final verification
echo ""
echo "📁 Final directory check:"
pwd
ls -la