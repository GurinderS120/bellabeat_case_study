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

def visualize_activity_distribution(df: pd.DataFrame) -> None:
    """Generates visualizations for user activity distribution.

    Args:
        df (pd.DataFrame): The dataset.
    """
    _, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Histogram for Total Steps
    sns.histplot(df["TotalSteps"], bins="auto", kde=True, ax=axes[0])
    axes[0].set_title("Distribution of Total Steps")
    axes[0].set_xlabel("Total Steps")
    axes[0].set_ylabel("Frequency")

    # Boxplot for Very Active Minutes
    sns.boxplot(
     x=df["VeryActiveMinutes"],
     medianprops={"color": "red", "linewidth": 2},
     ax=axes[1])
    
    axes[1].set_title("Boxplot of Very Active Minutes")
    axes[1].set_ylabel("Very Active Minutes")

    plt.tight_layout()
    plt.show()

def segment_users_by_activity(df: pd.DataFrame) -> pd.DataFrame:
    """Categorizes users into activity levels based on step count.

    Args:
        df (pd.DataFrame): The dataset.

    Returns:
        pd.DataFrame: The dataset with an added ActivityLevel column.
    """
    def categorize_activity(steps):
        if steps >= 10000:
            return "Highly Active"
        if steps >= 5000:
            return "Moderately Active"
        return "Low Activity"

    df["ActivityLevel"] = df["TotalSteps"].apply(categorize_activity)

    return df

def compare_activity_vs_calories(df: pd.DataFrame) -> pd.DataFrame:
    """Compares activity level against average calories burned.

    Args:
        df (pd.DataFrame): The dataset.

    Returns:
        pd.DataFrame: Average calories burned per activity level.
    """
    return df.groupby("ActivityLevel")["Calories"].mean()

def summarize_sleep(df: pd.DataFrame) -> pd.DataFrame:
    """Summarizes key sleep metrics.

    Args:
        df (pd.DataFrame): The dataset.

    Returns:
        pd.DataFrame: Summary statistics for sleep-related columns.
    """
    sleep_columns = ["TotalMinutesAsleep", "TotalTimeInBed", "SleepEfficiency"]

    return df[sleep_columns].describe()

def visualize_sleep_distribution(df: pd.DataFrame) -> None:
    """Generates visualizations for sleep tracking distribution.

    Args:
        df (pd.DataFrame): The dataset.
    """
    _, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Histogram for Total Minutes Asleep
    sns.histplot(df["TotalMinutesAsleep"], bins="auto", kde=True, ax=axes[0])
    axes[0].set_title("Distribution of Total Minutes Asleep")
    axes[0].set_xlabel("Total Minutes Asleep")
    axes[0].set_ylabel("Frequency")

    # Boxplot for Total Minutes Asleep
    sns.boxplot(x=df["TotalMinutesAsleep"], ax=axes[1],
                medianprops={"color": "red", "linewidth": 2})
    
    axes[1].set_title("Boxplot of Total Minutes Asleep")
    axes[1].set_xlabel("Total Minutes Asleep")

    plt.tight_layout()
    plt.show()

