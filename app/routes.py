import json
import logging
import os
import secrets

from flask import jsonify, session, redirect, request

from . import app
from .dao import user_dao
from .dao import twitch_dao as twitch
from .utils import shopify_utils as shopify

FRONTEND_URL = os.environ.get('FRONTEND_URL')

@app.route('/auth/twitch')
def twitch_auth():
    state = secrets.token_hex(16)
    session['oauth_state'] = state
    return redirect(twitch.get_auth_url(state))

@app.route('/callback')
def callback():
    response_state = request.args.get('state')
    expected_state = session.pop('oauth_state', None)
    logging.critical(response_state)
    logging.critical(expected_state)
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

    session['username'] = twitch_user.username
    session['display_name'] = twitch_user.display_name
    session['avatar_url'] = twitch_user.avatar_url

    logging.info(f"User {twitch_user.username} has successfully logged in")
    return redirect(FRONTEND_URL)

@app.route('/session')
def get_session():
    username = session.get('username')
    display_name = session.get('display_name')
    avatar_url = session.get('avatar_url')

    if username is None:
        return jsonify(status='not_logged_in')

    user = user_dao.get_user(username, display_name, avatar_url)
    if user is None:
        logging.info(f"User {username} is not in the database")
        return jsonify(msg="You are not a Streamify affiliate - Contact @StreamifyStore on Twitter to learn more")

    logging.info(f"Found user {user.username}")
    return user.toJson()

@app.route('/logout')
def logout():
    username = session.pop('username', None)
    session.pop('display_name')
    session.pop('avatar_url')

    logging.info(f"{username} has been logged out")
    return jsonify(status=f'{username}_logged_out')

@app.route('/shopifyOrder', methods=['POST'])
def shopify_order():
    data = request.get_data()
    verified = shopify.verify_webhook(data, request.headers.get('X-Shopify-Hmac-SHA256'))

    if not verified:
        return "Invalid request", 401
    
    # Add order to MongoDB database

    return jsonify(msg="Order added successfully")

@app.route('/sessiondebug')
def session_debug():
    username = session.pop('username', None)
    displayName = session.pop('display_name')
    avatarUrl = session.pop('avatar_url')
    oauthState = session.pop('oauth_state')

    return jsonify(username, displayName, avatarUrl, oauthState)
