from flask import Flask
from flask_cors import CORS
from flask_restful_swagger_3 import Api, swagger
from swagger_client.api import consumers_api
from swagger_client.models import PublicName
from utils.file_utils import read_tsv
from utils.db_utils import get_db

import sys
import connexion

db = get_db(db=None) # To store public names loaded from https://gitlab.com/wtsi-grit/darwin-tree-of-life-sample-naming

servers = [{"url": "http://localhost:5000"}]

# app = connexion.FlaskApp("ToL Public name registry", specification_dir='openapi/')
#     app.add_api(specification='public-name.yaml')

# def create_api(app, HOST="localhost", PORT=5000, API_PREFIX=""):
#     api = Api(app, version='1', servers=servers, api_spec_url='/api/swagger')
#     api.add_resource(PublicName, '/api/public-name')
#     print("Starting API: http://{}:{}/{}".format(HOST, PORT, API_PREFIX))

# def create_app(config_filename=None, host="localhost"):
#     #app = Flask("ToL Public name registry")
#     app.config.update(SQLALCHEMY_DATABASE_URI="sqlite://")
#     db.init_app(app)
#     CORS(app)

#     with app.app_context():
#         db.create_all()
#         # Populate the db with public names

#         df = read_tsv(file_name="/Users/kh14/Sanger/Dev/darwin-tree-of-life-sample-naming/final_merged.txt")
#         row_count = df.shape[0]  # gives number of row count
#         col_count = df.shape[1]  # gives number of col count
#         # for i in range(row_count):
#             # public_names = PublicName(
#             #     prefix=None, species=None, tax_id=None, 
#             #     common_name=None, genus=None, family=None, 
#             #     order=None, taxa_class=None, phylum=None)

#         create_api(app, host)
#     return app

# # address where the api will be hosted, change this if you're not running the app on localhost!
# host = sys.argv[1] if sys.argv[1:] else "127.0.0.1"
# app = create_app(host=host)

# if __name__ == '__main__':
#     app.run(debug=True, host=host)


app = connexion.FlaskApp("ToL Public name registry", specification_dir='openapi')
app.add_api(specification='public-name.yaml')
app.run(debug=True, port=8080)
