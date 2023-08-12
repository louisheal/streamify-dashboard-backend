from app import mongo
from .user import User

def get_user(username):
    user = mongo.db.users.find_one({'username': username})
    return User(user['username'], user['discount_code'], user['discount_amount'], user['orders'], user['withdrawals']) if user else None
