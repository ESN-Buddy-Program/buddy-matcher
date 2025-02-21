import munkres
import pandas as pd
import numpy as np


def compute_optimal_pairs(distance_matrix: pd.DataFrame, local_students: pd.DataFrame,
                          incoming_students: pd.DataFrame, base_local_capacity: int,
                          base_incoming_necessity: int) -> pd.DataFrame:
    """
    Computes the optimal pairs of local and incoming students based on a distance matrix.

    This function uses the Munkres algorithm to match local students to incoming students while
    respecting the capacity of local students. After each round of matching, incoming students that
    have been matched are removed from further consideration, and local students who have reached their
    capacity (buddyCount) are removed using remove_matched_local_students.

    Parameters:
    - distance_matrix (pd.DataFrame): A DataFrame representing the distances between local and incoming students.
    - local_students (pd.DataFrame): A DataFrame containing local student details, including their capacities.
    - incoming_students (pd.DataFrame): A DataFrame containing incoming student details.
    - base_local_capacity (int): The base capacity limit for local students.
    - base_incoming_necessity (int): The base necessity limit for incoming students.

    Returns:
    - pd.DataFrame: A DataFrame indicating the matching between local and incoming students, where 1 indicates a match.
    """
    # Work on copies so we don't modify the original DataFrames.
    local_students = local_students.copy()
    incoming_students = incoming_students.copy()

    # Create an empty matching matrix.
    matching_matrix = pd.DataFrame(
        np.zeros((len(local_students), len(incoming_students))),
        index=local_students.index,
        columns=incoming_students.index
    )

    # A set to track incoming students who have already been matched.
    matched_incoming_students = set()

    # Continue iterating until all incoming students are matched or no local students remain.
    while (len(matched_incoming_students) < len(incoming_students)) and (not local_students.empty):
        # Filter the distance matrix: use only local students still available and incoming students not yet matched.
        current_distance_matrix = distance_matrix.loc[
            local_students.index,
            [col for col in distance_matrix.columns if col not in matched_incoming_students]
        ]

        if current_distance_matrix.empty:
            break

        # Apply the Munkres algorithm to the filtered distance matrix.
        m = munkres.Munkres()
        cost_matrix = current_distance_matrix.values.tolist()
        indexes = m.compute(cost_matrix)

        # For each pairing provided by Munkres, update the matching if the local student still has capacity.
        for local_idx, inc_idx in indexes:
            local_student = current_distance_matrix.index[local_idx]
            incoming_student = current_distance_matrix.columns[inc_idx]

            # Only assign if this local student hasn't yet reached their buddyCount capacity.
            if matching_matrix.loc[local_student].sum() < local_students.loc[local_student, 'buddyCount']:
                matching_matrix.loc[local_student, incoming_student] = 1
                matched_incoming_students.add(incoming_student)

        # Remove local students that have now reached their matching capacity.
        local_students, distance_matrix = remove_matched_local_students(matching_matrix, local_students, distance_matrix)

    return matching_matrix


def remove_matched_local_students(matching_matrix: pd.DataFrame, local_students: pd.DataFrame,
                                  distance_matrix: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Removes local students who have reached their matching capacity from local_students and distance_matrix.

    A local student is removed if the total number of matches (row sum in matching_matrix) is equal to or
    exceeds their 'buddyCount' capacity.

    Parameters:
    - matching_matrix (pd.DataFrame): The matrix of matches where 1 indicates a match.
    - local_students (pd.DataFrame): DataFrame with local student details, including their 'buddyCount' capacity.
    - distance_matrix (pd.DataFrame): Matrix of distances between local and incoming students.

    Returns:
    - tuple[pd.DataFrame, pd.DataFrame]: Updated (local_students, distance_matrix) with students removed if they have reached capacity.
    """
    # Subset matching_matrix to only include rows of the currently active local students.
    matching_sum = matching_matrix.loc[local_students.index].sum(axis=1)

    # Compare the matching sum with the local capacities.
    remaining_mask = matching_sum < local_students['buddyCount']

    local_students_filtered = local_students[remaining_mask]
    distance_matrix_filtered = distance_matrix.loc[local_students_filtered.index]

    return local_students_filtered, distance_matrix_filtered #type: ignore

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
