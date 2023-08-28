import requests

from .twitch_user import TwitchUser

class TwitchApi:
    def __init__(self, client_id, client_secret, redirect_uri) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_user(self, code: str) -> TwitchUser:
        token_response = requests.post('https://id.twitch.tv/oauth2/token', params={
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri,
        }).json()

        access_token = token_response.get('access_token')
        if not access_token:
            return None

        user_response = requests.get('https://api.twitch.tv/helix/users', headers={
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {access_token}'
        }).json()

        user_data = user_response['data'][0]
        return TwitchUser(user_data['login'], user_data['display_name'], user_data['profile_image_url'])

    def get_auth_url(self, state: str) -> str:
        return f"https://id.twitch.tv/oauth2/authorize?client_id={self.client_id}&force_verify=true&redirect_uri={self.redirect_uri}&response_type=code&scope=user:read:email&state={state}"
