from connexion.apps.flask_app import FlaskJSONEncoder
from swagger_server.model import Base


class JSONEncoder(FlaskJSONEncoder):
    include_nulls = False

    def default(self, o):
        if isinstance(o, Base):
            return o.to_dict()
        return FlaskJSONEncoder.default(self, o)
