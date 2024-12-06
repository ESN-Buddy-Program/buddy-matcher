import pandas as pd
import math


# def calculate_distance_matrix(
#         local_students: pd.DataFrame,
#         incoming_students: pd.DataFrame,
#         weights: pd.DataFrame) -> pd.DataFrame:
#     """Calculates the distance matrix between local and incoming students.

#     Args:
#         local_students (pd.DataFrame): DataFrame of local student data.
#         incoming_students (pd.DataFrame): DataFrame of incoming student data.
#         weights (pd.DataFrame): DataFrame of weights for each feature.

#     Returns:
#         pd.DataFrame: Distance matrix between local and incoming students.
#     """
#     # Create an empty DataFrame to store the distance matrix
#     distance_matrix: pd.DataFrame = pd.DataFrame(
#         index=local_students.index,
#         columns=incoming_students.index)

#     return distance_matrix

#     # Iterate over each


# def calculate_distance(
#         local_student: pd.Series,
#         incoming_student: pd.Series, weights: pd.DataFrame) -> float:
#     return 1


def sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))

def calculate_age_distance(
  local_students: pd.Series,
  incoming_student: pd.Series,
  age_tolerance: int = 5
) -> float:

    local_age = local_students['Age']
    incoming_age = incoming_student['Age']

    age_difference = abs(int(local_age) - int(incoming_age))

    return sigmoid(age_difference/age_tolerance)
