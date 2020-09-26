import pandas as pd
import numpy as np
import os

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
