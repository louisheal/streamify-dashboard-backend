from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

url = "api.riotgames.com"
riot_header = {'X_Riot_Token':os.getenv('riot_token')}

@app.route('/valorant/v1/')
def home():
    args = request.args

    if 'region' not in args or invalid_region(str(args.get('region'))):
        return "Argument \"region\" is either missing or incorrect.", 400
    
    if 'username' not in args or invalid_username(str(args.get('username'))):
        return "Argument \"username\" is either missing or incorrect.", 400
    
    if 'tagline' not in args or invalid_tagline(str(args.get('tagline'))):
        return "Argument \"tagline\" is either missing or incorrect.", 400

    region, username, tagline = str(args.get['region']).toLower(), str(args.get['username']), str(args.get['tagline'])

    puuid = requests.get(f"https://{region}.{url}/riot/account/v1/accounts/by-riot-id/{username}/{tagline}", headers=riot_header)

    try:
        puuid = puuid.json()['puuid']
    except Exception:
        return "Invalid arguments entered.", 401
    
    response = requests.get(f"https://{region}.{url}/val/match/v1/matchlists/by-puuid/{puuid}", headers=riot_header)
    print(response.text)
    print(response.json())
    return response.json(), 200

def invalid_region(region):
    return region.toLower() not in ['americas','asia','esports','europe']

def invalid_username(username):
    return not username.isalnum()

def invalid_tagline(tagline):
    return len(tagline) != 4 or tagline.isalnum()
