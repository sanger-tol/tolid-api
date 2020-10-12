import connexion
import six
import json

from swagger_server.models.public_name import PublicName  
from swagger_server import util
from flask import jsonify
from swagger_server.db_utils import get_db, populate_db, query_local_database


def search_public_name(taxonomy_id=None, specimen_id=None, skip=None, limit=None):  
    """searches DToL public names

    By passing in the appropriate taxonomy string, you can search for available public names in the system 

    :param taxonomyId: pass an optional search string for looking up a public name
    :type taxonomyId: str
    # :param skip: number of records to skip for pagination
    # :type skip: int
    # :param limit: maximum number of records to return
    # :type limit: int

    :rtype: List[PublicName]
    """

    # If database:
    #     search for string, return public_name array
    # else:
    #     download file from repo
    #     create sqlite3 database 
    #     search for string, return public_name array

    if not taxonomy_id:
        return 'Please provide a taxon id to search for'

    if not specimen_id:
        return 'Please provide a GAL specimen id to search for'

    # Normal search string passed as input parameter
    try:
        conn, cur = get_db(conn=None)
    except Exception as e:
        print('Database connection failed. Error: ' + str(e))
        return str(e)

    try:
        public_names = query_local_database(conn=conn, cur=cur, tax_id=taxonomy_id, specimen_id=specimen_id, print_all=False)
    except Exception as e:
        print('Database Query failed. Error: ' + str(e))
        return str(e)
    
    public_names_list = []
    if public_names:
        for row in public_names:
            name_dict = map_public_names_dict(data=row)
            public_names_list.append(name_dict)

    return jsonify({"data": public_names_list})

def is_missing(data=None, query_type=None):
    if data and data.lower() == 'none':
        # ToDo, query NCBI/OLS for missing data and type
        return ""
    return data

def get_public_name(taxid=None, specimen_id=None):
    public_name = "None"  # ToDo
    return public_name

def map_public_names_dict(data=None, specimen_id=None):
    # Database columns ['prefix', 'species', 'taxid', 'common_name', 'genus', 'family', 'tax_order', 'class', 'phylum']
    # prefix is the first part of the public name
    # ToDo, change to generate a real public name. i.e. prefix + number
    taxid = data[2]
    d = {'prefix': data[0], 
         'species': is_missing(data=data[1], query_type='species'), 
         'taxid': taxid, 
         'common_name': is_missing(data=data[3], query_type='common_name'), 
         'genus': is_missing(data=data[4], query_type='genus'), 
         'family': is_missing(data=data[5], query_type='family'), 
         'order': is_missing(data=data[6], query_type='order'), 
         'class': is_missing(data=data[7], query_type='class'), 
         'phylum': is_missing(data=data[8], query_type='phylum'),
         'public_name': get_public_name(taxid=taxid, specimen_id=specimen_id)}

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
