import sqlite3
import json
import pandas as pd

from sqlalchemy import func
from swagger_server.file_utils import read_tsv
from swagger_server.model import db, PnaSpecies, PnaSpecimen

def create_new_specimen(species, specimen_id):
    # What is the current highest specimen number?
    highest = db.session.query(func.max(PnaSpecimen.number)).filter(PnaSpecimen.species_id == species.taxonomy_id).scalar()
    if not highest:
        highest = 0
    specimen = PnaSpecimen(specimen_id=specimen_id, number=highest+1)
    specimen.species = species
    return specimen


def is_missing(data=None, query_type=None):
    if data and data.lower() == 'none':
        # ToDo, query NCBI/OLS for missing data and type
        return "None"
    return data

def map_public_names_dict(data=None):
    # Database columns ['prefix', 'public_nane', 'species', 'taxid', 'common_name', 'genus', 'family', 'tax_order', 'class', 'phylum', 'specimen_id']
    # prefix is the first part of the public name
    d = {}
    if data:
        d = {'prefix': data[0], 
            'publicName': data[1],
            'species': is_missing(data=data[2], query_type='species'), 
            'taxonomyId': int(data[3]), 
            'commonName': is_missing(data=data[4], query_type='common_name'), 
            'genus': is_missing(data=data[5], query_type='genus'), 
            'family': is_missing(data=data[6], query_type='family'), 
            'order': is_missing(data=data[7], query_type='order'), 
            'taxaClass': is_missing(data=data[8], query_type='class'), 
            'phylum': is_missing(data=data[9], query_type='phylum'),
            'specimenId': data[10]
            }

    return d   

def get_next_pub_number(public_names=None):
    pub_number = 1
    # ToDo, get next pub_number by looking at the last number used for this specimen
    # Need to know all the public names for this specimen to find the next number in the sequence
    return pub_number


def map_allocated_names(data=None):
    # Database columns ['public_name', 'species', 'specimen_id', 'pub_number'
    prefix = None
    pub_number = None
    public_name = None
    species = None

    for row in data:
        if row:
            prefix = row[0]
            public_name = str(prefix) + str(pub_number)
            species = is_missing(data=data[1], query_type='species')

    return public_name, species


def map_prefix_pub_names(data=None, specimen_id=None):
    # Database columns ['prefix', 'species', 'taxid', 'common_name', 'genus', 'family', 'tax_order', 'class', 'phylum']
    prefix = None
    pub_number = None
    public_name = None
    species = None

    if data:
        prefix = data[0]
        public_name = str(prefix) + str(pub_number)
        species = is_missing(data=data[1], query_type='species')

    return specimen_id, public_name, species, prefix


def get_db_cols_and_file_name(table_name=None):
    db_cols_public_names = ['prefix', 'species', 'taxid', 'common_name', 'genus', 'family', 'tax_order', 'class', 'phylum']
    db_cols_unique_ids = ['public_name', 'species', 'specimen_id', 'pub_number','extra_empty_tab']

    if table_name == 'public_names':
        return db_cols_public_names, 'final_merged.txt', False
    return db_cols_unique_ids, 'unique_ids_assigned.txt', True


def get_db(conn=None):
    if not conn:
        try:
            conn = sqlite3.connect("public_names.db")
        except Exception as e:
            print('Cound not find database file public_names.db. Error: ' + str(e))
    cur = conn.cursor()
    return conn, cur


def populate_db():
    created = False
    conn, cur = get_db(conn=None)
    try:
        with conn:
            for table_name in ['public_names', 'unique_ids']:
                try:
                    print("drop table " + table_name + ";")
                    cur.execute("drop table " + table_name + ";")
                except Exception as e:
                    print("Could not drop the " + table_name + " table. Ignore this error if the database is new. Error: " + str(e))

            cur.execute('create table public_names(prefix varchar, species varchar, taxid int, common_name varchar, genus varchar, family varchar, tax_order varchar, class varchar, phylum varchar);')
            cur.execute('create table unique_ids(public_name varchar, species varchar, specimen_id varchar, pub_number varchar, ignore varchar);')

    except Exception as e:
        print('Database creation failed. Error: ' + str(e))
        # return created

    df = None
    row_count = 0
    for table_name in ['public_names', 'unique_ids']:
        db_cols, tsv_file_name, update_floats = get_db_cols_and_file_name(table_name=table_name)
        try:
            df = read_tsv(file_name=tsv_file_name, columns=db_cols)
            row_count = df.shape[0]  # number of rows
            # col_count = df.shape[1]  # number of columns
        except Exception as e:
            print('Could not read the public name tsv file {tsv_file_name}. Error: ' + str(e))
            return created, row_count, conn    
            
        try:
            # Add to the database
            df.columns = db_cols  # There are no column names in the tsv file, so need to add
            df.to_sql(name=table_name, con=conn, if_exists='replace', index=False)
            conn.commit()  # Should not have to, but just in case
        except Exception as e:
            print('Could not add the public names to the local database. Error: ' + str(e))
            return created 

    return True, row_count, conn


