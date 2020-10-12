import connexion
import six
import os

from swagger_server.models.public_name import PublicName  # noqa: E501
from swagger_server import util
from swagger_server.file_utils import get_file_times
from swagger_server.db_utils import populate_db, get_db_cols_and_file_name

db_file_name = 'public_names.db'
db_cols, tsv_pub_file_name = get_db_cols_and_file_name(table_name='public_names')
db_cols, tsv_unique_file_name = get_db_cols_and_file_name(table_name='unique_names')

def verify_database():  
    """verifies the integrigty of the local database

    :rtype: None
    """

    integrity_verified = False
    db_found = False

    try:
        db_found = os.path.isfile(db_file_name)  # Database file exists
        source_file_pub_found = os.path.isfile(tsv_pub_file_name)  # TSV file with all public names exist
        source_file_unique_found = os.path.isfile(tsv_unique_file_name)  # TSV file with all allocated public names exist
    except Exception as e:
        print(str(e))

    if db_found and source_file_pub_found and source_file_unique_found:
        # ToDo count rows in both
        db_file_time, db_raw_time = get_file_times(directory='.', file_name=db_file_name)
        tsv_pub_file_time, tsv_pub_raw_time = get_file_times(directory='.', file_name=tsv_pub_file_name)
        tsv_unique_file_time, tsv_unique_raw_time = get_file_times(directory='.', file_name=tsv_pub_file_name)
        integrity_verified = True
        print('TSV pub timestamp: ' + tsv_pub_file_time)
        print('TSV unique timestamp: ' + tsv_unique_file_time)
        print('DB timestamp: ' + db_file_time)

        if tsv_pub_raw_time > db_raw_time or tsv_unique_raw_time > db_raw_time:  
            # The TSV files should not be newer than the database files, re-download and rebuild the database
            integrity_verified = False

    # if not source_file_found:
        # ToDo curl the file


    if not db_found or not integrity_verified:
        database_created = None
        row_count = 0
        try:
            database_created, row_count, conn = populate_db()
        except Exception as e:
            print('Database connection failed. Error: ' + str(e))
            return str(e)
        if database_created:
            return str(row_count) + ' rows added to the newly created local database, please try a valid search term'


    return 'Success: Database and TSV files validates'


def add_public_name(taxonomy_id=None, specimen_id=None): 
    """adds a public name

    Adds a new public name to the system 

    :param taxonomyId: valid NCBI Taxonomy identifier
    :type taxonomyId: str
    :param specimenId: valid GAL specimen identifier
    :type specimenId: str

    :rtype: String
    """
    # Todo
    # Check if we have already allocated a public name for this specimen:
    #   return existing id
    # else:
    #   Do we already have a public name for this taxa but not for this specimen:
    #       select the latest id number used (number after prefix)
    #   else
    #       allocate a new sequence = 1
    #  
    #   Select the existing prefix
    #   
    #   new public name = combine prefix and sequence
    #   add new public name and specimen into allocated id's file and database
    # 
    #   return new public name 


    return 'taxonomy_id='+ taxonomy_id
