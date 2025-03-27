import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")


# ✅ Enable required intents
intents = nextcord.Intents.default()
intents.message_content = True  # Required for message-based commands

# ✅ Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

    # 🔹 Load all cogs (excluding __init__.py)
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"🔹 Loaded cog: {filename[:-3]}")

    # 🔄 Sync Slash Commands Properly
    try:
        await bot.sync_application_commands()  # ✅ Use this instead of bot.tree.sync()
        print("✅ Slash commands synced successfully!")
    except Exception as e:
        print(f"⚠️ Error syncing commands: {e}")

bot.run(BOT_TOKEN)
