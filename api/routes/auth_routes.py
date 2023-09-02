from api import app
from api.controllers import auth_controller as controller


@app.route('/auth/twitch')
def twitch_auth():
    return controller.twitch_auth()


@app.route('/callback')
def callback():
    return controller.callback()


@app.route('/logout')
def logout():
    return controller.logout()
