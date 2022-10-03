import aiosqlite
import discord
from discord.ext import commands


class initServer(commands.Cog):
    """Initialize a new discord guild to the Database."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        embed = discord.Embed(title="Hello, I'm Licensy!",
                              description="I'm a bot that helps you manage and create licenses and products for your customer. To get started, please run the command `/init`. If you need help, please use the command `/help`.",
                              color=0x00ff00)
        try:
            await guild.system_channel.send(embed=embed)
        except discord.Forbidden or AttributeError:
            try:
                guild.owner.send(embed=embed)
            except discord.Forbidden or AttributeError:
                pass

    @discord.app_commands.command(name='init', description='Initialize the server to the database')
    async def init(self, interaction: discord.Interaction):
        async with aiosqlite.connect('./data/db.sqlite') as db:
            cursor = await db.cursor()
            await cursor.execute('INSERT INTO guilds (guild_id, prefix) VALUES (?, ?)', (interaction.guild.id, "/"))
            await db.commit()
        embed = discord.Embed(
            title="Server initialized", description="The server has been initialized to the database.", color=0x00ff00)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(initServer(bot))
