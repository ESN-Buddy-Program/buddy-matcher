#TODO: Implement the format validator

import pandas as pd
from datetime import datetime

#TODO: Implement the schema validator
def validate_schema(data: pd.DataFrame, schema: pd.DataFrame) -> bool:
  # return True if each column in the data is present in the schema
  return True


# TODO: Implement the age validator
def validate_age(data: pd.DataFrame) -> bool:
  # return True if the 'Age' column is present in the data
  return True


#TODO: Implement the date time format determiner
def determine_datetime_format(date_str: str) -> str:
    formats = ['%d-%m-%Y', '%m-%d-%Y', '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d']
    for fmt in formats:
        try:
            datetime.strptime(date_str, fmt)
            return fmt
        except ValueError:
            pass
    return "Unknown format"