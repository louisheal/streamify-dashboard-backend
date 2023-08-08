import json

from flask import jsonify, request

from . import app
from .dao import user_dao
from .utils import twitch_utils as twitch

# Generate a session id from a Twitch access token
@app.route('/sessionId', methods=['GET'])
def user_info():
    access_token = request.args.get('access_token')

    if not access_token:
        return jsonify({"msg": "Missing access_token parameter"}), 400

    twitch_username = twitch.get_username(access_token)
    if twitch_username is None:
        return jsonify({"msg": "Invalid Twitch access token"}), 401

    return jsonify(username=twitch_username), 200

# Retrieve user info from database using session id
@app.route('/info', methods=['GET'])
def get_user_info():
    streamer_name = request.args.get('streamer_name')

    user = user_dao.get_user_by_streamer_name(streamer_name)
    return json.dumps(user.__dict__)