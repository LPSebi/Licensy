from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
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
app.add_middleware(SessionMiddleware,
                   secret_key=os.getenv("CUSTOM_SECRET_KEY"))
limiter = Limiter(key_func=get_remote_address, default_limits=["5/1second"])
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


def rateLimitHandler(request: Request, exc: RateLimitExceeded):
    response = JSONResponse(
        {"error": f"Rate limit exceeded: {exc.detail}"}, status_code=429
    )
    response = request.app.state.limiter._inject_headers(
        response, request.state.view_rate_limit
    )
    print(request.state.view_rate_limit)
    response = templates.TemplateResponse(
        "rate_limit.html", {'request': request, 'code': 429, 'message': response}, status_code=429)
    return response


app.add_exception_handler(RateLimitExceeded, rateLimitHandler)


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
    async with aiohttp.ClientSession() as session, session.post(DISCORD_API_ENDPOINT + "/oauth2/token", data=data, headers=headers) as resp:
        resp.raise_for_status()
        print(await resp.json())
        return await resp.json()

# GENERAL PART


@app.get('/licensy')
async def info_route():
    return 'Licensy is a discord bot that allows you to manage custom licenses'


@app.get('/licensy/tos')
async def tos_route():
    return 'Terms of Service'


@app.get('/licensy/privacy')
async def privacy_route():
    return 'Privacy Policy'


@app.get('/licensy/login')
async def login_route(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@app.get('/licensy/cb')
@limiter.limit("5/60second")
async def cb_route(request: Request, code: str):
    # get token
    token = (await exchange_code(request, code))['access_token']
    # write token to session
    request.session['token'] = token
    return RedirectResponse('/licensy/dashboard')


@app.get('/licensy/dashboard')
@limiter.limit("5/10second")
async def dashboard_route(request: Request):
    if 'token' not in request.session:
        return RedirectResponse(DISCORD_OAUTH2_URL)
    user_guilds = await get_user_guilds(request.session['token'])
    if user_guilds == "rate limited":
        return templates.TemplateResponse(
            "rate_limit.html", {'request': request, 'code': 429}, status_code=429)
    bot_guilds = await get_bot_guilds()
    mutual_guilds = await get_mutual_guilds(user_guilds, bot_guilds)
    print(request.session['token'])
    print(mutual_guilds)
    return templates.TemplateResponse('dashboard.html', {'request': request, 'guilds': mutual_guilds})


@app.get('/licensy/guild/{guild_id}')
async def guild_route(request: Request, guild_id: str):
    if 'token' not in request.session:
        return RedirectResponse(DISCORD_OAUTH2_URL)
    if await check_self_permission(request.session['token'], guild_id) != True:
        return RedirectResponse(LOGIN_PAGE_URL)
    guild_data = await get_guild_data(guild_id)
    if guild_data is None:
        return RedirectResponse('/licensy/dashboard')
    products = await get_products(guild_id)
    return templates.TemplateResponse('guild.html', {'request': request, 'guild': guild_data, 'products': products, 'token': request.session['token']})

# API PART


@app.delete('/licensy/api/delete_product/{uuid}/{token}')
@limiter.limit("5/10second")
async def delete_product_route(request: Request, uuid: str, token: str):
    print(uuid)
    print(token)
    guild_id = await get_guildId_from_product_uuid(uuid)
    if guild_id is None:
        return JSONResponse({'error': 'Product not found', 'code': 404}, status_code=404)
    is_token_allowed = await check_self_permission(token, guild_id)
    print(is_token_allowed)
    print(guild_id)
    if is_token_allowed is False:
        return JSONResponse({'error': 'Forbidden', 'code': 403}, status_code=403)
    elif is_token_allowed == "rate limited":
        return templates.TemplateResponse("rate_limit.html", {'request': request, 'code': 429}, status_code=429)
    if await delete_product(uuid) == "not found":
        return JSONResponse({"error": "Product not found"}, status_code=404)
    else:
        return JSONResponse({"success": "Product deleted"}, status_code=200)


# @app.get("/test")
# async def _test_route(request: Request):
#    if 'token' not in request.session:
#        return RedirectResponse(DISCORD_OAUTH2_URL)
#    return await check_self_permission(request.session['token'], 981576035176964117)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=80)
