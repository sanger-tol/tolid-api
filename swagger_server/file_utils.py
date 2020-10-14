import pandas as pd
import numpy as np
import os
import time


def read_tsv(file_name=None, columns=None, update_floats=False):
    table_df = pd.DataFrame() 

    if not file_name:
        return table_df

    try:
        if os.path.getsize(file_name) == 0:  # Empty file
            print("Error: Could not read file " + file_name)
        else:
            print("Trying to read and parse file " + file_name)
            table_df = pd.read_csv(file_name, sep="\t", header=None, names=columns, index_col=None, encoding='utf-8', low_memory=False)
            if update_floats:
                # Make sure we do not change int to float
                table_df['pub_number'] = table_df['pub_number'].fillna(0).astype(int)
                table_df['pub_number'] = table_df['pub_number'].astype(float).astype(int)
                
    except Exception as e: 
        print("Error: Could not read file " + file_name + ". " + str(e))

    table_df = table_df.replace(np.nan, '', regex=True)  # Remove NaN
    return table_df


def write_tsv(dataframe=None, file_name=None):
    try:
        # Write the new rows to the file
        dataframe.to_csv(file_name, sep="\t", encoding='utf-8', index=False, header=False)
    except Exception as e:
        return 'Error: Could not write/update the file ' + file_name + '. ' + str(e)

    return 'Success. Update file ' + file_name


def get_file_times(directory, file_name):
    file_date_format = "%B %d %Y %H:%M:%S"  # 20180724092134
    date_format = "%Y%m%d%H%M%S"  # 20180724092134
    file_time = ""
    raw_time = ""
    try:
        dt = time.gmtime(os.path.getmtime(os.path.join(directory, file_name)))
        raw_time = time.strftime(date_format, dt)  
        file_time = time.strftime(file_date_format, dt) 
    except Exception as e:
        print(str(e))

    return file_time, raw_time
