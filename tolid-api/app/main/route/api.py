# SPDX-FileCopyrightText: 2022 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from flask import Blueprint

from flask_restx import Api, Namespace, Resource

from main.resource import api_species

from tol.api_base.auth import authorizations
from tol.api_base.resource import api_auth, api_environment, api_user


def _get_environment_string(app):
    environment = app.config['DEPLOYMENT_ENVIRONMENT']
    if environment == 'production':
        return ''
    return f' ({environment})'


def _setup_api(blueprint, app):
    api = Api(
        blueprint,
        doc='/ui',
        title=f'Tree of Life Workflows{_get_environment_string(app)}',
        authorizations=authorizations
    )
    api.add_namespace(api_environment)
    api.add_namespace(api_auth)
    api.add_namespace(api_species)


def init_blueprint(app):
    blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
    _setup_api(blueprint, app)
    return blueprint
