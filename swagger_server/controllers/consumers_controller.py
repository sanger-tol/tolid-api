import connexion
import six
import json

from swagger_server.models.public_name import PublicName  
from swagger_server import util
from flask import jsonify
from swagger_server.db_utils import get_db, populate_db, query_local_database, map_public_names_dict


def get_public_names(public_names_list=None, taxonomy_id=None, specimen_id=None, conn=None, cur=None):

    if not taxonomy_id:
        return 'Please provide a taxon id to search for'

    if not specimen_id:
        return 'Please provide a GAL specimen id to search for'

    if not conn or not cur:
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

    if public_names:
        for row in public_names:
            name_dict = map_public_names_dict(data=row)
            public_names_list.append(name_dict)

    return public_names_list

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
    public_names_list = []

    try:
        conn, cur = get_db(conn=None)
    except Exception as e:
        print('Database connection failed. Error: ' + str(e))
        return str(e)

    public_names_list = get_public_names(public_names_list=public_names_list, taxonomy_id=taxonomy_id, specimen_id=specimen_id, conn=conn, cur=cur)

    return jsonify({"data": public_names_list})


def bulk_search_public_name(body=None):  
    """searches DToL public names in bulk

    By passing in the appropriate taxonomy string, you can search for available public names in the system 

    :param bosy: 
    :type taxonomyId: str

    :rtype: List[PublicName]
    """
    
    public_names_list = []

    try:
        conn, cur = get_db(conn=None)
    except Exception as e:
        print('Database connection failed. Error: ' + str(e))
        return str(e)

    # body contains the rows of data
    if body:
        data_rows = body['dataRows']
        for row in data_rows:
            specimen_id = row['specimenId']
            taxonomy_id = row['taxId']
            
            public_names_list = get_public_names(public_names_list=public_names_list, taxonomy_id=taxonomy_id, specimen_id=specimen_id, conn=conn, cur=cur)

    return jsonify({"data": public_names_list})


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
