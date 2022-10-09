from flask import Flask
import aiosqlite

flask = Flask(__name__)


@flask.get('/licensy')
async def info():
    return 'Licensy is a discord bot that allows you to manage custom licenses'


@flask.get('/licensy/tos')
async def tos():
    return 'Terms of Service'


@flask.get('/licensy/privacy')
async def privacy():
    return 'Privacy Policy'


flask.run()
