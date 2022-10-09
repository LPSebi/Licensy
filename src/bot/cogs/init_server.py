from time import time
from discord.ext import commands
from discord import app_commands
import discord
import aiosqlite
import uuid
import sys
from constants.constants import EMBED_ERROR_TITLE, EMBED_ERROR_COLOR, EMBED_SUCCESS_COLOR


class InitServer(commands.Cog):
    """Initialize a new discord guild to the Database."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        embed = discord.Embed(
            title="Hello, I'm Licensy!",
            description="I'm a bot that helps you manage and create licenses and products for your customer. To get started, please run the command `/init`. If you need help, please use the command `/help`.",
            color=0x00FF00,
        )
        try:
            await guild.system_channel.send(embed=embed)
        except discord.Forbidden or AttributeError:
            try:
                await guild.owner.send(embed=embed)
            except discord.Forbidden or AttributeError:
                pass

    @app_commands.command(
        name="init", description="Initialize the server to the database"
    )
    async def init(self, interaction: discord.Interaction):
        async with aiosqlite.connect("./data/db.sqlite") as db:
            cursor = await db.execute("SELECT * FROM guilds WHERE id = ?", (interaction.guild.id,))
            if (await cursor.fetchone() is not None):
                embed = discord.Embed(
                    title=EMBED_ERROR_TITLE,
                    description="This server is already initialized.",
                    color=EMBED_ERROR_COLOR,
                )
                return await interaction.response.send_message(embed=embed)
            cursor = await db.execute(
                "INSERT INTO guilds (uuid, id, date) VALUES (?, ?, ?)",
                (str(uuid.uuid4()), interaction.guild.id, int(round(time()))),
            )
            await db.commit()
        embed = discord.Embed(
            title="Server initialized",
            description="The server has been initialized to the database.",
            color=EMBED_SUCCESS_COLOR,
        )
        return await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(InitServer(bot))
