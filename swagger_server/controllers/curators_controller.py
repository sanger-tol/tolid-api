import connexion
import six

from swagger_server.models.public_name import PublicName  # noqa: E501
from swagger_server import util


def add_public_name(body=None):  # noqa: E501
    """adds a public name

    Adds a new public name to the system # noqa: E501

    :param body: Public name to add
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = PublicName.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
