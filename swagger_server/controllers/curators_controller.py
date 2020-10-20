import connexion
import six
import os

# from swagger_server.models.public_name import PublicName 
# from swagger_server import util
from flask import jsonify
from swagger_server.file_utils import get_file_times, read_tsv, write_tsv
from swagger_server.db_utils import populate_db, get_db_cols_and_file_name, update_local_database, map_public_names_dict

db_file_name = 'public_names.db'
db_cols, tsv_pub_file_name, update_floats = get_db_cols_and_file_name(table_name='public_names')
unique_db_cols, tsv_unique_file_name, unique_update_floats = get_db_cols_and_file_name(table_name='unique_names')

def verify_database():  
    """verifies the integrigty of the local database
    :rtype: Verification message (str)
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

    :param taxonomy_id: valid NCBI Taxonomy identifier
    :type taxonomy_id: str
    :param specimen_id: valid GAL specimen identifier
    :type specimen_id: str

    :return: JSON with complete public name and taxa structure
    """

    public_names, new_public_name, q_species, specimen_id, pub_number, new_record = update_local_database(conn=None, cur=None, tax_id=taxonomy_id, specimen_id=specimen_id, print_all=True)

    if new_record:
        # Now, update the local tsv file with the new allocation
        file_df = read_tsv(file_name=tsv_unique_file_name, columns=unique_db_cols, update_floats=unique_update_floats)  # Read the TSV file
        # Adding a row. We need 'public_name', 'species', 'specimen_id', 'pub_number' for the new entry
        file_df.loc[-1] = [new_public_name, q_species, specimen_id, pub_number, None] 
        write_tsv(dataframe=file_df, file_name=tsv_unique_file_name)

    public_names_list = []
    if public_names:
        for row in public_names:
            name_dict = map_public_names_dict(data=row)
            public_names_list.append(name_dict)

    return jsonify(public_names_list)

