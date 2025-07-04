#!/bin/bash

# Dr. Freud AI Chatbot - Update Deployment Script
# This script updates the application without losing user data

# Exit on error
set -e

# Set project directory
PROJECT_DIR="/opt/containers/Dr_Freud_AI_Chatbot"

echo "🧠 Dr. Freud AI Chatbot - Update Deployment"
echo "=========================================="

# Check if project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ Project directory does not exist: $PROJECT_DIR"
    echo "Please run the initial deployment script first:"
    echo "   sudo ./deploy-improved.sh"
    exit 1
fi

# Navigate to project directory
cd "$PROJECT_DIR"

# Check if it's a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not a git repository. Please run the initial deployment script:"
    echo "   sudo ./deploy-improved.sh"
    exit 1
fi

echo "🛑 Stopping containers..."
sudo docker compose down

echo "📥 Pulling latest changes from repository..."
sudo git fetch origin
sudo git reset --hard origin/main

echo "🔄 Rebuilding and starting containers..."
sudo docker compose up -d --build

echo ""
echo "✅ Update complete!"
echo "🧠 Dr. Freud AI Chatbot is available at:"
echo "   Local: http://localhost:$(grep STREAMLIT_SERVER_PORT .env | cut -d '=' -f2)"
echo "   Public: https://$(grep TRAEFIK_HOST .env | cut -d '=' -f2) (if Traefik is configured)"
echo ""
echo "📊 User data (presets) preserved during update!"
echo ""

# Ask if user wants to see logs
read -p "Show container logs? (y/N): " SHOW_LOGS
if [[ $SHOW_LOGS =~ ^[Yy]$ ]]; then
    echo "📋 Showing logs (press Ctrl+C to exit):"
    sudo docker compose logs -f
fi