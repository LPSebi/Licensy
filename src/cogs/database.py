import time
import discord
from discord.ext import commands
import aiosqlite


class database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='databasecheck', description='Check the database connection')
    async def databasecheck(self, interaction: discord.Interaction):
        async with aiosqlite.connect('./data/db.sqlite') as db:
            # get ping of db
            try:
                time1 = time.time()
                db.execute('SELECT * FROM `guilds`')
                time2 = time.time()
            except:
                embed = discord.Embed(
                    title='Database Error', description='There was an error connecting to the database. Please try again later.', color=0xff0000)
                return await interaction.response.send_message(embed=embed)
            ping = round((time2 - time1) * 1000, 3)
            embed = discord.Embed(
                title='Database', description=f'Ping: {ping}ms', color=discord.Color.green())
            return await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(database(bot))
