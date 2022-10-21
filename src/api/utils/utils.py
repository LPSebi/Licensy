
from utils.constants import *
from aiocache import cached
from api import BOT_TOKEN
import aiohttp
import aiosqlite


async def get_user_guilds(token: str):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    async with aiohttp.ClientSession() as session, session.get(DISCORD_API_ENDPOINT + "/users/@me/guilds", headers=headers) as resp:
        if resp.status == 429:
            return "rate limited"
        return await resp.json()


async def get_bot_guilds():
    headers = {
        "Authorization": f"Bot {BOT_TOKEN}"
    }
    async with aiohttp.ClientSession() as session, session.get(DISCORD_API_ENDPOINT + "/users/@me/guilds", headers=headers) as resp:
        if resp.status == 429:
            return "rate limited"
        return await resp.json()


@cached(ttl=550)
async def get_mutual_guilds(user_guilds: list, bot_guilds: list):
    return [guild for guild in user_guilds if guild['id'] in map(lambda i: i['id'], bot_guilds) and (int(guild['permissions']) & 0x20) == 0x20]


async def get_guild_data(guild_id: int):
    async with aiohttp.ClientSession() as session, session.get(DISCORD_API_ENDPOINT + f"/guilds/{guild_id}", headers={"Authorization": f"Bot {BOT_TOKEN}"}) as resp:
        if resp.status != 200:
            return None
        else:
            return await resp.json()


async def get_products(guild_id: int):
    async with aiosqlite.connect('./data/db.sqlite') as db:
        cursor = await db.execute('SELECT * FROM guilds WHERE id = ?', (guild_id,))
        if await cursor.fetchone() is None:
            return "not init"
        else:
            current_guild = await db.execute('SELECT * FROM guilds WHERE id = ?', (guild_id,))
            guild_uuid = (await current_guild.fetchone())[0]
            cursor = await db.execute('SELECT * FROM products WHERE guild_uuid = ?', (guild_uuid,))
            products = await cursor.fetchall()
            if len(products) == 0:
                return products
            else:
                # success
                return products


async def delete_product(uuid: str):
    async with aiosqlite.connect('./data/db.sqlite') as db:
        cursor = await db.execute('SELECT * FROM products WHERE uuid = ?', (uuid,))
        if await cursor.fetchone() is None:
            return "not found"
        else:
            await db.execute('DELETE FROM products WHERE uuid = ?', (uuid,))
            await db.commit()
            return "success"


async def check_self_permission(token: str, guild_id: int):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    # request all guilds
    async with aiohttp.ClientSession() as session, session.get(DISCORD_API_ENDPOINT + "/users/@me/guilds", headers=headers) as resp:
        if resp.status == 429:
            return "rate limited"
        user_guilds = await resp.json()
        # check if the guild is in the list
        print(map(lambda i: i['id'], user_guilds))
        if not str(guild_id) in map(lambda i: i['id'], user_guilds):
            return False  # not in guild
        # check if the user has the permission
        elif not (int(list(filter(lambda i: i['id'] == str(guild_id), user_guilds))[0]['permissions']) & 0x20) == 0x20:
            return False  # no permission
        else:
            return True  # success
