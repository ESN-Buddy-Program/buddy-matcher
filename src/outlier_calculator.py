import pandas as pd


def calculate_age_outliers(
  data: pd.DataFrame,
  threshold: float = 3.0,
  std: float = 2.0) -> pd.DataFrame:
    """Calculates outliers in a series of data using the z-score method.

    Args:
        age_data (pd.Series): Series of numerical data (e.g., ages).
        threshold (float): Threshold for determining outliers. Defaults to 2.0.
        std_data (Optional[pd.Series]): Series of standard deviation data.

    Returns:
        pd.DataFrame: DataFrame of outliers (True/False) and their z-scores.
        columns: is_outlier, z_score
    """
    # Extract age data from the DataFrame
    age_data: pd.Series = pd.Series(data['age'].values)

    # Calculate z-scores
    mean_data = age_data.mean()
    z_scores: pd.Series = pd.Series((age_data - mean_data) / std)

    # Calculate outliers
    outliers: pd.DataFrame = (z_scores.abs() > threshold).to_frame()
    outliers = outliers.rename(columns={0: "is_outlier"})
    outliers = pd.concat([outliers, z_scores.rename("z_score")], axis=1)
    return outliers


def remove_outliers(
  data: pd.DataFrame,
  outliers: pd.DataFrame) -> pd.DataFrame:
    for index, value in outliers.iterrows():
        if value["is_outlier"] is True:
            data = data.drop(index)
    return data


def outliers_to_str(data: pd.DataFrame, outliers: pd.DataFrame) -> list[str]:
    """Returns array of strings of the names of outliers"""

    outlier_names: list[str] = []
    for index, value in outliers.iterrows():
        if value["is_outlier"]:
            # Get the corresponding row in 'data' using index alignment
            row = data.loc[data.index == index]

            # Check if the row exists (this step is to avoid potential errors)
            if not row.empty:
                first_name = row["firstName"].iloc[0]
                last_name = row["lastName"].iloc[0]
                age = row["age"].iloc[0]
                # Append the formatted name to the list of outliers
                outlier_names.append(
                    f"{first_name} {last_name} ({age})")

    return outlier_names
