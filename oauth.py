from aiohttp import web
from aiohttp_session import get_session
from aioauth_client import DiscordClient
from urllib.parse import quote

import config


routes = web.RouteTableDef()


def requires_login(handler):
    async def check_login(request, *args, **kwargs):
        session = await get_session(request)
        if session.get("user") is None:
            raise web.HTTPFound("/login")

        request["user"] = session["user"]

        return await handler(request)

    return check_login


@routes.get("/login")
async def _login(request):
    session = await get_session(request)
    if request.query.get("code") is None:
        print("asasd")
        raise web.HTTPFound(
            f"https://discordapp.com/api/oauth2/authorize?client_id={config.client_id}&redirect_uri={quote(config.redirect_uri)}&response_type=code&scope=identify")

    code = request.query["code"]
    client = DiscordClient(
        client_id=config.client_id,
        client_secret=config.client_secret
    )
    try:
        session["token"] = await client.get_access_token(code=code,
                                                         redirect_uri=config.redirect_uri)

        session["user"] = await client.request("GET", "users/@me")
    except:
        raise web.HTTPFound("/login")

    raise web.HTTPFound("/")


@routes.get("/logout")
async def _logout(request):
    session = await get_session(request)
    session.pop("user", None)
    session.pop("token", None)

    raise web.HTTPFound("/")
