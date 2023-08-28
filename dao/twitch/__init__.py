import os

from config import config
from .twitch_api import TwitchApi

client_id = config.CLIENT_ID
client_secret = os.environ.get('CLIENT_SECRET')
redirect_uri = config.REDIRECT_URI

twitch_api = TwitchApi(client_id, client_secret, redirect_uri)
