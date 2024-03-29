from time import time
from typing import List
import discord
from discord.ext import commands
from discord import app_commands, ui
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
                         placeholder='Ex: 10 (Max 5 characters)', required=True, max_length=5, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            price = int(self.price.value)
        except ValueError:
            embed = discord.Embed(
                title=EMBED_ERROR_TITLE, description=EMBED_ERROR_INVALID_PRICE, color=EMBED_ERROR_COLOR)
            return await interaction.response.send_message(embed=embed)
        if int(price) < 0:
            embed = discord.Embed(
                title=EMBED_ERROR_TITLE, description="An error has occurred. Price must be a positive number.", color=EMBED_ERROR_COLOR)
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


class EditProductModal(ui.Modal, title='Edit Product'):
    """The modal for creating a product."""
    name = ui.TextInput(label='New name of your product',
                        placeholder='Ex: My product (Max 20 characters)', max_length=20, style=discord.TextStyle.short)
    description = ui.TextInput(
        label='New description of your product', placeholder='Ex: This Product does cool things (Max 100 characters)', style=discord.TextStyle.paragraph, required=False, max_length=100)
    price = ui.TextInput(label='Price of your product',
                         placeholder='Ex: 10 (Max 5 characters)', required=True, max_length=5, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            price = int(self.price.value)
        except ValueError:
            embed = discord.Embed(
                title=EMBED_ERROR_TITLE, description=EMBED_ERROR_INVALID_PRICE, color=EMBED_ERROR_COLOR)
            return await interaction.response.send_message(embed=embed)
        if int(price) < 0:
            embed = discord.Embed(
                title=EMBED_ERROR_TITLE, description="An error has occurred. Price must be a positive number.", color=EMBED_ERROR_COLOR)
            return await interaction.response.send_message(embed=embed)
        async with aiosqlite.connect('./data/db.sqlite') as db:
            current_guild = await db.execute('SELECT * FROM guilds WHERE id = ?', (interaction.guild.id,))
            guild_uuid = (await current_guild.fetchone())[0]
            await db.execute('INSERT INTO products (uuid, guild_uuid, name, price, description, date) VALUES (?, ?, ?, ?, ?, ?)',
                             (str(uuid.uuid4()), guild_uuid, self.name.value, int(self.price.value), self.description.value, int(round(time()))))
            await db.commit()
            return await interaction.response.send_message(f'Thanks for your response, {interaction.user.name}!', ephemeral=True)


class Confirm(ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @ui.button(label='Confirm', style=discord.ButtonStyle.red)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title=EMBED_CONFIRMED_TITLE,
                              description=EMBED_CONFIRMED_DESCRIPTION, color=EMBED_CONFIRMED_COLOR)

        self.value = True
        for i in self.children:
            i.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(embed=embed, ephemeral=True)
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title=EMBED_CANCELED_TITLE,
                              description=EMBED_CANCELED_DESCRIPTION, color=EMBED_CANCELED_COLOR)
        self.value = False
        for i in self.children:
            i.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(embed=embed, ephemeral=True)
        self.stop()


