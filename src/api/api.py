from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get('/licensy')
async def info():
    return 'Licensy is a discord bot that allows you to manage custom licenses'


@app.get('/licensy/tos')
async def tos():
    return 'Terms of Service'


@app.get('/licensy/privacy')
async def privacy():
    return 'Privacy Policy'

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
