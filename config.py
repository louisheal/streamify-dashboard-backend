import os

class Config:
    CLIENT_ID = "7ymgtul3j19tqstv5duu657yw3y854"
    DB_USER = "streamify-admin"

class DevelopmentConfig(Config):
    COOKIE_DOMAIN = "localhost"
    FRONTEND_URL = "http://localhost:3000"
    REDIRECT_URI = "http://localhost:5000/callback"

class ProductionConfig(Config):
    COOKIE_DOMAIN = ".streamifystore.com"
    FRONTEND_URL = "https://dashboard.streamifystore.com"
    REDIRECT_URI = "https://api.streamifystore.com/callback"

environment = os.environ.get('ENVIRONMENT')
config = ProductionConfig if environment == 'production' else DevelopmentConfig
