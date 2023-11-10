import logging
from flask import session, jsonify, request

from dao.users import user_dao


def get_user_data():
    user_id = session.get('user_id', None)

    if user_id is None:
        logging.debug("No user associated with session")
        return jsonify(status='logged_out')

    user = user_dao.get_user(user_id)
    if user is None:
        logging.info(f"User {user_id} is not in the database")
        return jsonify(status='login_failed')

    logging.info(f"Found user {user.display_name}")
    return user.jsonify()

def print_body():
    data = request.data.decode()
    print(data)
    return "Success", 200
