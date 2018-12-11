import os
from quart import Quart, request, url_for, jsonify, session, redirect
from requests_oauthlib import OAuth2Session
import asyncio
import asyncpg
from aiohttp import web
import aiohttp
from aiohttp_requests import requests
import datetime


# OAUTH2_CLIENT_ID = os.environ['OAUTH2_CLIENT_ID']
# OAUTH2_CLIENT_SECRET = os.environ['OAUTH2_CLIENT_SECRET']
# OAUTH2_REDIRECT_URI = 'http://localhost:5000/callback'

# API_BASE_URL = os.environ.get('API_BASE_URL', 'https://discordapp.com/api')
# AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
# TOKEN_URL = API_BASE_URL + '/oauth2/token'

api = Quart(__name__)

# api.debug = True
# api.config['SECRET_KEY'] = OAUTH2_CLIENT_SECRET




async def init_app():
    """Initialize the application server."""
    app = web.Application()
    credentials = {"user": "user", "password": "password", "database": "database", "host": "82.165.207.55"}
    app.pool = await asyncpg.create_pool(**credentials, command_timeout=1)
    return app




@api.route("/test", methods=['POST'])
async def test():
    data = await request.get_json()
    print(data)
    
    # print(data)
    row = await app.pool.fetchrow("""SELECT * from ECONOMY WHERE ID = $1""", int(data["useid"]))
    return jsonify({"Cash": row['cash']})
    
@api.route("/channels", methods=['GET'])
async def test2():
    token = "token"
    headers = {
    'Authorization': f'Bot {token}'
     }
    response = await requests.get("https://discordapp.com/api/guilds/178245179436695553/channels", headers = headers)
    #print(await response.json())
    ra = await response.json()
    return jsonify(ra)


     


loop = asyncio.get_event_loop()
app = loop.run_until_complete(init_app())

if __name__ == '__main__':
    api.run()
    web.run_app(app)