@app_commands.guild_only()
class ManageProduct(commands.GroupCog, name="product"):

    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    async def product_autocomplete(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice]:
        async with aiosqlite.connect('./data/db.sqlite') as db:
            current_guild = await db.execute('SELECT * FROM guilds WHERE id = ?', (interaction.guild.id,))
            guild_uuid = (await current_guild.fetchone())[0]
            products = await db.execute('SELECT * FROM products WHERE guild_uuid = ?', (guild_uuid,))
            products = await products.fetchall()
            choices = []
            for product in products:
                choices.append([product[2], product[0]])
            return [
                app_commands.Choice(
                    name=choice[0], value=choice[1]
                )
                for choice in choices
            ]

    # create product
    @app_commands.command(name='create', description='Create a product for your server')
    async def create_product(self, interaction: discord.Interaction):
        async with aiosqlite.connect('./data/db.sqlite') as db:
            cursor = await db.execute(
                "SELECT * FROM guilds WHERE id = ?", (interaction.guild.id,))
            product_count = await db.execute("SELECT COUNT(*) FROM products WHERE guild_uuid = (SELECT uuid FROM guilds WHERE id = ?)", (interaction.guild.id,))
            product_count = await product_count.fetchone()
            if await cursor.fetchone() is None:
                embed = discord.Embed(
                    title=EMBED_ERROR_TITLE, description=EMBED_ERROR_DESCRIPTION_NOT_INITIALIZED, color=EMBED_ERROR_COLOR)
                await db.close()
                return await interaction.response.send_message(embed=embed)
            # TODO: Set product limit !DONE!
            elif product_count[0] >= PRODUCT_LIMIT:
                embed = discord.Embed(
                    title=EMBED_ERROR_TITLE, description=EMBED_ERROR_DESCRIPTION_MAX_PRODUCTS, color=EMBED_ERROR_COLOR)
                return await interaction.response.send_message(embed=embed)

            else:
                return await interaction.response.send_modal(CreateProductModal())

    @app_commands.autocomplete(product=product_autocomplete)
    @app_commands.command(name='edit', description='Edit a product for your server')
    async def edit_product(self, interaction: discord.Interaction, product: str):
        async with aiosqlite.connect('./data/db.sqlite') as db:
            cursor = await db.execute(
                "SELECT * FROM guilds WHERE id = ?", (interaction.guild.id,))
            if await cursor.fetchone() is None:
                embed = discord.Embed(
                    title=EMBED_ERROR_TITLE, description=EMBED_ERROR_DESCRIPTION_NOT_INITIALIZED, color=EMBED_ERROR_COLOR)
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
                        title=EMBED_ERROR_TITLE, description="There are no products to edit.", color=EMBED_ERROR_COLOR)
                    await db.close()
                    return await interaction.response.send_message(embed=embed)
                else:
                    return await interaction.response.send_modal(EditProductModal())

    @app_commands.autocomplete(product=product_autocomplete)
    @app_commands.command(name='delete', description='Delete a product for your server')
    async def delete_product(self, interaction: discord.Interaction, product: str):
        view = Confirm()
        await interaction.response.send_message('Are you sure you want to delete this product?', view=view)
        await view.wait()
        if view.value is None:
            await interaction.response.send_message('You did not respond in time.', ephemeral=True)
        elif view.value:
            async with aiosqlite.connect('./data/db.sqlite') as db:
                cursor = await db.execute(
                    "SELECT * FROM guilds WHERE id = ?", (interaction.guild.id,))
                if await cursor.fetchone() is None:
                    embed = discord.Embed(
                        title=EMBED_ERROR_TITLE, description=EMBED_ERROR_DESCRIPTION_NOT_INITIALIZED, color=EMBED_ERROR_COLOR)
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
                            title=EMBED_ERROR_TITLE, description="There are no products to delete.", color=EMBED_ERROR_COLOR)
                        await db.close()
                        return await interaction.response.send_message(embed=embed)
                    else:
                        await db.execute('DELETE FROM products WHERE uuid = ?', (product,))
                        await db.commit()

    @app_commands.command(name='list', description='List all products for your server')
    async def list_products(self, interaction: discord.Interaction):
        async with aiosqlite.connect('./data/db.sqlite') as db:
            cursor = await db.execute('SELECT * FROM guilds WHERE id = ?', (interaction.guild.id,))
            if await cursor.fetchone() is None:
                embed = discord.Embed(
                    title=EMBED_ERROR_TITLE, description=EMBED_ERROR_DESCRIPTION_NOT_INITIALIZED, color=EMBED_ERROR_COLOR)
                return await interaction.response.send_message(embed=embed)
            else:
                current_guild = await db.execute('SELECT * FROM guilds WHERE id = ?', (interaction.guild.id,))
                guild_uuid = (await current_guild.fetchone())[0]
                cursor = await db.execute('SELECT * FROM products WHERE guild_uuid = ?', (guild_uuid,))
                products = await cursor.fetchall()
                if len(products) == 0:
                    embed = discord.Embed(
                        title=EMBED_ERROR_TITLE, description="There are no products to list.", color=EMBED_ERROR_COLOR)
                    return await interaction.response.send_message(embed=embed)
                else:
                    embed = discord.Embed(
                        title=EMBED_SUCCESS_TITLE, description="Here is the list of all products.", color=EMBED_SUCCESS_COLOR)
                    for product in products:
                        embed.add_field(
                            name=f"{product[2]}", value=f"Price: **{str(product[3])}** | Description: **{product[4]}**", inline=False)
                    return await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(ManageProduct(bot))
