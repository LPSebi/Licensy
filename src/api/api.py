from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from constants.constants import *
from dotenv import load_dotenv
import os
import aiohttp

load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="./src/api/templates")
app.mount("/static", StaticFiles(directory="./src/api/static"), name="static")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


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
    return await exchange_code(request, code)
    # return templates.TemplateResponse('cb.html', {'request': request})


async def exchange_code(request: Request, code: str):
    data = {
        "client_id": DISCORD_CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": DISCORD_REDIRECT_URL
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(DISCORD_API_ENDPOINT + "/oauth2/token", data=data, headers=headers) as resp:
            resp.raise_for_status()
            print(await resp.json())
            return await resp.json()


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80)
