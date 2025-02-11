# Importing external libraries
import pandas as pd
import pyfiglet
import colorlog as log
# Importing internal libraries
import formatter
import outlier_calculator
import distance_calculator
import student_matcher



def main():
    # figlet name
    custom_fig = pyfiglet.Figlet(font='standard')
    print(custom_fig.renderText('ESN Buddy Matcher'), flush=True)

    log.basicConfig(level=log.INFO)

    # Load the data
    local_students: pd.DataFrame = pd.read_csv(
        "/input/local_students.csv", skipinitialspace=True)
    log.info("Local students loaded [%s]", local_students.shape)

    incoming_students: pd.DataFrame = pd.read_csv(
        "/input/incoming_students.csv", skipinitialspace=True)
    log.info("Incoming students loaded [%s]", incoming_students.shape)

    local_students_schema: pd.DataFrame = pd.read_csv(
        "/config/local_students_schema.csv", skipinitialspace=True)
    log.info("Local students schema loaded [%s]", local_students_schema.shape)

    incoming_students_schema: pd.DataFrame = pd.read_csv(
        "/config/incoming_students_schema.csv", skipinitialspace=True)
    log.info(
        "Incoming students schema loaded [%s]", incoming_students_schema.shape)

    # Validate and format the data
    local_students, incoming_students = formatter.validate_and_format_data(
        local_students, incoming_students,
        local_students_schema, incoming_students_schema)

    # Filter out outliers from the data
    threshold: float = 7.0

    # look for outliers by age in the incoming students
    local_std: float = float(local_students['age'].std())
    incoming_outliers = outlier_calculator.calculate_age_outliers(
        incoming_students, threshold=threshold, std=local_std)

    log.info("Outliers calculated")
    are_outliers: bool = any(incoming_outliers)
    if are_outliers:
        log.warning("Outliers found")
        log.warning("local std: %.001f, local_mean: %.001f",
                    local_std, local_students['age'].mean())
        log.warning("z-score threshold: %.001f", threshold)
        print(incoming_outliers)
        str_outlier = outlier_calculator.outliers_to_str(
            incoming_students, incoming_outliers)
        for i in str_outlier:
            # print in red color
            log.warning(f"\033[91m{i}\033[00m")
        incoming_students = outlier_calculator.remove_outliers(
            incoming_students, incoming_outliers)
    else:
        log.info
        log.info("No outliers foundusing a threshold of %.001f", threshold)


    distance_matrix= distance_calculator.calculate_distance_matrix(local_students, incoming_students)
    print(distance_matrix)

    base_local_capacity = local_students['buddyCount'].sum()
    base_incoming_necessity = incoming_students.shape[0]


    matches_matrix = student_matcher.compute_optimal_pairs(
        distance_matrix, local_students, incoming_students, base_local_capacity, base_incoming_necessity)
    print(matches_matrix)




if __name__ == '__main__':
    main()
