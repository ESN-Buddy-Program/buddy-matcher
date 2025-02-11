import munkres
import pandas as pd
import numpy as np
import colorlog as log
from pandas.io.parsers.base_parser import DataFrame


def compute_optimal_pairs(distance_matrix: pd.DataFrame, local_students: pd.DataFrame, incoming_students: pd.DataFrame, base_local_capacity: int, base_incoming_necessity: int) -> pd.DataFrame:
    """
    Computes the optimal pairs of local and incoming students based on a distance matrix.

    This function uses the Munkres algorithm to find the best matches between local students and incoming students
    while considering the capacity of local students and the necessity of incoming students. The function iteratively
    adjusts the matching based on the capacities of local students, ensuring that only those who can accommodate the
    current number of matches are considered.

    Parameters:
    - distance_matrix (pd.DataFrame): A DataFrame representing the distances between local and incoming students.
    - local_students (pd.DataFrame): A DataFrame containing information about local students, including their capacities.
    - incoming_students (pd.DataFrame): A DataFrame containing information about incoming students.
    - base_local_capacity (int): The base capacity limit for local students.
    - base_incoming_necessity (int): The base necessity limit for incoming students.

    Returns:
    - pd.DataFrame: A DataFrame indicating the matching between local and incoming students, where 1 indicates a match.
    """

    print(distance_matrix)
    local_students = local_students.copy()
    incoming_students = incoming_students.copy()

    matching_matrix: pd.DataFrame = pd.DataFrame(np.zeros((len(local_students), len(
        incoming_students))), index=local_students.index, columns=incoming_students.index)
    # Get the highest capacity local student
    highest_capacity: int = int(local_students['buddyCount'].max())
    print(highest_capacity)

    # Keep track of the matched incoming students
    matched_incoming_students: set[str] = set()

    for i in range(highest_capacity):
        # Remove local students who do not have enough capacity for i matches
        # TODO: issue with the indexes because of drops prior to this
        for index, row in local_students.iterrows():
            if row['buddyCount'] < i:
                distance_matrix = distance_matrix.drop(index)
                # Remove them from the local students dataframe (to keep indexes in sync)
                local_students = local_students.drop(index)

        # Filter distance_matrix to exclude matched incoming students
        distance_matrix_filtered = distance_matrix.loc[:, ~distance_matrix.columns.isin(
            matched_incoming_students)]

        # Only proceed if there are local students and incoming students to match
        if not local_students.empty and not distance_matrix_filtered.empty:
            m = munkres.Munkres()

            # Convert the filtered DataFrame to matrix format
            matrix: munkres.Matrix = distance_matrix_filtered.values.tolist()

            # Apply the algorithm to the matrix
            indexes = m.compute(matrix)

            log.info(indexes)
            log.info("Creating pair set %i", i)

            for row, column in indexes:
                matching_matrix.iloc[row, column] = 1
                # Add matched incoming student to the set
                matched_incoming_students.add(
                    distance_matrix_filtered.columns[column])
    return matching_matrix

def generate_matching_table(matching_matrix: pd.DataFrame, local_students: pd.DataFrame, incoming_students: pd.DataFrame) -> pd.DataFrame:
    """
    Generates a table of matched students with their contact details.

    For every match (cell value = 1) in the matching_matrix, this function
    retrieves the corresponding local and incoming student details and creates
    a row with:
        - Local Student: firstName + " " + lastName
        - Local Email
        - Local Phone
        - Incoming Student: firstName + " " + lastName
        - Incoming Email
        - Incoming Phone

    Parameters:
    - matching_matrix (pd.DataFrame): The matrix of matches where 1 indicates a match.
    - local_students (pd.DataFrame): DataFrame containing local student details.
    - incoming_students (pd.DataFrame): DataFrame containing incoming student details.

    Returns:
    - pd.DataFrame: A DataFrame containing paired students and their contact details.
    """

    # List to store matching details
    matching_rows = []

    # Iterate through the matching matrix; the index represents local students
    # and the columns represent incoming students.
    for local_idx in matching_matrix.index:
        for incoming_idx in matching_matrix.columns:
            if matching_matrix.loc[local_idx, incoming_idx] == 1:
                # Retrieve local and incoming student details.
                local: pd.Series = local_students.loc[local_idx]
                incoming: pd.Series = incoming_students.loc[incoming_idx]

                # Create full names by combining first and last names.
                local_name: str = f"{local['firstName']} {local['lastName']}"
                incoming_name: str = f"{incoming['firstName']} {incoming['lastName']}"

                # Build a dictionary for the matching row.
                matching_rows.append({
                    "Local Name": local_name,
                    "Local Email": local.get("email", ""),
                    "local Age" : local.get("age", ""),
                    "Local Phone": local.get("phone", ""),
                    "Incoming Name": incoming_name,
                    "Incoming Age" : incoming.get("age", ""),
                    "Incoming Email": incoming.get("email", ""),
                    "Incoming Phone": incoming.get("phone", "")
                })

    # Convert the list of matching rows to a DataFrame.
    matching_table = pd.DataFrame(matching_rows)
    return matching_table
