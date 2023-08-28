import logging
from flask import session, jsonify

from dao.users import user_dao

def get_session():
    username = session.get('username', None)
    display_name = session.get('display_name', None)
    avatar_url = session.get('avatar_url', None)

    if username is None:
        return jsonify(status='not_logged_in')

    user = user_dao.get_user(username, display_name, avatar_url)
    if user is None:
        logging.info(f"User {username} is not in the database")
        return jsonify(msg="You are not a Streamify affiliate - Contact @StreamifyStore on Twitter to learn more")

    logging.info(f"Found user {user.username}")
    return user.jsonify()
