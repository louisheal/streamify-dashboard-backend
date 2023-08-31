import logging
from flask import session, jsonify

from dao.users import user_dao

def get_user_data():
    username = session.get('username', None)
    display_name = session.get('display_name', None)
    avatar_url = session.get('avatar_url', None)

    if username is None:
        return jsonify(status='logged_out')

    user = user_dao.get_user(username, display_name, avatar_url)
    if user is None:
        logging.info(f"User {username} is not in the database")
        return jsonify(status="login_failed")

    logging.info(f"Found user {user.username}")
    return user.jsonify()
