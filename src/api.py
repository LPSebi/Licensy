from flask import Flask

flask = Flask(__name__)


@flask.route('/licensy')
def info():
    return 'Licensy is a discord bot that allows you to manage custom licenses'


flask.run()
