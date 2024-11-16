from numpy._typing import _UnknownType
import pandas as pd
import colorlog as logging
from typing import Tuple, Optional, Union, List, Dict
from datetime import datetime, timedelta
import numpy as np
import configparser
import validator
import logging as log


# write a main function to check the format and correctly format the data
def validate_and_format_data(local_students: pd.DataFrame,
                incoming_students: pd.DataFrame,
                local_students_schema: pd.DataFrame,
                incoming_students_schema: pd.DataFrame,
) -> Tuple[ Union[pd.DataFrame, pd.Series, None], Union[pd.DataFrame, pd.Series, None]]:

     # Validate schemas
    is_valid_schema_local = validator.validate_schema(local_students, local_students_schema)
    if not is_valid_schema_local:
        log.error("Local students data does not match the schema.")
        raise ValueError("Local students data does not match the schema.")
    log.info("local schema matches")

    # print the columns in the schema
    print(local_students_schema.columns)

    is_valid_schema_incoming = validator.validate_schema(incoming_students, incoming_students_schema)
    if not is_valid_schema_incoming:
        log.error("Incoming students data does not match the schema.")
        raise ValueError("Incoming students data does not match the schema.")
    log.info("incoming schema matches")

    log.info("Data is valid")
    # format to fit schema
    print(local_students_schema)
    print(incoming_students_schema)
    formatted_local_students = format_to_fit_schema(local_students, local_students_schema)
    formateed_incoming_students = format_to_fit_schema(incoming_students, incoming_students_schema)

    return local_students, incoming_students




def format_to_fit_schema(data: pd.DataFrame, schema: pd.DataFrame) -> Union[pd.DataFrame, pd.Series, None]:
    """
    Formats a DataFrame to fit the given schema by:
    1. Renaming columns in `data` based on the schema's 'headerName'.
    where the 'questionText' matches the column name in `data` and replacing the column name with the corresponding 'headerName'.
    2. Keeping only the columns that exist in the schema.

    Parameters:
        data (pd.DataFrame): The DataFrame to be formatted.
        schema (pd.DataFrame): The schema DataFrame with columns 'headerName' and 'questionText'.

    Returns:
        Union[pd.DataFrame, None]: The formatted DataFrame if valid columns are found, otherwise None.
    """
    # Create a mapping of every question to its corresponding header name
    column_mapping = schema.set_index('questionText')[' headerName'].to_dict()



    # Get the valid columns based on the schema
    valid_columns = [col for col in data.columns if col in column_mapping]
    if not valid_columns:
      return None
        # Return None if no valid columns are found

    # Rename columns and filter only valid columns
    formatted_data = data.rename(columns=column_mapping)[valid_columns]

    # Ensure the result is always a DataFrame (even if only one column is left)
    if formatted_data.shape[1] == 1:
        formatted_data = formatted_data.to_frame()

    return formatted_data




# depricated soon (should be moved to different file )
def get_base_capacities(local_students: pd.DataFrame) -> int:
    """Function to get the base capacities of the local students and the necessity of incoming students"""
    base_local_capacity: int = int(local_students['Capacity'].sum())
    return base_local_capacity



# depricated soon (should be moved to different file )
def get_base_necessity(incoming_students: pd.DataFrame) -> int:
    """Function to get the base necessity of incoming students"""
    base_necessity: int = int(incoming_students.count(axis=1).count())
    return base_necessity