def query_local_database(conn=None, cur=None, tax_id=None, specimen_id=None, print_all=False):
    """
    Query rows in the public_name table
    :param conn: the Connection object
    :param cur: the Cursor object
    :param tax_id: the Taxon id to search for
    :param print_all: print results to screen
    :return: JSON with complete public name and taxa structure
    """
    if not conn:
        conn, cur = get_db(conn=None)

    if not cur:    
        cur = conn.cursor()

    # public_names table = ['prefix', 'species', 'taxid', 'common_name', 'genus', 'family', 'tax_order', 'class', 'phylum']
    # unique_ids table = ['public_name', 'species', 'specimen_id', 'pub_number']
    if tax_id and specimen_id:
        cur.execute("SELECT a.prefix, b.public_name, a.species, a.taxid, a.common_name, a.genus, a.family, a.tax_order, a.class, a.phylum, b.specimen_id FROM public_names a, unique_ids b where a.species = b.species AND a.taxid=? and b.specimen_id=?", (tax_id,specimen_id))

    rows = cur.fetchall()

    #if not rows:
    #    rows = [(None, None, None, tax_id, None, None, None, None, None, None, specimen_id)]

    if print_all:
        for row in rows:
            print(row)
    return rows


def update_local_database(conn=None, cur=None, tax_id=None, specimen_id=None, print_all=False):
    """
    Query rows in the public_name database and adds a new entry if required
    :param conn: the Connection object
    :param cur: the Cursor object
    :param tax_id: the Taxon id to search for
    :param specimen_id: the GAL specimen id to allocate a new name for
    :param print_all: print results to screen
    :return: JSON with complete public name and taxa structure
    """

    if not tax_id or not specimen_id:
        return "Error: Please provide a NCBI tax id and GAL specimen id"

    if not conn:
        conn, cur = get_db(conn=None)

    if not cur:    
        cur = conn.cursor()

    new_public_name = None 
    q_species = None 
    pub_number = None
    new_record = False

    # Check that we do not have the record already
    public_names = query_local_database(conn=conn, cur=cur, tax_id=tax_id, specimen_id=specimen_id, print_all=print_all)
    if not public_names:
       
        # Get all relevant prefix data from the list of generated public name prefixes
        if tax_id:
            cur.execute("SELECT prefix, species, taxid, common_name, genus, family, tax_order, class, phylum FROM public_names where taxid=?", (tax_id,))
            rows = cur.fetchall()
        
        if rows:
            for row in rows:
                q_specimen_id, q_public_name, q_species, q_prefix = map_prefix_pub_names(data=row, specimen_id=specimen_id)
    
        # Now we have the entry from the pre-allocated names list, so next is to get the entries for this species already allocated public names
        # We need 'public_name', 'species', 'specimen_id', 'pub_number' for the new entry
        cur.execute("SELECT max(CAST(pub_number AS INTEGER)) FROM unique_ids where species=?", (q_species,))
        all_rows = cur.fetchall()

        # pub_number is the max number allready used, so pub_number+1 will be added to the public name
        pub_number = 0
        for row in all_rows:
            max_number = row[0]
            if max_number:
                pub_number = max_number + 1
            else:
                pub_number = 1

        new_public_name = q_prefix+str(pub_number)
        # Insert new record into the database
        with conn:
            cur.execute("INSERT INTO unique_ids('public_name','species','specimen_id','pub_number') values(?,?,?,?)", (new_public_name, q_species, specimen_id, pub_number))
            conn.commit
            new_record = True

        if print_all:
            print(new_public_name, q_species, specimen_id, pub_number)

        # Now read the newly inserted record back from the database using the "normal" method 
        public_names = query_local_database(conn=conn, cur=cur, tax_id=tax_id, specimen_id=specimen_id, print_all=False)

    return public_names, new_public_name, q_species, specimen_id, pub_number, new_record