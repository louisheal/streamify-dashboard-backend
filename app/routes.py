import json
import logging
import os
import secrets

from flask import jsonify, session, redirect, request

from . import app
from .dao import user_dao
from .utils import twitch_utils as twitch

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
    if response_state is None or response_state != expected_state:
        logging.critical("Endpoint /callback accessed with incorrect state")
        return jsonify(msg="State mismatch error"), 400

    code = request.args.get('code')
    if not code:
        logging.critical("Endpoint /callback accessed without code")
        return jsonify(msg="Missing code parameter"), 400

    username = twitch.get_username(code)
    if username is None:
        logging.critical("Endpoint /callback accessed with invalid code")
        return jsonify(msg="Invalid Twitch access token"), 401

    session['username'] = username
    logging.info(f"User {username} has successfully logged in")
    return redirect(FRONTEND_URL)

@app.route('/session')
def get_session():
    print(session.get('username'))
    username = session.get('username')
    if username is None:
        logging.info("No username set")
        return jsonify(status='No username provided')

    logging.info(f"Retrieving info for {username} from database")
    user = user_dao.get_user(username)
    if user is None:
        logging.info(f"User {username} is not in the database")
        return jsonify(msg="User is not a streamify affiliate")

    logging.info(f"Found user {user.username}")
    return json.dumps(user.__dict__)

@app.route('/logout')
def logout():
    username = session.get('username')
    session.pop('username', None)
    logging.info(f"{username} has been logged out")
    return jsonify(status=f'{username}_logged_out')
