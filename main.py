import discord
import os
from discord import app_commands
from discord.ext import commands
from config import DISCORD_TOKEN, MESSAGE_LIMIT
from discord.errors import Forbidden
from services import analyze_messages
from logger import log_event
from filter import is_good_message
from cooldown import is_on_cooldown, set_cooldown

# Clean up the log file if it is too large
LOG_FILE = "bot.log"
MAX_SIZE = 1_000_000  # 1 MB
if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > MAX_SIZE:
    open(LOG_FILE, "w").close()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Universal analysis function:
# - ensures Discord response (defer)   
# - performs text analysis
# - posts result in channel
# - logs event and sets cooldown
async def process_analysis(
    *,
    interaction: discord.Interaction,
    texts: list[str],
    public_message: str
):
    if not interaction.response.is_done():
        await interaction.response.defer(ephemeral=True)

    try:
        analysis = await analyze_messages(texts)

        await interaction.channel.send(
            f"{public_message}\n{analysis[:1900]}"
        )

        await interaction.followup.send(
            "✅ Analysis complete.",
            ephemeral=True
        )

        log_event(
            interaction,
            interaction.user,
            len(texts),
            "OK"
        )

        set_cooldown(interaction.user.id)

    except Exception as e:
        await interaction.followup.send(
            "❌ Analysis failed.",
            ephemeral=True
        )

        log_event(
            interaction,
            interaction.user,
            len(texts),
            f"ERROR: {e}"
        )

@bot.event
async def on_ready():
    print(f"✅ Bot is running as {bot.user}")

    # синхронизация slash-команд
    await bot.tree.sync()
    print("✅ Slash commands synchronized")


# Context menu: analyze a single message
# Technical responses — only to the initiator (ephemeral)
# Analysis result — public in the channel
@bot.tree.context_menu(name="Analyze message")
async def analyze_message_ctx(
    interaction: discord.Interaction,
    message: discord.Message
):
    if is_on_cooldown(interaction.user.id):
        await interaction.response.send_message(
            "⏳ Please wait before running another analysis.",
            ephemeral=True
        )
        return

    if not is_good_message(message.content):
        await interaction.response.send_message(
            "❌ Message is not suitable for analysis.",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        "⏳ Analyzing message...",
        ephemeral=True
    )

    await process_analysis(
        interaction=interaction,
        texts=[message.content],
        public_message=f"**Message analysis for {message.author.mention}:**"
    )

# Context menu: analyze user's messages in the channel
# Technical responses — only to the initiator (ephemeral)
# Analysis result — public in the channel
@bot.tree.command(name="analyze", description="Analyze a user's messages in this channel")
@app_commands.describe(user="User to analyze")
async def analyze(interaction: discord.Interaction, user: discord.User):
    if is_on_cooldown(interaction.user.id):
        await interaction.response.send_message(
            "⏳ Please wait before running another analysis.",
            ephemeral=True
        )
        return

    await interaction.response.defer(ephemeral=True)

    messages = []
    try:
        async for msg in interaction.channel.history(limit=200):
            if msg.author.id == user.id and is_good_message(msg.content):
                messages.append(msg.content)
                if len(messages) >= MESSAGE_LIMIT:
                    break
    except Forbidden:
        await interaction.followup.send(
            "❌ Missing permissions to read message history.",
            ephemeral=True
        )
        return

    if not messages:
        await interaction.followup.send(
            f"❌ No suitable messages found. {user.mention}.",
            ephemeral=True
        )
        return

    await process_analysis(
        interaction=interaction,
        texts=messages,
        public_message = f"**Analysis result for {user.mention}:**"
    )

    
bot.run(DISCORD_TOKEN)