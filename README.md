
## Discord Message Analyzer Bot

Analyzes Discord messages in a sarcastic and harsh style using an LLM.

### Features
- Context menu: analyze a single message
- Slash command: analyze a user's recent messages
- Public analysis results
- Private technical feedback
- Cooldown protection
- Full logging

### Commands
- Right-click message → "Analyze message"
- /analyze @user

### Tech
- discord.py
- Groq API (LLaMA 3.1)

### How to start

1. Download or clone this repository
2. Create a `.env` file in the project root
3. Add your API keys to `.env`:
4. Create a virtual environment: python -m venv .venv -
5. Activate the virtual environment: .venv\Scripts\Activate.ps1
6. Install requirements: pip install -r requirements.txt
7. Run the bot: python main.py
