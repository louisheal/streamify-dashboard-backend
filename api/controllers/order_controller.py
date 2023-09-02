from flask import request, jsonify
from utils import shopify_utils as shopify


def order():
    data = request.get_data()
    verified = shopify.verify_webhook(data, request.headers.get('X-Shopify-Hmac-SHA256'))

    if not verified:
        return "Invalid request", 401
    
    # Add order to MongoDB database

    return jsonify(msg="Order added successfully")
