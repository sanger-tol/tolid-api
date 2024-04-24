# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from flask import Flask


def application() -> Flask:
    app = Flask(__name__)

    @app.get('/')
    def get():
        return 'HELLO WORLD', 200

    return app
