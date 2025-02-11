import pandas as pd
import numpy as np
from scipy.optimize import linear_sum_assignment
from sentence_transformers import SentenceTransformer, util

# Initialize the embedding model (you can choose another model if preferred)
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_hobby_simularity(local_student: pd.Series, incoming_student: pd.Series) -> float:
    """
    Calculate the hobby similarity between a local student and an incoming student.

    Both students have three interest fields: 'interest1', 'interest2', 'interest3'.
    We compute embeddings for each interest, calculate pairwise cosine distances between
    the interests (where a distance of 0 indicates identical interests), and then use the
    Hungarian algorithm to optimally match the interests and return the average distance.

    Args:
        local_student (pd.Series): A series with at least keys 'interest1', 'interest2', 'interest3'.
        incoming_student (pd.Series): A series with at least keys 'interest1', 'interest2', 'interest3'.

    Returns:
        float: The average cosine distance (0 = very similar, higher = less similar).
    """

    # Extract the interest strings for each student
    local_interests = [
        str(local_student.get('interest1') or ""),
        str(local_student.get('interest2') or ""),
        str(local_student.get('interest3') or "")
    ]

    incoming_interests = [
        str(incoming_student.get('interest1') or ""),
        str(incoming_student.get('interest2') or ""),
        str(incoming_student.get('interest3') or "")
    ]

    # Compute the embeddings for each list of interests
    local_embeddings = model.encode(local_interests, convert_to_tensor=True)
    incoming_embeddings = model.encode(incoming_interests, convert_to_tensor=True)

    # Compute a 3x3 cosine similarity matrix between the two sets of embeddings.
    # util.cos_sim returns a tensor of cosine similarities.
    cosine_sim_matrix = util.cos_sim(local_embeddings, incoming_embeddings)

    # Convert cosine similarity to cosine distance (so that 0 means identical).
    # Note: cosine_distance = 1 - cosine_similarity.
    cost_matrix = 1 - cosine_sim_matrix.cpu().numpy()  # Convert to NumPy array if using GPU

    # Use the Hungarian algorithm to find the optimal matching between interests.
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    # Calculate the average distance for the optimal assignment.
    average_distance = cost_matrix[row_ind, col_ind].mean()

    return average_distance
