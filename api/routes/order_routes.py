from api import app
from api.controllers import order_controller as controller


@app.route('/order', methods=['POST'])
def add_order():
    return controller.add_order()


@app.route('/order_fake')
def order_fake():
    return controller.order_fake()
