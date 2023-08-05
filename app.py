import os

from flask import Flask, jsonify, request
from flask_dance.contrib.twitch import make_twitch_blueprint, twitch

app = Flask(__name__)

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

twitch_blueprint = make_twitch_blueprint(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

app.register_blueprint(twitch_blueprint)

@app.route("/")
def index():
    pass

@app.route("/twitchlogin")
def twitch_login():
    pass

@app.route("/userinfo")
def user_info():
    pass
