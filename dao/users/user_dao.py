import logging

from api import mongo
from .user import User
from dao.orders.order import Order


def get_user(user_id):
    logging.info(f"Retrieving info for {user_id} from database")
    user = mongo.db.users.find_one({'user_id': user_id})
    return User(
        user['user_id'],
        user['display_name'],
        user['avatar_url'],
        user['discount_code'],
        user['discount_amount'],
        __parse_orders(user['orders']),
        user['payouts'],
        user['is_affiliate']
    ) if user else None


def create_user(user_id: str, display_name: str, avatar_url: str) -> None:
    mongo.db.users.update_one(
        {'user_id': user_id},
        {
            "$set": {
                'display_name': display_name,
                'avatar_url': avatar_url
            },
            "$setOnInsert": {
                'discount_code': None,
                'discount_amount': 0.00,
                'orders': [],
                'payouts': [],
                'is_affiliate': False
            }
        },
        upsert=True
    )


def __parse_orders(order_objects: [object]) -> [Order]:
    orders = []
    for order_object in order_objects:
        order = Order(order_object['amount'], order_object['order_date'])
        orders.append(order)
    return orders
