import os

import requests

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
SCOPE = "user:read:email"

def get_username(code):
    token_response = requests.post('https://id.twitch.tv/oauth2/token', params={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
    }).json()

    print(f"Client Id = {CLIENT_ID}")

    access_token = token_response.get('access_token')
    if not access_token:
        return None

    user_response = requests.get('https://api.twitch.tv/helix/users', headers={
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {access_token}'
    }).json()

    return user_response['data'][0]['login']

def get_auth_url(state):
    return f"https://id.twitch.tv/oauth2/authorize?client_id={CLIENT_ID}&force_verify=true&redirect_uri={REDIRECT_URI}&response_type=code&scope={SCOPE}&state={state}"
