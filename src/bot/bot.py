# General imports
import os
import typing
from discord.ext import commands
import discord
from discord import app_commands
from discord.app_commands import Choice
from dotenv import load_dotenv
import rich


# Init bot and env variables
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='.', intents=intents)


@bot.event
async def on_ready():
    for filename in os.listdir('./src/cogs'):
        if filename.endswith('.py') and not filename.startswith('_'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            rich.print(
                f'[bold green]Successfully loaded cog[/bold green] [bold magenta]{filename[:-3]}[/bold magenta]')
    await bot.tree.sync(guild=discord.Object(id=981576035176964117))
    rich.print(
        f'[bold magenta]{bot.user.name}[/bold magenta] [bold green]successfully connected to the discord API![/bold green]')


@commands.is_owner()
@bot.tree.command(name='reload', description='Reload an Extension')
@app_commands.choices(cog=[
    Choice(name='Default', value='_default'),
    Choice(name='Backup', value='backup'),
    Choice(name='Database', value='database'),
    Choice(name='Init Server', value='init_server'),
    Choice(name='Manage Product', value='manage_product'),
])
async def reload(interaction: discord.Interaction, cog: Choice[str]) -> None:
    try:
        await bot.reload_extension(f'cogs.{cog.value}')
        await interaction.response.send_message(f'Extension {cog.value} reloaded!', ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f'Error while reloading Extension {cog.value}: {e}', ephemeral=True)


@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
        ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: typing.Optional[typing.Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

bot.run(TOKEN)
