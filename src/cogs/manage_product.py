import discord
from discord.ext import commands
from discord import app_commands, ui
from discord.app_commands import Choice
from constants.constants import embedErrorFull, embedErrorTitle, embedErrorColor, embedErrorInvalidPrice
import aiosqlite
import uuid


class CreateProductModal(ui.Modal, title='Create Product'):
    """The modal for creating a product."""
    name = ui.TextInput(label='Name of your product',
                        placeholder='Ex: My product (Max 20 characters)', max_length=20, style=discord.TextStyle.short)
    description = ui.TextInput(
        label='Description of your product', placeholder='Ex: This Product does cool things (Max 100 characters)', style=discord.TextStyle.paragraph, required=True, max_length=100)
    price = ui.TextInput(label='Price of your product',
                         placeholder='Ex: 10 (no floating numbers, Max 5 characters)', required=True, max_length=5, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        #print(self.name.value + self.description.value + str(type(self.price.value)))
        try:
            self.price.value = int(self.price.value)
        except ValueError:
            embed = discord.Embed(
                title=embedErrorTitle, description=embedErrorInvalidPrice, color=embedErrorColor)
            return await interaction.response.send_message(embed=embed)
        except AttributeError:
            if int(self.price.value) < 0:
                embed = discord.Embed(
                    title=embedErrorTitle, description="An error has occurred. Price must be a positive number.", color=embedErrorColor)
                return await interaction.response.send_message(embed=embed)
            # TODO: import data to db
            with aiosqlite.connect('./data/db.sqlite') as db:
                cursor = await db.execute('SELECT * FROM guilds WHERE guild_id = ?', (interaction.guild.id,))
                guild_uuid = await cursor.fetchone()[0]
                await db.execute('INSERT INTO products (uuid, server_uuid, name, description, price) VALUES (?, ?, ?, ?, ?)', (uuid.uuid4(), guild_uuid, self.name.value, self.description.value, int(self.price.value)))
            return await interaction.response.send_message(f'Thanks for your response, {interaction.user.name}!', ephemeral=True)


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
                db = await aiosqlite.connect('./data/db.sqlite')
                cursor = await db.execute(
                    "SELECT * FROM guilds WHERE id = ?", (interaction.guild.id,))
                if await cursor.fetchone() is None:
                    embed = discord.Embed(
                        title=embedErrorTitle, description="This server is not initialized. Please run the command `/init` to initialize the server.", color=embedErrorColor)
                    return await interaction.response.send_message(embed=embed)
                else:
                    return await interaction.response.send_modal(CreateProductModal())

            case 'edit':
                with aiosqlite.connect('./data/db.sqlite') as db:
                    cursor = db.execute(
                        'SELECT * FROM guilds WHERE id = ?', (interaction.guild.id,))
                    if cursor.fetchone() is None:
                        embed = discord.Embed(
                            title=embedErrorTitle, description="This server is not initialized. Please run the command `/init` to initialize the server.", color=embedErrorColor)
                    else:
                        pass
                        return await interaction.response.send_message(embed=embed)
                await interaction.response.send_message('edit')
            case 'delete':
                await interaction.response.send_message('delete')
            case _:
                await interaction.response.send_message(embed=embedErrorFull)


async def setup(bot):
    await bot.add_cog(ManageProduct(bot))
