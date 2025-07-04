# 🧠 Dr. Freud AI Chatbot

A Streamlit-based AI chatbot that simulates conversations with Dr. Sigmund Freud in a post-apocalyptic setting. The chatbot uses OpenAI's API through the Pydantic AI framework and responds exclusively in German with a distinctive personality.

## 🚀 Features

- Interactive chat interface with conversation memory
- Real-time personality editing and preset management
- Post-apocalyptic Dr. Freud persona with psychological depth
- German language responses with distinctive behavioral traits
- Agent memory debug log for development insights
- Web search capabilities (optional)
- Containerized deployment with Docker and Traefik support

## 🛠️ Prerequisites

- Docker and Docker Compose installed on your system
- OpenAI API key
- Git (for cloning the repository)

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/kbstn/Dr_Freud_AI_Chatbot.git
   cd Dr_Freud_AI_Chatbot
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your OpenAI API key and other settings
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker compose up -d --build
   ```

4. **Access the chatbot**
   - Local: http://localhost:8501
   - Or via your configured domain if using Traefik

## ⚙️ Configuration

Edit the `.env` file to customize:
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `STREAMLIT_SERVER_PORT`: Port to run the Streamlit server (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Network interface to bind to (default: 0.0.0.0)
- `TRAEFIK_HOST`: Your domain name if using Traefik

## 🐳 Local Development

For local development without Docker:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application locally
streamlit run app.py
```

## 🚀 Production Deployment

### Quick Start (with data persistence)
```bash
chmod +x deploy-improved.sh
sudo ./deploy-improved.sh
```

### Regular Updates (preserves user data)
```bash
sudo ./deploy-update.sh
```

📖 **For detailed deployment options and data persistence solutions, see [DEPLOYMENT.md](DEPLOYMENT.md)**

## 🛑 Stopping the Application

```bash
docker compose down
```

## 🧩 Application Architecture

The application is built with a modular architecture:

- **`app.py`**: Main application entry point
- **`src/config.py`**: Configuration constants and settings
- **`src/styles.py`**: CSS styling functions
- **`src/session_manager.py`**: Session state and conversation management
- **`src/agent_manager.py`**: AI agent creation and caching
- **`src/ui_components.py`**: Reusable UI components
- **`src/prompts.py`**: System prompts and personality definitions
- **`src/edit_system_prompt.py`**: Personality editing functionality
- **`presets/`**: Personality preset files

## 🤖 About the AI Persona

The chatbot simulates Dr. Sigmund Freud in a post-apocalyptic setting with:
- Knowledge limited to pre-1960 technology
- Arrogant, passive-aggressive personality
- Responds exclusively in German
- Psychological analysis of every interaction
- Strong reactions to improper addressing (requires "Dr. Freud")
- Conversation memory that persists throughout the session

## 🔍 Debug Features

The application includes a comprehensive debug log (expandable section at the bottom) showing:
- **Current Session State**: Total message count and model settings
- **Conversation History**: Formatted history sent to the agent
- **System Prompts**: Base personality prompt and complete prompt with conversation context
- **Real-time Memory State**: Live updates as you chat
- **Model Configuration**: Current model, temperature, and web search settings

This debug log helps verify that conversation memory is working correctly and shows exactly what context the AI agent receives.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
