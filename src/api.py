from flask import Flask

flask = Flask(__name__)


@flask.route('/licensy')
def info():
    return 'Licensy is a discord bot that allows you to manage custom licenses'


@flask.route('/licensy/tos')
def tos():
    return 'Terms of Service'


@flask.route('/licensy/privacy')
def privacy():
    return 'Privacy Policy'


flask.run()
