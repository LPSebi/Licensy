import discord
from discord.ext import commands
from discord import app_commands, ui
from discord.app_commands import Choice
from constants.constants import embedErrorFull, embedErrorTitle, embedErrorColor
import aiosqlite


class CreateProductModal(ui.Modal, title='Questionnaire Response'):
    """The modal for creating a product."""  # TODO: Continue class
    name = ui.TextInput(label='Name')
    answer = ui.TextInput(label='Answer', style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)


class ManageProduct(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='product', description='commandDescription')
    @app_commands.choices(option1=[
        Choice(name='Create', value='create'),
        Choice(name='Edit', value='edit'),
        Choice(name='Delete', value='delete'),
        Choice(name='List', value='list'),
    ])
    async def product(self, interaction: discord.Interaction, option1: Choice[str]):
        match option1.value:
            case 'create':
                with aiosqlite.connect("./data/db.sqlite") as db:
                    cursor = db.execute(
                        "SELECT * FROM guilds WHERE id = ?", (interaction.guild.id,))
                    if cursor.fetchone() is None:
                        embed = discord.Embed(
                            title=embedErrorTitle, description="This server is not initialized. Please run the command `/init` to initialize the server.", color=embedErrorColor)
                        return await interaction.response.send_message(embed=embed)
                    else:
                        pass  # TODO: Run a modal to get user input

                await interaction.response.send_message('create')
            case 'edit':
                await interaction.response.send_message('edit')
            case 'delete':
                await interaction.response.send_message('delete')
            case _:
                await interaction.response.send_message(embed=embedErrorFull)


async def setup(bot):
    await bot.add_cog(ManageProduct(bot))
