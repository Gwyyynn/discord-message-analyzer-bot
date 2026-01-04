import discord
from datetime import datetime

# Logging analysis events
def log_event(
    interaction: discord.Interaction,
    target: discord.User | None,
    message_count: int,
    status: str
):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    guild = interaction.guild
    channel = interaction.channel
    invoker = interaction.user

    line = (
        f"[{ts}] "
        f"guild={guild.name if guild else 'DM'} | "
        f"channel={channel.name if channel else 'DM'} | "
        f"invoker={invoker} ({invoker.id}) | "
        f"target={target} ({target.id}) | "
        f"messages={message_count} | "
        f"status={status}\n"
    )

    with open("bot.log", "a", encoding="utf-8") as f:
        f.write(line)
