from app import mongo
from .user import User

# TODO: Add error handling when user not in db
def get_user_by_streamer_name(streamer_name):
    user = mongo.db.users.find_one({'streamer_name': streamer_name})
    return User(user['streamer_name'], user['discount_code'], user['discount_amount'], user['orders'], user['withdrawals'])
