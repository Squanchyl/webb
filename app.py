import asyncpg
from aiohttp import web, ClientSession
import aiohttp_session as sessions
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet
import base64

from routes import routes
import oauth

# api.debug = True
# api.config['SECRET_KEY'] = OAUTH2_CLIENT_SECRET


class App(web.Application):
    def __init__(self):
        super().__init__()
        self.on_startup.append(self.prepare)

    async def prepare(self, app):
        self.http = ClientSession(loop=self.loop)

        sessions.setup(app, EncryptedCookieStorage(
            base64.urlsafe_b64decode(fernet.Fernet.generate_key())))  # It's better to save that somewhere or everyone will get logged out after restarting the server

        credentials = {"user": "user", "password": "password",
                       "database": "database", "host": "82.165.207.55"}
        # self.pool = await asyncpg.create_pool(**credentials, command_timeout=1)

        self.add_routes(routes)
        self.add_routes(oauth.routes)


if __name__ == '__main__':
    app = App()
    web.run_app(app, port=5000)
