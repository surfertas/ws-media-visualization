#!/usr/bin/env python
# date: 5/5/2017
# author: Tasuku Miura

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, g, request
from views import view

configpath = os.path.expanduser('~')
configdb = "user.db"
configschema = "schema.sql"
MEDIA_BANK_PATH = "{}/media".format(configpath)


def init_app(schema_uri, db_uri):
    app = Flask(__name__)

    app.config.update(dict(
        MEDIAFOLDER=MEDIA_BANK_PATH,
        SCHEMA=os.path.join(app.root_path, schema_uri),
        DATABASE=os.path.join(app.root_path, db_uri),
        DEBUG=True
    ))

    app.register_blueprint(view)
    return app

if __name__ == '__main__':
    app = init_app(configschema, configdb)
    app.run(host='0.0.0.0', port=5050)
