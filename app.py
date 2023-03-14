from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

url = "api.riotgames.com"
riot_header = {'X_Riot_Token':os.getenv('riot_token')}

@app.route('/valorant/v1/')
def home():
    args = request.args

    if 'region' not in args or valid_region(str(args.get('region')).lower()):
        return "Argument \"region\" is either missing or incorrect.", 400
    
    if 'username' not in args or valid_username(str(args.get('username'))):
        return "Argument \"username\" is either missing or incorrect.", 400
    
    if 'tagline' not in args or not valid_tagline(str(args.get('tagline'))):
        return "Argument \"tagline\" is either missing or incorrect.", 400

    region, username, tagline = str(args.get['region']).lower(), str(args.get['username']), str(args.get['tagline'])

    puuid = requests.get(f"https://{region}.{url}/riot/account/v1/accounts/by-riot-id/{username}/{tagline}", headers=riot_header)

    try:
        puuid = puuid.json()['puuid']
    except Exception:
        return "Invalid arguments entered.", 401
    
    response = requests.get(f"https://{region}.{url}/val/match/v1/matchlists/by-puuid/{puuid}", headers=riot_header)
    print(response.text)
    print(response.json())
    return response.json(), 200

def valid_region(region):
    return region in ['americas','asia','esports','europe']

def valid_username(username):
    return username.isalnum()

def valid_tagline(tagline):
    return len(tagline) == 4 and tagline.isdigit()
