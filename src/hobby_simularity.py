import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

# Load a pre-trained model to generate text embeddings.
# (You might need to install the package with: pip install sentence-transformers)
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')


def calculate_hobby_simularity(local_student: pd.Series, incoming_student: pd.Series) -> float:
    """
    Calculate the hobby similarity between a local student and an incoming student by computing
    the sine difference between the embeddings of their hobby interest strings.

    This function retrieves the 'interest1', 'interest2', and 'interest3' fields from both student records.
    For each interest, it obtains an embedding using a pre-trained sentence transformer and computes the cosine
    similarity. It then converts the cosine similarity into a sine difference using:

        sine_difference = sin(arccos(cosine_similarity))

    which yields 0 when the interests are identical (perfect match) and values closer to 1 for less similar interests.
    The final result is the average sine difference across all three interests.

    Args:
        local_student (pd.Series): The local student's data, including hobby fields.
        incoming_student (pd.Series): The incoming student's data, including hobby fields.

    Returns:
        float: The average sine difference across the three interest fields.
    """
    interests = ['interest1', 'interest2', 'interest3']
    sine_differences = []

    for interest in interests:
        # Retrieve the hobby strings; use empty string if not present.
        local_interest = local_student.get(interest, "")
        incoming_interest = incoming_student.get(interest, "")

        # If either interest is missing or empty, we assume maximal difference.
        if not local_interest or not incoming_interest:
            sine_differences.append(1.0)
            continue

        # Compute the embeddings for the given interest strings.
        embedding_local = model.encode(local_interest)
        embedding_incoming = model.encode(incoming_interest)

        # Compute the cosine similarity between the two embeddings.
        norm_local = np.linalg.norm(embedding_local)
        norm_incoming = np.linalg.norm(embedding_incoming)
        if norm_local == 0 or norm_incoming == 0:
            cosine_sim = 0.0  # Avoid division by zero.
        else:
            cosine_sim = np.dot(embedding_local, embedding_incoming) / (norm_local * norm_incoming)

        # Clip the cosine similarity to the valid range [-1, 1] to avoid numerical issues.
        cosine_sim = np.clip(cosine_sim, -1, 1)

        # Convert the cosine similarity to a sine difference.
        # Note: sin(arccos(x)) == sqrt(1 - x**2) for x in [-1, 1]
        sine_diff = np.sin(np.arccos(cosine_sim))
        sine_differences.append(sine_diff)

    # Return the average sine difference across the three interests.
    return float(np.mean(sine_differences))
