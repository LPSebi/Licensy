from time import time
import discord
from discord.ext import commands
from discord import app_commands, ui
from discord.app_commands import Choice
from constants.constants import *
import aiosqlite
import uuid


class CreateProductModal(ui.Modal, title='Create Product'):
    """The modal for creating a product."""
    name = ui.TextInput(label='Name of your product',
                        placeholder='Ex: My product (Max 20 characters)', max_length=20, style=discord.TextStyle.short)
    description = ui.TextInput(
        label='Description of your product', placeholder='Ex: This Product does cool things (Max 100 characters)', style=discord.TextStyle.paragraph, required=False, max_length=100)
    price = ui.TextInput(label='Price of your product',
                         placeholder='Ex: 10 (no floating numbers, Max 5 characters)', required=True, max_length=5, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        #print(self.name.value + self.description.value + str(type(self.price.value)))
        try:
            price = int(self.price.value)
        except ValueError:
            embed = discord.Embed(
                title=embedErrorTitle, description=embedErrorInvalidPrice, color=embedErrorColor)
            return await interaction.response.send_message(embed=embed)
        if int(price) < 0:
            embed = discord.Embed(
                title=embedErrorTitle, description="An error has occurred. Price must be a positive number.", color=embedErrorColor)
            return await interaction.response.send_message(embed=embed)
        # TODO: import data to db
        async with aiosqlite.connect('./data/db.sqlite') as db:
            current_guild = await db.execute('SELECT * FROM guilds WHERE id = ?', (interaction.guild.id,))
            guild_uuid = (await current_guild.fetchone())[0]
            await db.execute('INSERT INTO products (uuid, guild_uuid, name, price, description, date) VALUES (?, ?, ?, ?, ?, ?)',
                             (str(uuid.uuid4()), guild_uuid, self.name.value, int(self.price.value), self.description.value, int(round(time()))))
            await db.commit()
            await db.close()
            # TODO: change
            return await interaction.response.send_message(f'Thanks for your response, {interaction.user.name}!', ephemeral=True)


class EditProductModal(ui.Modal, title='Edit Product'):
    """The modal for creating a product."""
    name = ui.TextInput(label='New name of your product',
                        placeholder='Ex: My product (Max 20 characters)', max_length=20, style=discord.TextStyle.short)
    description = ui.TextInput(
        label='New description of your product', placeholder='Ex: This Product does cool things (Max 100 characters)', style=discord.TextStyle.paragraph, required=False, max_length=100)
    price = ui.TextInput(label='Price of your product',
                         placeholder='Ex: 10 (no floating numbers, Max 5 characters)', required=True, max_length=5, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        #print(self.name.value + self.description.value + str(type(self.price.value)))
        try:
            price = int(self.price.value)
        except ValueError:
            embed = discord.Embed(
                title=embedErrorTitle, description=embedErrorInvalidPrice, color=embedErrorColor)
            return await interaction.response.send_message(embed=embed)
        if int(price) < 0:
            embed = discord.Embed(
                title=embedErrorTitle, description="An error has occurred. Price must be a positive number.", color=embedErrorColor)
            return await interaction.response.send_message(embed=embed)
        # TODO: import data to db
        async with aiosqlite.connect('./data/db.sqlite') as db:
            current_guild = await db.execute('SELECT * FROM guilds WHERE id = ?', (interaction.guild.id,))
            guild_uuid = (await current_guild.fetchone())[0]
            await db.execute('INSERT INTO products (uuid, guild_uuid, name, price, description, date) VALUES (?, ?, ?, ?, ?, ?)',
                             (str(uuid.uuid4()), guild_uuid, self.name.value, int(self.price.value), self.description.value, int(round(time()))))
            await db.commit()
            # TODO: change
            return await interaction.response.send_message(f'Thanks for your response, {interaction.user.name}!', ephemeral=True)


class ConfirmEditProduct(ui.View):
    def __init__(self):
        super().__init__()

    @ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EditProductModal())
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Cancelling', ephemeral=True)
        self.stop()


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
                async with aiosqlite.connect('./data/db.sqlite') as db:
                    cursor = await db.execute(
                        "SELECT * FROM guilds WHERE id = ?", (interaction.guild.id,))
                    if await cursor.fetchone() is None:
                        embed = discord.Embed(
                            title=embedErrorTitle, description="This server is not initialized. Please run the command `/init` to initialize the server.", color=embedErrorColor)
                        await db.close()
                        return await interaction.response.send_message(embed=embed)
                    else:
                        return await interaction.response.send_modal(CreateProductModal())

            case 'edit':
                async with aiosqlite.connect('./data/db.sqlite') as db:
                    cursor = await db.execute(
                        "SELECT * FROM guilds WHERE id = ?", (interaction.guild.id,))
                    if await cursor.fetchone() is None:
                        embed = discord.Embed(
                            title=embedErrorTitle, description="This server is not initialized. Please run the command `/init` to initialize the server.", color=embedErrorColor)
                        await db.close()
                        return await interaction.response.send_message(embed=embed)
                    else:
                        # add all uuid of all products to a list with name
                        current_guild = await db.execute('SELECT * FROM guilds WHERE id = ?', (interaction.guild.id,))
                        guild_uuid = (await current_guild.fetchone())[0]
                        cursor = await db.execute('SELECT * FROM products WHERE guild_uuid = ?', (guild_uuid,))
                        products = await cursor.fetchall()
                        if len(products) == 0:
                            embed = discord.Embed(
                                title=embedErrorTitle, description="There are no products to edit.", color=embedErrorColor)
                            await db.close()
                            return await interaction.response.send_message(embed=embed)
                        else:
                            view = ConfirmEditProduct()
                            embed = discord.Embed(
                                title=embedWarningTitle, description="The next input requires the product uuid. Please make sure you have it.\nYou can get it by running `/products list`", color=embedWarningColor)
                            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
                            # return await interaction.response.send_modal(EditProductModal())
            case 'delete':
                await interaction.response.send_message('delete')
            case 'list':
                # return list of all products in an embed
                async with aiosqlite.connect('./data/db.sqlite') as db:
                    cursor = await db.execute('SELECT * FROM guilds WHERE id = ?', (interaction.guild.id,))
                    if await cursor.fetchone() is None:
                        embed = discord.Embed(
                            title=embedErrorTitle, description="This server is not initialized. Please run the command `/init` to initialize the server.", color=embedErrorColor)
                        return await interaction.response.send_message(embed=embed)
                    else:
                        current_guild = await db.execute('SELECT * FROM guilds WHERE id = ?', (interaction.guild.id,))
                        guild_uuid = (await current_guild.fetchone())[0]
                        cursor = await db.execute('SELECT * FROM products WHERE guild_uuid = ?', (guild_uuid,))
                        products = await cursor.fetchall()
                        if len(products) == 0:
                            embed = discord.Embed(
                                title=embedErrorTitle, description="There are no products to list.", color=embedErrorColor)
                            return await interaction.response.send_message(embed=embed)
                        else:
                            embed = discord.Embed(
                                title=embedSuccessTitle, description="Here is the list of all products.", color=embedSuccessColor)
                            for product in products:
                                embed.add_field(
                                    name=product[2], value=f"Price: {str(product[3])} | UUID: {product[0]} | Description: {product[4]}", inline=False)
                            return await interaction.response.send_message(embed=embed)
                pass
            case _:
                await interaction.response.send_message(embed=embedErrorFull)


async def setup(bot):
    await bot.add_cog(ManageProduct(bot))
