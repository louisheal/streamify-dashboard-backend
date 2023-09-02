import secrets
import logging

from flask import session, redirect, jsonify, request

from dao.twitch import twitch_api as twitch
from config import config
import dao.users.user_dao as user_dao

FRONTEND_URL = config.FRONTEND_URL


def twitch_auth():
    state = secrets.token_hex(16)
    session['oauth_state'] = state
    return redirect(twitch.get_auth_url(state))


def callback():
    response_state = request.args.get('state')
    expected_state = session.pop('oauth_state', None)
    if response_state is None or response_state != expected_state:
        logging.critical("Endpoint /callback accessed with incorrect state")
        return jsonify(msg="State mismatch error"), 400

    code = request.args.get('code')
    if not code:
        logging.critical("Endpoint /callback accessed without code")
        return jsonify(msg="Missing code parameter"), 400

    twitch_user = twitch.get_user(code)
    if twitch_user is None:
        logging.critical("Endpoint /callback accessed with invalid code")
        return jsonify(msg="Invalid Twitch access token"), 401

    session['user_id'] = twitch_user.user_id

    user_dao.create_user(twitch_user.user_id, twitch_user.display_name, twitch_user.avatar_url)

    logging.info(f"User {twitch_user.user_id} has successfully logged in")
    return redirect(FRONTEND_URL)


def logout():
    username = session.pop('username', None)
    session.pop('display_name', None)
    session.pop('avatar_url', None)

    logging.info(f"{username} has been logged out")
    return jsonify(status=f'{username}_logged_out')
