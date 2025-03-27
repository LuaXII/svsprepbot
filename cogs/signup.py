import nextcord
from nextcord.ext import commands
from pymongo import MongoClient
from utils import log_success, log_failure, log_warning
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["discord_bot"]
collection = db["schedule"]

class SignupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="signup", description="Register a user's schedule sign-up")
    async def signup(self, interaction: nextcord.Interaction, alliance: str, user_id: str, username: str, speeds: int, time_slots: str):
        # Split the time_slots string into a list
        time_slots = time_slots.split(',') if time_slots else []

        log_success(f"Signup attempt by {interaction.user}: alliance={alliance}, user_id={user_id}, username={username}, speeds={speeds}, time_slots={time_slots}")

        try:
            # Check if the time slots are available
            for slot in time_slots:
                existing_entry = collection.find_one({"time_slots": slot})
                if existing_entry:
                    await interaction.response.send_message(f"❌ **Time slot `{slot}` is already taken. Please choose a different time.**")
                    log_warning(f"Conflict for {interaction.user} with time slot `{slot}`.")
                    return

            # Check if the user has an existing entry
            existing_entry = collection.find_one({"user_id": user_id})
            if existing_entry:
                collection.update_one({"user_id": user_id}, {"$set": {
                    "alliance": alliance, "username": username, "speeds": speeds, "time_slots": time_slots
                }})
                await interaction.response.send_message(f"✅ **{interaction.user.mention}, your entry has been updated!**", embed=nextcord.Embed(title="Update Successful", description="Your schedule has been updated!", color=nextcord.Color.green()))
            else:
                collection.insert_one({
                    "alliance": alliance, "user_id": user_id, "username": username, "speeds": speeds, "time_slots": time_slots
                })
                await interaction.response.send_message(f"✅ **{interaction.user.mention}, your signup has been recorded!**", embed=nextcord.Embed(title="Signup Successful", description="Your schedule has been recorded!", color=nextcord.Color.green()))

        except Exception as e:
            log_failure(f"Error during signup: {str(e)}")
            await interaction.response.send_message("❌ **An error occurred. Try again later.**")

def setup(bot):
    bot.add_cog(SignupCog(bot))
