# 🧠 Dr. Freud AI Chatbot

A Streamlit-based AI chatbot that simulates a conversation with a mutated version of Dr. Sigmund Freud in a post-apocalyptic setting. The chatbot responds exclusively in German, embodying the persona of Dr. Freud with psychological insights and a distinctive communication style.

## 🚀 Features

- Interactive chat interface with a unique AI personality
- Post-apocalyptic Dr. Freud persona with distinct behavioral traits
- German language responses with psychological depth
- Containerized deployment with Docker
- Traefik reverse proxy support for production deployment

## 🛠️ Prerequisites

- Docker and Docker Compose
- OpenAI API key
- Git

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/kbstn/Dr_Freud_AI_Chatbot.git
   cd Dr_Freud_AI_Chatbot
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Build and start the application**
   ```bash
   docker compose up -d --build
   ```

4. **Access the chatbot**
   - Local: http://localhost:8501
   - Or via your configured domain if using Traefik

## 🔧 Configuration

Edit the `.env` file to customize:
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `STREAMLIT_SERVER_PORT`: Port to run the Streamlit server (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Network interface to bind to (default: 0.0.0.0)
- `TRAEFIK_HOST`: Your domain name if using Traefik

## 🐳 Using the Deployment Script

For easy deployment, use the provided script:

```bash
chmod +x deploy.sh
sudo ./deploy.sh
```

The script will guide you through the setup process and start the application.

## 🛑 Stopping the Application

To stop the application:

```bash
docker compose down
```

## 🤖 About the AI Persona

The chatbot is designed to simulate Dr. Sigmund Freud in a post-apocalyptic setting, with the following characteristics:
- Knowledge limited to pre-1960 information
- Distinct personality traits including mood swings and fixations
- Passive-aggressive communication style
- Responds exclusively in German
- May react strongly to being addressed without the proper title "Dr. Freud"

## 📝 License

[Specify your license here]
