import connexion
import six
import os

from swagger_server.models.public_name import PublicName  # noqa: E501
from swagger_server import util
from swagger_server.utilities.file_utils import get_file_times
from swagger_server.utilities.db_utils import populate_db

db_file_name = 'public_names.db'
tsv_file_name = 'final_merged.txt'

def verify_database():  
    """verifies the integrigty of the local database

    :rtype: None
    """

    integrity_verified = False
    db_found = False
    source_file_found = False

    try:
        db_found = os.path.isfile(db_file_name)  # Database file exists
        source_file_found = os.path.isfile(tsv_file_name)  # TSV file with all public names exist
    except Exception as e:
        print(str(e))

    if db_found and source_file_found:
        # ToDo count rows in both
        db_file_time, db_raw_time = get_file_times(directory='.', file_name=db_file_name)
        tsv_file_time, tsv_raw_time = get_file_times(directory='.', file_name=tsv_file_name)
        integrity_verified = True
        print('TSV timestamp: ' + tsv_file_time)
        print('DB timestamp: ' + db_file_time)

        if tsv_raw_time > db_raw_time:  
            # The TSV file should not be newer than the database files, re-download and rebuild the database
            integrity_verified = False

    if not source_file_found:
        # ToDo curl the file
        source_file_found = os.path.isfile(tsv_file_name) 

    if not db_found or not integrity_verified:
        database_created = None
        row_count = 0
        conn = None
        try:
            database_created, row_count, conn = populate_db()
        except Exception as e:
            print('Database connection failed. Error: ' + str(e))
            return str(e)
        if database_created:
            return str(row_count) + ' rows added to the newly created local database, please try a valid search term'


    return 'Database and TSV file validates!'


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
