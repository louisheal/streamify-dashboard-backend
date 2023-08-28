from api import app
import api.controllers.user_controller as controller

@app.route('/session')
def get_session():
    return controller.get_session()
