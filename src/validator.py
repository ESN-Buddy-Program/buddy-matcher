# format validator

import pandas as pd


def validate_schema(data: pd.DataFrame, schema: pd.DataFrame) -> list[str]:
    # Create a list to store the columns that do not match the schema
    mismatched_columns = []

    # Iterate over each column in the data
    for column in data.columns:
        # Check if the column is present in the schema
        if column not in schema['questionText'].values:
            mismatched_columns.append(column)

    return mismatched_columns
