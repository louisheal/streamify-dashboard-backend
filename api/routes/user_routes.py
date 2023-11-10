from api import app
import api.controllers.user_controller as controller

@app.route('/userdata')
def get_user_data():
    return controller.get_user_data()

@app.route('/')
def index():
    return controller.print_body()
