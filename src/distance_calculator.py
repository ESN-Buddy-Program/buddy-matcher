import pandas as pd


def calculate_distance_matrix(
        local_students: pd.DataFrame,
        incoming_students: pd.DataFrame) -> pd.DataFrame:
#     """Calculates the distance matrix between local and incoming students.

#     Args:
#         local_students (pd.DataFrame): DataFrame of local student data.
#         incoming_students (pd.DataFrame): DataFrame of incoming student data.

#     Returns:
#         pd.DataFrame: Distance matrix between local and incoming students.
#     """
#     # Create an empty DataFrame to store the distance matrix
    distance_matrix: pd.DataFrame = pd.DataFrame(index=local_students.index,
        columns=incoming_students.index)
    # configure the pd.DataFrame
    for local_student in local_students:
        for incoming_student in incoming_students:
            distance_matrix.loc[local_student, incoming_student] = calculate_distance(
                local_students.loc[local_student], incoming_students.loc[incoming_student])

    return distance_matrix


def calculate_distance(local_student: pd.Series, incoming_student: pd.Series) -> float:
    distance : float = 0.0
    distance += is_same_university(incoming_student, local_student)
    distance += similar_personalities(incoming_student, local_student)
    distance += is_expectations(incoming_student, local_student)
    distance += gender_preference(incoming_student, local_student)
    return distance


def is_same_university(incoming_student: pd.Series, local_student: pd.Series) -> float:
    """
    Check if the university or study field matches between an incoming and a local student.

    Parameters:
        incoming_student (pd.Series): Details of the incoming student.
        local_student (pd.Series): Details of the local student.

    Returns:
        float: 0.0 if there's a match in university and study field, 0.5 for a match in
       university and 1.0 otherwise.
    """
    if incoming_student['University'] == local_student['University']:
        if incoming_student ['Faculty'] == local_student['Faculty']:
            return 0.0
        else:
            return 0.5
    else:
        return 1.0

def similar_personalities(incoming_student: pd.Series, local_student: pd.Series) -> float:
    """
    Check if the personalities matches between an incoming and a local student.

    Parameters:
        incoming_student (pd.Series): Details of the incoming student.
        local_student (pd.Series): Details of the local student.

    Returns:
        float: 0.0 if there's a match in personalities, 1.0 otherwise.
    """
    personality_match: float = 0.0

    if ((incoming_student['openess'] == local_student['openess']) or
        (incoming_student['openess'] < local_student['openess'] and local_student['openess'] - incoming_student['openess'] <= 2.0) or
        (incoming_student['openess'] > local_student['openess'] and incoming_student['openess'] - local_student['openess'] <= 2.0)):
        personality_match += 0.0
    else:
        personality_match += 1.0

    if ((incoming_student['conscientiousness'] == local_student['conscientiousness']) or
        (incoming_student['conscientiousness'] < local_student['conscientiousness'] and local_student['conscientiousness'] - incoming_student['conscientiousness'] <= 2.0) or
        (incoming_student['conscientiousness'] > local_student['conscientiousness'] and incoming_student['conscientiousness'] - local_student['conscientiousness'] <= 2.0)):
        personality_match += 0.0
    else:
        personality_match += 1.0

    if ((incoming_student['extraversion'] == local_student['extraversion']) or
        (incoming_student['extraversion'] < local_student['extraversion'] and local_student['extraversion'] - incoming_student['extraversion'] <= 2.0) or
        (incoming_student['extraversion'] > local_student['extraversion'] and incoming_student['extraversion'] - local_student['extraversion'] <= 2.0)):
        personality_match += 0.0
    else:
        personality_match += 1.0

    if ((incoming_student['agreeableness'] < local_student['agreeableness'] and local_student['agreeableness'] - incoming_student['agreeableness'] >= 2.0) or
        (incoming_student['agreeableness'] > local_student['agreeableness'] and incoming_student['agreeableness'] - local_student['agreeableness'] >= 2.0)):
        personality_match += 0.0
    else:
        personality_match += 1.0

    if ((incoming_student['neuroticism'] == local_student['neuroticism']) or
        (incoming_student['neuroticism'] < local_student['neuroticism'] and local_student['neuroticism'] - incoming_student['neuroticism'] <= 2.0) or
        (incoming_student['neuroticism'] > local_student['neuroticism'] and incoming_student['neuroticism'] - local_student['neuroticism'] <= 2.0)):
        personality_match += 0.0
    else:
        personality_match += 1.0

    if ((incoming_student['selfEfficacy'] == local_student['selfEfficacy']) or
        (incoming_student['selfEfficacy'] < local_student['selfEfficacy'] and local_student['selfEfficacy'] - incoming_student['selfEfficacy'] <= 2.0) or
        (incoming_student['selfEfficacy'] > local_student['selfEfficacy'] and incoming_student['selfEfficacy'] - local_student['selfEfficacy'] <= 2.0)):
        personality_match += 0.0
    else:
        personality_match += 1.0

    if personality_match == 5.0:
        personality_match = 1.0

    return personality_match

