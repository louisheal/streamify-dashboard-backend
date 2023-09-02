from api import app
from api.controllers import order_controller as controller


@app.route('/order', methods=['POST'])
def order():
    return controller.order()
