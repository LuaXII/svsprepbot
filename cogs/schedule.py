import nextcord
from nextcord.ext import commands
from pymongo import MongoClient
from utils import log_success, log_failure
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["discord_bot"]
collection = db["schedule"]

class ScheduleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="schedule", description="View the current schedule")
    async def schedule(self, interaction: nextcord.Interaction):
        try:
            entries = collection.find()
            schedule_dict = {}

            # Build the schedule dictionary from the MongoDB entries
            for entry in entries:
                for slot in entry.get("time_slots", []):
                    schedule_dict[slot] = (entry["alliance"], entry["user_id"], entry["username"], entry["speeds"])

            embed = nextcord.Embed(
                title="📅 **Master Schedule**",
                description="Here is the schedule for the upcoming sessions. 🗓️",
                color=nextcord.Color.blue()
            )

            # Loop through the sorted slots and add them to the embed with extra space
            for slot, (alliance, user_id, username, speeds) in sorted(schedule_dict.items()):
                embed.add_field(
                    name=f"🕒 **{slot}**",
                    value=f"🏰 **Alliance:** {alliance}\n👤 **User:** {username} (ID: `{user_id}`)\n⚡ **Speeds:** `{speeds}`",
                    inline=False
                )

            embed.set_footer(text="Powered by SvS Prep Bot")
            await interaction.response.send_message(embed=embed)
            log_success("📅 **Displayed the master schedule.**")

        except Exception as e:
            log_failure(f"Error while displaying the schedule: {str(e)}")
            await interaction.response.send_message(f"❌ **An error occurred: {str(e)}.**")

def setup(bot):
    bot.add_cog(ScheduleCog(bot))
