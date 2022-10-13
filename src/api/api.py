from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse
import uvicorn
from utils.constants import *
from utils.utils import *
from dotenv import load_dotenv
import os
import aiohttp

load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="./src/api/templates")
app.mount("/static", StaticFiles(directory="./src/api/static"), name="static")
app.add_middleware(SessionMiddleware, secret_key="!secret")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


async def exchange_code(request: Request, code: str):
    data = {
        "client_id": DISCORD_CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": DISCORD_REDIRECT_URL,
        "scope": DISCORD_SCOPES
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(DISCORD_API_ENDPOINT + "/oauth2/token", data=data, headers=headers) as resp:
            resp.raise_for_status()
            print(await resp.json())
            return await resp.json()


@app.get('/licensy')
async def info():
    return 'Licensy is a discord bot that allows you to manage custom licenses'


@app.get('/licensy/tos')
async def tos():
    return 'Terms of Service'


@app.get('/licensy/privacy')
async def privacy():
    return 'Privacy Policy'


@app.get('/licensy/login')
async def login(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@app.get('/licensy/cb')
async def cb(request: Request, code: str):
    # get token
    token = (await exchange_code(request, code))['access_token']
    # write token to session
    request.session['token'] = token
    return RedirectResponse('/licensy/dashboard')


@app.get('/licensy/dashboard')
async def dashboard(request: Request):
    if 'token' not in request.session:
        return RedirectResponse(DISCORD_OAUTH2_URL)
    user_guilds = await get_user_guilds(request.session['token'])
    bot_guilds = await get_bot_guilds()
    mutual_guilds = await get_mutual_guilds(user_guilds, bot_guilds)
    print(request.session['token'])
    # print(user_guilds)
    # print(bot_guilds)
    print(mutual_guilds)
    return templates.TemplateResponse('dashboard.html', {'request': request, 'guilds': mutual_guilds})


@app.get('/licensy/guild/{guild_id}')
async def guild(request: Request, guild_id: str):
    if 'token' not in request.session:
        return RedirectResponse(DISCORD_OAUTH2_URL)
    guild_data = await get_guild_data(guild_id)
    if guild_data is None:
        return RedirectResponse('/licensy/dashboard')
    products = await get_products(guild_id)
    return templates.TemplateResponse('guild.html', {'request': request, 'guild': guild_data, 'products': products})


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80)
