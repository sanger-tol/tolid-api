import pandas as pd
import numpy as np
import os
import time


def read_tsv(file_name=None):
    table_df = pd.DataFrame() 

    if not file_name:
        return table_df

    try:
        try:
            if os.path.getsize(file_name) == 0:  # Empty file
                print("Error: Could not read file " + file_name)
            else:
                # Enforce str datatype for all columns we read from the file
                col_names = pd.read_csv(file_name, sep="\t", nrows=0).columns
                types_dict = {col: str for col in col_names}
                table_df = pd.read_csv(file_name, sep="\t", header=0, encoding='utf-8', dtype=types_dict)
        except Exception as e: 
            if os.path.getsize(file_name) > 0:
                # Todo, should check if the file format is Excel. ie. not in the exception handler
                table_df = pd.read_csv(file_name, sep="\t", header=0, encoding='ISO-8859-1')  # Excel format
                print("Tried to open as Excel tsv file 'ISO-8859-1' file " + file_name + ". " + str(e))
    except Exception as e:
        print("Error: Could not read file " + file_name + ". " + str(e))

    table_df = table_df.replace(np.nan, '', regex=True)  # Remove NaN
    return table_df

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
