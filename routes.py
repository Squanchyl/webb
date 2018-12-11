from aiohttp import web

from oauth import requires_login


routes = web.RouteTableDef()


@routes.post("/test")
async def test(request):
    data = await request.get_json()
    print(data)

    row = await request.app.pool.fetchrow("""SELECT * from ECONOMY WHERE ID = $1""", int(data["useid"]))
    return web.json_response({"Cash": row['cash']})


@routes.get("/channels")
@requires_login
async def test2(request):
    token = "token"
    headers = {
        'Authorization': f'Bot {token}'
    }
    response = await request.app.http.get("https://discordapp.com/api/guilds/178245179436695553/channels", headers=headers)
    ra = await response.json()
    return web.json_response(ra)


@routes.get("/me")
@requires_login
async def _me(request):
    user = request["user"]  # This only works in routes that have the "requires_login" decorator!!!
    return web.json_response(user)


@routes.get("/")
async def _index(request):
    return web.Response(text="Hallo :)")
