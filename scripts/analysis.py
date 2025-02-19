import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def summarize_activity(df: pd.DataFrame) -> pd.DataFrame:
    """Summarizes key activity metrics.

    Args:
        df (pd.DataFrame): The dataset.

    Returns:
        pd.DataFrame: Summary statistics for activity-related columns.
    """
    activity_columns = ["TotalSteps", "TotalDistance", "VeryActiveMinutes", "Calories"]
    return df[activity_columns].describe()

