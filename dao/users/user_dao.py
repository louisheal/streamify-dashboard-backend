import logging

from api import mongo
from .user import User

def get_user(username, display_name, avatar_url):
    logging.info(f"Retrieving info for {username} from database")
    user = mongo.db.users.find_one({'username': username})
    return User(
        username,
        display_name,
        avatar_url,
        user['discount_code'],
        user['discount_amount'],
        user['orders'],
        user['withdrawals']
    ) if user else None
