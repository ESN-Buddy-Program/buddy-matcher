import pandas as pd
from typing import Tuple


def add_matches_column(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()
    """
    Adds a new 'Matches' column to the DataFrame if it doesn't exist.

    Parameters:
    df (pd.DataFrame): The DataFrame to which the new column will be added.

    Returns:
    pd.DataFrame: The DataFrame with the new 'Matches' column if it was not present.
    """

    if 'Matches' not in df.columns:
        # You can initialize it with any default value you like
        df['Matches'] = None
        print("'Matches' column added.")
    else:
        print("'Matches' column already exists.")

    return df


def add_id(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a new 'id' column to the DataFrame if it doesn't exist.

    Parameters:
    df (pd.DataFrame): The DataFrame to which the new column will be added.

    Returns:
    pd.DataFrame: The DataFrame with the new 'id' column if it was not present.
    """

    df_copy = df.copy()
    if 'id' not in df_copy.columns:
        df_copy = df_copy.reset_index().rename(columns={'index': 'id'})
        print("'id' column added.")
    else:
        print("'id' column already exists.")

    return df_copy


def _prepare_for_one_to_one_matching(self):
    self.add_matches_column()
    self.add_id_and_adjust_capacity()
    self.handle_extra_buddies()
