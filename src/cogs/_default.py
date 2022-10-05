import discord
from discord.ext import commands


class Default(commands.Cog):
    """All of the essential commands for the bot to function."""

    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Default(bot))
