#!/usr/bin/env python3

import connexion
import os

from swagger_server import encoder
from swagger_server.model import db


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Tree of Life public name API'}, pythonic_params=True)
    app.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URI']
    app.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app.app)
    app.run(port=8080)


if __name__ == '__main__':
    main()
