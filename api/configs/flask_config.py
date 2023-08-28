from datetime import timedelta

from config import config

class FlaskConfig:
    DEBUG = True
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_DOMAIN = config.COOKIE_DOMAIN
