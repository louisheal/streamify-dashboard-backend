import base64
import hashlib
import hmac
import os

SHOPIFY_SECRET = os.environ.get('SHOPIFY_SECRET')


def verify_webhook(data, hmac_header):
    digest = hmac.new(SHOPIFY_SECRET.encode('utf-8'), data, digestmod=hashlib.sha256).digest()
    computed_hmac = base64.b64encode(digest)

    return hmac.compare_digest(computed_hmac, hmac_header.encode('utf-8'))
