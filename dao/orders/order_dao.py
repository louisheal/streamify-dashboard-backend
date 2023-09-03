import logging
from datetime import datetime

from api import mongo
from .order import Order


def add_order(user_id: str, order: Order) -> None:
    logging.info(f"Adding order of amount {order.amount} to user {user_id}")
    mongo.db.users.update_one(
        {'user_id': user_id},
        {
            "$push": {
                'orders': order.to_json()
            }
        }
    )


def add_fake_order():
    user_id = "83125762"
    order = Order(49, datetime(2023, 8, 31))
    mongo.db.users.update_one(
        {'user_id': user_id},
        {
            "$push": {
                'orders': order.to_json()
            }
        }
    )
