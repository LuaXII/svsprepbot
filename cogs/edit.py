import nextcord
from nextcord.ext import commands

class EditCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="edit", description="Edit an existing schedule entry")
    async def edit(self, interaction: nextcord.Interaction):
        await interaction.response.send_message("✏️ Edit feature coming soon!")

def setup(bot):
    bot.add_cog(EditCog(bot))
