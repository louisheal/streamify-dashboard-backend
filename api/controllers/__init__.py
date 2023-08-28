from .auth_controller import AuthController
from config import config

frontend_url = config.FRONTEND_URL

auth_controller = AuthController(frontend_url)
