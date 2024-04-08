# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from flask import Response


def assert200(r: Response, *args):
    assert r.status_code == 200


def assert400(r: Response, *args):
    assert r.status_code == 400


def assert401(r: Response, *args):
    assert r.status_code == 401


def assert403(r: Response, *args):
    assert r.status_code == 403


def assert404(r: Response, *args):
    assert r.status_code == 404


def assertEqual(a, b, *args):
    assert a == b
