import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MESSAGE_LIMIT = 50   # messages limit for user analysis
COOLDOWN = 60  # cooldown time in seconds
MAX_MESSAGE_LENGTH = 2000  # max length of a message to be analyzed

