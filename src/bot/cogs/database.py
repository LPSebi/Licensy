import time
import discord
from discord.ext import commands
from discord import app_commands
import aiosqlite


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='databasecheck', description='Check the database connection')
    async def databasecheck(self, interaction: discord.Interaction):
        try:
            async with aiosqlite.connect('./data/db.sqlite') as db:
                # get ping of db
                try:
                    time1 = time.time()
                    await db.execute('SELECT * FROM `guilds`')
                    time2 = time.time()
                except:
                    embed = discord.Embed(
                        title='Database Error', description='There was an error connecting to the database. Please try again later.', color=0xff0000)
                    return await interaction.response.send_message(embed=embed)
                ping = round((time2 - time1) * 10000, 3)
                embed = discord.Embed(
                    title='Database', description=f'Ping: {ping}ms', color=discord.Color.green())
                return await interaction.response.send_message(embed=embed)
        except aiosqlite.OperationalError as e:
            embed = discord.Embed(
                title='Database Error', description=f'There was an error connecting to the database. Please try again later.\nError: {e}', color=0xff0000)
            return await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Database(bot))
