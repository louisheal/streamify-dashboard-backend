import os

import requests

CLIENT_ID = os.environ.get('CLIENT_ID')

def get_username(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Client-ID': CLIENT_ID
    }
    response = requests.get('https://api.twitch.tv/helix/users', headers=headers)

    if response.status_code != 200:
        return None

    return response.json().get('data', [{}])[0].get('login')
