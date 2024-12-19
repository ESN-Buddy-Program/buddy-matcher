
import pandas as pd
from transformers import BartTokenizer
from sklearn.metrics.pairwise import cosine_similarity
# Initialize the BART tokenizer
tokenizer = BartTokenizer.from_pretrained("facebook/bart-base")

def calculate_interest_similarity(tokenizer, local_student: pd.Series, incoming_student: pd.Series) -> float:
    """
    Calculate a normalized similarity score (0–1) between two students based on their top 3 interests.

    TODO:
    - Extract the top 3 interests from both students.
    - Tokenize the interests using a helper function.
    - Compute the raw similarity score using another helper function.
    - Normalize the raw score to the range of 0–1.
    - Return the normalized score.

    Parameters:
    - local_student (pd.Series): Series containing local student's details, including interests.
    - incoming_student (pd.Series): Series containing incoming student's details, including interests.

    Returns:
    - float: A normalized similarity score between the students' interests.
    """
    return 0.0
