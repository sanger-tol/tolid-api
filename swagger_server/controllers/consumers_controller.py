import connexion
import six
import json

from swagger_server.models.public_name import PublicName  # noqa: E501
from swagger_server import util
from flask import jsonify
from swagger_server.utilities.db_utils import get_db, populate_db, query_local_database


def search_public_name(search_string=None, skip=None, limit=None):  # noqa: E501
    """searches DToL public names

    By passing in the appropriate options, you can search for available public names in the system  # noqa: E501

    :param search_string: pass an optional search string for looking up a public name
    :type search_string: str
    :param skip: number of records to skip for pagination
    :type skip: int
    :param limit: maximum number of records to return
    :type limit: int

    :rtype: List[PublicName]
    """

    # ToDo
    # If database:
    #     search for string, return public_name array
    # else:
    #     download file from repo
    #     create sqlite3 database 
    #     search for string, return public_name array

    if not search_string:
        return 'Please provide a term to search for'

    if search_string == 'force_database_rebuild':  # ToDo, implement a server startup check
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

    # Normal search string passed as input parameter
    try:
        conn, cur = get_db(conn=None)
    except Exception as e:
        print('Database connection failed. Error: ' + str(e))
        return str(e)

    try:
        public_names = query_local_database(conn=conn, cur=cur, query_str=search_string, print_all=False)
    except Exception as e:
        print('Database Query failed. Error: ' + str(e))
        return str(e)
    
    public_names_list = []
    if public_names:
        for row in public_names:
            #json_row = jsonify(row)
            name_dict = map_public_names_dict(row)
            public_names_list.append(name_dict)

    return jsonify({"data": public_names_list})

def isMissing(data=None, query_type=None):
    if data and data.lower() == 'none':
        # ToDo, query NCBI/OLS for missing data and type
        return ""
    return data

def map_public_names_dict(data):
    # Database columns ['prefix', 'species', 'taxid', 'common_name', 'genus', 'family', 'tax_order', 'class', 'phylum']
    # prefix is the public name
    d = {'prefix': data[0], 
         'species': isMissing(data=data[1], query_type='species'), 
         'taxid': data[2], 
         'common_name': isMissing(data=data[3], query_type='common_name'), 
         'genus': isMissing(data=data[4], query_type='genus'), 
         'family': isMissing(data=data[5], query_type='family'), 
         'order': isMissing(data=data[6], query_type='order'), 
         'class': isMissing(data=data[7], query_type='class'), 
         'phylum': isMissing(data=data[8], query_type='phylum')}

    return d   

def map_public_names_class(data):
    # Database columns ['prefix', 'species', 'taxid', 'common_name', 'genus', 'family', 'tax_order', 'class', 'phylum']
    pname = PublicName
    pname.prefix = data[0]
    pname.species = data[1]
    pname.tax_id = data[2]
    pname.common_name = data[3]
    pname.genus = data[4]
    pname.family = data[5]
    pname.order = data[6]
    pname.taxa_class = data[7]
    pname.prefix = data[8]
    return pname    
