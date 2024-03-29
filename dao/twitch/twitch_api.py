import os
import requests

from config import config
from .twitch_user import TwitchUser

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = config.REDIRECT_URI


def get_user(code: str) -> TwitchUser | None:
    token_response = requests.post('https://id.twitch.tv/oauth2/token', params={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
    }).json()

    access_token = token_response.get('access_token')
    if not access_token:
        return None

    user_response = requests.get('https://api.twitch.tv/helix/users', headers={
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {access_token}'
    }).json()

    user_data = user_response['data'][0]
    return TwitchUser(user_data['id'], user_data['display_name'], user_data['profile_image_url'])


def get_auth_url(state: str) -> str:
    return (f"https://id.twitch.tv/oauth2/authorize?client_id={CLIENT_ID}&force_verify=true&redirect_uri={REDIRECT_URI}"
            f"&response_type=code&scope=user:read:email&state={state}")
