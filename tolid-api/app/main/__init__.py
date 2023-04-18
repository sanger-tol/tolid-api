#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

import os

import connexion

from main import encoder
from main.model import db


def application():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Tree of Life ToLID API'},
                pythonic_params=True)
    app.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URI']
    app.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True,
                                                   'pool_recycle': 1800}
    db.init_app(app.app)
    return app
