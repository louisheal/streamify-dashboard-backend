import secrets
import logging

from flask import session, redirect, jsonify, request

from dao.twitch import twitch_api as Twitch

class AuthController:
    def __init__(self, frontend_url):
        self.frontend_url = frontend_url

    def twitch_auth(self):
        state = secrets.token_hex(16)
        session['oauth_state'] = state
        return redirect(Twitch.get_auth_url(state))

    def callback(self):
        response_state = request.args.get('state')
        expected_state = session.pop('oauth_state', None)
        if response_state is None or response_state != expected_state:
            logging.critical("Endpoint /callback accessed with incorrect state")
            return jsonify(msg="State mismatch error"), 400

        code = request.args.get('code')
        if not code:
            logging.critical("Endpoint /callback accessed without code")
            return jsonify(msg="Missing code parameter"), 400

        twitch_user =Twitch.get_user(code)
        if twitch_user is None:
            logging.critical("Endpoint /callback accessed with invalid code")
            return jsonify(msg="Invalid Twitch access token"), 401

        session['username'] = twitch_user.username
        session['display_name'] = twitch_user.display_name
        session['avatar_url'] = twitch_user.avatar_url

        logging.info(f"User {twitch_user.username} has successfully logged in")
        return redirect(self.frontend_url)
    
    def logout(self):
        username = session.pop('username', None)
        session.pop('display_name', None)
        session.pop('avatar_url', None)

        logging.info(f"{username} has been logged out")
        return jsonify(status=f'{username}_logged_out')