def is_expectations(incoming_student: pd.Series, local_student: pd.Series) -> float:
    """
    Check if the expectations matches between an incoming and a local student.

    Parameters:
        incoming_student (pd.Series): Details of the incoming student.
        local_student (pd.Series): Details of the local student.

    Returns:
        float: 0.0 if there's a match in expectations, 1.0 otherwise.
    """
    expectations_score: float = 0.0
    if (('I just want someone to answer my questions (online)' in incoming_student['expectations']) and ('I just want to answer some questions (online)' in local_student['expectations'])):
        expectations_score += 0.0
    else:
        expectations_score += 0.2

    if(('I want someone to answer my questions in person' in incoming_student['expectations']) and ('I want to answer some questions in person' in local_student['expectations'])):
        expectations_score += 0.0
    else:
        expectations_score += 0.2

    if(('I want to be shown around the city' in incoming_student['expectations']) and ('I want to show someone around the city' in local_student['expectations'])):
        expectations_score += 0.0
    else:
        expectations_score += 0.2

    if(('I want to meet more frequently' in incoming_student['expectations']) and ('I want to meet more frequently' in local_student['expectations'])):
        expectations_score += 0.0
    else:
        expectations_score += 0.2
    if(('I want to become friends' in incoming_student['expectations']) and ('I want to become friends' in local_student['expectations'])):
        expectations_score += 0.0
    else:
        expectations_score += 0.2

    return expectations_score

def gender_preference(incoming_student: pd.Series, local_student: pd.Series) -> float:
    """
    Check if the expectations matches between an incoming and a local student.

    Parameters:
        incoming_student (pd.Series): Details of the incoming student.
        local_student (pd.Series): Details of the local student.

    Returns:
        float: 0.0 if there's a match in gender, 0.5 * their preference otherwise.
    """
    if incoming_student['genderPreference'] == "I don't have a preference":
        if local_student['genderPreference'] == "I don't have a preference":
            return 0.0
        if local_student['genderPreference'] == incoming_student['gender']:
            return 0.0
        else:
            return 0.5 * local_student['genderPreferenceImportance']
    else:
        if incoming_student['genderPreference'] == local_student['gender']:
            if local_student['genderPreference'] == "I don't have a preference":
                return 0.0
            if local_student['genderPreference'] == incoming_student['gender']:
                return 0.0
            else:
                return 0.5 * local_student['genderPreferenceImportance']
        else:
            if local_student['genderPreference'] == "I don't have a preference":
                return 0.5 * incoming_student['genderPreferenceImportance']
            if local_student['genderPreference'] == incoming_student['gender']:
                return (0.0 + 0.5 * float( incoming_student['genderPreferenceImportance']))
            else:
                return (0.5 * float(local_student['genderPreferenceImportance']) + 0.5 * float(incoming_student['genderPreferenceImportance'])
)
