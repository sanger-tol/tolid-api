#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from flask import Flask

from main import encoder


def application():
    app = Flask(__name__)
    app.json_encoder = encoder.JSONEncoder

    return app
