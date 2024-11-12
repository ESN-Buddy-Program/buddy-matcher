import format_check
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
) -> Tuple[pd.DataFrame, pd.DataFrame]:

    # Validate schemas
    is_valid_schema_local = validator.validate_schema(local_students, local_students_schema)
    if not is_valid_schema_local:
        log.error("Local students data does not match the schema.")
        raise ValueError("Local students data does not match the schema.")
    is_valid_schema_incoming = validator.validate_schema(incoming_students, incoming_students_schema)
    if not is_valid_schema_incoming:
        log.error("Incoming students data does not match the schema.")
        raise ValueError("Incoming students data does not match the schema.")

    # format to fit schema
    local_students = format_to_fit_schema(local_students, local_students_schema)
    incoming_students = format_to_fit_schema(incoming_students, incoming_students_schema)

    return local_students, incoming_students


# remove the colums that arn't in the schema'
def format_to_fit_schema(data: pd.DataFrame, schema: pd.DataFrame) -> pd.DataFrame:

  # rename the columns to match the schema
  data = data.rename(columns = schema.set_index('questionText')['headerName'].to_dict())
  # drop the columns that are not in the schema
  columns_to_keep: list = schema['headerName'].tolist()
  filtered_data: pd.DataFrame | pd.Series = data[columns_to_keep]

  if isinstance(filtered_data, pd.Series):
    log.error("Data is not a DataFrame")
    raise ValueError("Data is not a DataFrame")

  return filtered_data




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
