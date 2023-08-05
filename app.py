import os

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

CLIENT_ID = os.environ.get('CLIENT_ID')

def get_twitch_username(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Client-ID': CLIENT_ID
    }
    response = requests.get('https://api.twitch.tv/helix/users', headers=headers)

    if response.status_code != 200:
        return None

    return response.json().get('data', [{}])[0].get('login')

@app.route('/info', methods=['GET'])
def user_info():
    access_token = request.args.get('access_token')

    if not access_token:
        return jsonify({"msg": "Missing access_token parameter"}), 400

    twitch_username = get_twitch_username(access_token)
    if twitch_username is None:
        return jsonify({"msg": "Invalid Twitch access token"}), 401

    return jsonify(username=twitch_username), 200
