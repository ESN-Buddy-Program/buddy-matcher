from difflib import get_close_matches
import pandas as pd
import colorlog as log
from typing import Tuple
import validator


# write a main function to check the format and correctly format the data
def validate_and_format_data(local_students: pd.DataFrame,
                             incoming_students: pd.DataFrame,
                             local_students_schema: pd.DataFrame,
                             incoming_students_schema: pd.DataFrame,
                             ) -> Tuple[pd.DataFrame, pd.DataFrame]:

    # Validate schemas
    is_valid_schema_local = validator.validate_schema(
        local_students, local_students_schema)
    if not is_valid_schema_local:
        log.error("Local students data does not match the schema.")
        raise ValueError("Local students data does not match the schema.")
    is_valid_schema_incoming = validator.validate_schema(
        incoming_students, incoming_students_schema)
    if not is_valid_schema_incoming:
        log.error("Incoming students data does not match the schema.")
        raise ValueError("Incoming students data does not match the schema.")

    # format to fit schema
    log.info("Formatting local student data")
    local_students = format_to_fit_schema(
        local_students, local_students_schema)
    log.info("Formatting incoming student data")
    incoming_students = format_to_fit_schema(
        incoming_students, incoming_students_schema)

    return local_students, incoming_students


def format_to_fit_schema(
  data: pd.DataFrame,
  schema: pd.DataFrame) -> pd.DataFrame:
    # Rename the columns in the data to match the schema
    rename_map = schema.set_index('questionText')['headerName'].to_dict()
    data = data.rename(columns=rename_map)

    # Get the columns to keep based on the schema
    columns_to_keep: list = schema['headerName'].tolist()  # type: ignore

    # Identify columns that are missing
    missing_columns = [
        col for col in columns_to_keep if col not in data.columns]

    # Log missing columns and their closest matches
    for missing_col in missing_columns:
        closest_matches = get_close_matches(
            missing_col, data.columns, n=3, cutoff=0.6)
        log.warning(
            "Column '%s' is missing. Closest matches: %s",
            missing_col, closest_matches if closest_matches else
            "No close matches"
        )

    # Filter the DataFrame to only include columns that exist in the data
    columns_to_keep = [col for col in columns_to_keep if col in data.columns]
    filtered_data = data[columns_to_keep]
    log.info("Filtered data: %s", filtered_data.shape)

    if not isinstance(filtered_data, pd.DataFrame):
        log.error("Filtered data is not a DataFrame")
        raise ValueError("Filtered data is not a DataFrame")

    return filtered_data
