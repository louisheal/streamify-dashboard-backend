import json
import os

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import requests

CLIENT_ID = os.environ.get('CLIENT_ID')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

app = Flask(__name__)
app.config['MONGO_URI'] = f"mongodb+srv://{DB_USER}:{DB_PASS}@streamify.j2vdk73.mongodb.net/dashboard"
mongo = PyMongo(app)

@app.route('/sessionId', methods=['GET'])
def user_info():
    access_token = request.args.get('access_token')

    if not access_token:
        return jsonify({"msg": "Missing access_token parameter"}), 400

    twitch_username = get_twitch_username(access_token)
    if twitch_username is None:
        return jsonify({"msg": "Invalid Twitch access token"}), 401

    return jsonify(username=twitch_username), 200

@app.route('/info', methods=['GET'])
def get_user_info():
    streamer_name = request.args.get('streamer_name')
    print(streamer_name)
    user = get_user_by_streamer_name(streamer_name)
    return json.dumps(user.__dict__)

def get_twitch_username(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Client-ID': CLIENT_ID
    }
    response = requests.get('https://api.twitch.tv/helix/users', headers=headers)

    if response.status_code != 200:
        return None

    return response.json().get('data', [{}])[0].get('login')

def get_user_by_streamer_name(streamer_name):
    user = mongo.db.users.find_one({'streamer_name': streamer_name})
    return User(user['streamer_name'], user['discount_code'], user['discount_amount'], user['orders'], user['withdrawals'])

class User:
    
    def __init__(self, streamer_name, discount_code, discount_amount, orders, withdrawals):
        self.streamer_name   = streamer_name
        self.discount_code   = discount_code
        self.discount_amount = discount_amount
        self.orders          = orders
        self.withdrawals     = withdrawals
        self.balance         = self.__calculate_balance(orders)
    
    def __calculate_balance(self, orders):
        prices = [order['price_gbp'] for order in orders]
        return sum(prices)

if __name__ == '__main__':
    app.run()
