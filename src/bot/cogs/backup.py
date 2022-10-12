from datetime import date, datetime
import os
import discord
from discord.ext import commands, tasks
import aiosqlite


class Backup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dbBackup.start()

    @tasks.loop(hours=24)
    async def dbBackup(self):
        async with aiosqlite.connect('./data/db.sqlite') as db:
            tables = await db.execute('SELECT name FROM sqlite_master WHERE type="table"')
            tablesCursor = await tables.fetchall()
            guildTableRows = await db.execute('SELECT count(*) FROM guilds')
            guildTableRowsCursor = await guildTableRows.fetchall()
            productsTableRows = await db.execute('SELECT count(*) FROM products')
            productsTableRowsCursor = await productsTableRows.fetchall()

        if os.path.exists('./data/temp/backup.sql'):
            os.remove('./data/temp/backup.sql')
        today = date.today()
        channelId = 1026064413377187850
        _channel = self.bot.get_channel(channelId)
        _now = datetime.now().time()
        os.system(".\\sqlite3 ./data/db.sqlite .dump > ./data/temp/backup.sql")
        _file = discord.File("./data/temp/backup.sql")
        _file.filename = f"SPOILER_backup.sql"

        embed = discord.Embed(
            title="Database Backup",
            description="Database Backup",
            color=0xff0000)
        embed.add_field(name="Date", value=today.strftime(
            "%d.%m.%Y"), inline=False)

        embed.add_field(name="Time", value=_now, inline=False)
        embed.add_field(name="Size", value=str(
            os.stat("./data/temp/backup.sql").st_size) + " bytes", inline=False)
        embed.add_field(name="Tables", value=', '.join(
            [str(x) for t in tablesCursor for x in t]), inline=False)
        embed.add_field(name="Guild table rows",
                        value=guildTableRowsCursor[0][0], inline=False)
        embed.add_field(name="licenses table rows",
                        value=productsTableRowsCursor[0][0], inline=False)

        with open('./data/temp/backup.sql', 'r'):
            await _channel.send(file=_file, embed=embed)
        os.remove("./data/temp/backup.sql")


async def setup(bot):
    await bot.add_cog(Backup(bot))
