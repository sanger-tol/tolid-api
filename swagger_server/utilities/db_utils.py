import sqlite3
import json
import pandas as pd

from swagger_server.utilities.file_utils import read_tsv


db_cols = ['prefix', 'species', 'taxid', 'common_name', 'genus', 'family', 'tax_order', 'class', 'phylum']
file_name = "final_merged.txt"

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
            try:
                print('drop table public_names;')
                cur.execute('drop table public_names;')
            except Exception as e:
                print('Could not drop the public_names table. Error: ' + str(e))

            cur.execute('create table public_names(prefix varchar, species varchar, taxid int, common_name varchar, genus varchar, family varchar, tax_order varchar, class varchar, phylum varchar);')
    except Exception as e:
        print('Database creation failed. Error: ' + str(e))
        # return created

    df = None
    row_count = 0
    try:
        df = read_tsv(file_name=file_name)
        row_count = df.shape[0]  # number of rows
        # col_count = df.shape[1]  # number of columns
    except Exception as e:
        print('Could not read the public name tsv file. Error: ' + str(e))
        return created, row_count, conn    
        
    try:
        # Add to the database
        df.columns = db_cols  # There are no column names in the tsv file, so need to add
        df.to_sql(name='public_names', con=conn, if_exists='replace', index=False)
        conn.commit()  # Should not have to, but just in case
    except Exception as e:
        print('Could not add the public names to the local database. Error: ' + str(e))
        return created 

    return True, row_count, conn

def query_local_database(conn=None, cur=None, query_str=None, print_all=False):
    """
    Query rows in the public_name table
    :param conn: the Connection object
    :param cur: the Cursor object
    :param query_str: the Taxon id to search for
    :param print_all: print results to screen
    :return:
    """
    if not conn:
        return False

    if not cur:    
        cur = conn.cursor()

    if query_str and query_str != 'all':
        cur.execute("SELECT * FROM public_names where taxid=?", (query_str,))
    else:
        cur.execute("SELECT * FROM public_names")

    rows = cur.fetchall()

    if print_all:
        for row in rows:
            print(row)
    return rows
