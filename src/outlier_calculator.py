import pandas as pd
import numpy as np
from typing import Union, Optional
import colorlog

def calculate_outliers(data: pd.DataFrame, threshold: float = 3.0, std: float = 2.0) -> pd.DataFrame:
    """Calculates outliers in a series of data using the z-score method.

    Args:
        age_data (pd.Series): Series of numerical data (e.g., ages).
        threshold (float): Threshold for determining outliers. Defaults to 2.0.
        std_data (Optional[pd.Series]): Series of standard deviation data. If None, calculate from age_data.

    Returns:
        pd.DataFrame: DataFrame of outliers (True/False) for each data point and their z-scores.
        columns: is_outlier, z_score
    """
    # Extract age data from the DataFrame
    age_data: pd.Series = pd.Series(data['age'].values)

    # Calculate z-scores
    mean_data = age_data.mean()
    z_scores: pd.Series = pd.Series((age_data - mean_data) / std)


    # Calculate outliers
    outliers: pd.DataFrame = z_scores.abs() > threshold
    outliers = outliers.rename("is_outlier")
    outliers = pd.concat([outliers, z_scores.rename("z_score")], axis=1)
    return outliers


def remove_outliers(data: pd.DataFrame, outliers: pd.DataFrame) -> pd.DataFrame:
  for index, value in outliers.iterrows():
    if value["is_outlier"] == True:
      data = data.drop(index)
  return data




def outliers_to_str(data: pd.DataFrame, outliers: pd.DataFrame) -> list[str]:
    """returns array of strings of the names of outliers"""

    outlier_names: list[str] = []
    for index, value in outliers.iterrows():
        if value["is_outlier"] == True:
            first_name = data.loc[index, "firstName"]
            last_name = data.loc[index, "lastName"]
            age = data.loc[index, "age"]
            # Append the formatted name to the list of outliers
            outlier_names.append(f"{first_name} {last_name}  ({age} years, z-score: {value['z_score']:.2f})")
    return outlier_names
