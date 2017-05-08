#!/usr/bin/env python
# date: 5/5/2017
# author: Tasuku Miura

import os
from flask import Flask, g, request
from views import view

configpath = os.path.expanduser('~')
MEDIA_BANK_PATH = "{}/media".format(configpath)


def init_app():
    app = Flask(__name__)
    app.config.update(dict(
        MEDIAFOLDER=MEDIA_BANK_PATH,
        DEBUG=True
    ))

    app.register_blueprint(view)
    return app

if __name__ == '__main__':
    app = init_app()
    app.run(host='0.0.0.0', port=5050)
