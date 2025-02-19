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

def segment_users_by_sleep_tracking(df: pd.DataFrame) -> pd.Series:
    """Categorizes users based on whether they track sleep.

    Args:
        df (pd.DataFrame): The dataset.

    Returns:
        pd.Series: Percentage of users who track sleep vs. those who don’t.
    """
    return df["HasSleepData"].value_counts(normalize=True) * 100

def compare_sleep_vs_activity(df: pd.DataFrame) -> pd.DataFrame:
    """Compares sleep duration against activity levels.

    Args:
        df (pd.DataFrame): The dataset.

    Returns:
        pd.DataFrame: Average sleep duration per activity level.
    """
    return df.groupby("ActivityLevel")["TotalMinutesAsleep"].mean()

def summarize_heart_rate(df: pd.DataFrame) -> pd.DataFrame:
    """Summarizes key heart rate metrics.

    Args:
        df (pd.DataFrame): The dataset.

    Returns:
        pd.DataFrame: Summary statistics for heart rate-related columns.
    """
    heart_rate_columns = ["AvgHeartRate"]

    return df[heart_rate_columns].describe()

def visualize_heart_rate_distribution(df: pd.DataFrame) -> None:
    """Generates visualizations for heart rate distribution.

    Args:
        df (pd.DataFrame): The dataset.
    """
    _, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Histogram for AvgHeartRate
    sns.histplot(df["AvgHeartRate"], bins="auto", kde=True, ax=axes[0])

    axes[0].set_title("Distribution of Average Heart Rate")
    axes[0].set_xlabel("Avg Heart Rate (bpm)")
    axes[0].set_ylabel("Frequency")

    # Boxplot for AvgHeartRate
    sns.boxplot(x=df["AvgHeartRate"], ax=axes[1],
                medianprops={"color": "red", "linewidth": 2})
    
    axes[1].set_title("Boxplot of Average Heart Rate")
    axes[1].set_xlabel("Avg Heart Rate (bpm)")

    plt.tight_layout()
    plt.show()

def segment_users_by_heart_rate_tracking(df: pd.DataFrame) -> pd.Series:
    """Categorizes users based on whether they track heart rate.

    Args:
        df (pd.DataFrame): The dataset.

    Returns:
        pd.Series: Percentage of users who track heart rate vs. those who don’t.
    """
    return df["HasHeartRateData"].value_counts(normalize=True) * 100

def compare_heart_rate_vs_activity(df: pd.DataFrame) -> pd.DataFrame:
    """Compares average heart rate against activity levels.

    Args:
        df (pd.DataFrame): The dataset.

    Returns:
        pd.DataFrame: Average heart rate per activity level.
    """
    return df.groupby("ActivityLevel")["AvgHeartRate"].mean()

def summarize_weight(df: pd.DataFrame) -> pd.DataFrame:
    """Summarizes key weight and BMI metrics.

    Args:
        df (pd.DataFrame): The dataset.

    Returns:
        pd.DataFrame: Summary statistics for weight-related columns.
    """
    weight_columns = ["AvgWeightKg", "AvgBMI"]

    return df[weight_columns].describe()

def visualize_weight_distribution(df: pd.DataFrame) -> None:
    """Generates visualizations for weight and BMI distribution.

    Args:
        df (pd.DataFrame): The dataset.
    """
    _, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Histogram for AvgWeightKg
    sns.histplot(df["AvgWeightKg"], bins="auto", kde=True, ax=axes[0])

    axes[0].set_title("Distribution of Avg Weight (kg)")
    axes[0].set_xlabel("Avg Weight (kg)")
    axes[0].set_ylabel("Frequency")

    # Boxplot for AvgBMI
    sns.boxplot(x=df["AvgBMI"], ax=axes[1],
                medianprops={"color": "red", "linewidth": 2})
    
    axes[1].set_title("Boxplot of BMI")
    axes[1].set_xlabel("BMI")

    plt.tight_layout()
    plt.show()

def segment_users_by_weight_tracking(df: pd.DataFrame) -> dict:
    """Categorizes users based on whether they track weight and BMI.

    Args:
        df (pd.DataFrame): The dataset.

    Returns:
        dict: Percentage of users who track weight and BMI.
    """
    return {
        "Weight Tracking": df["HasWeightData"].value_counts(normalize=True) * 100,
        "BMI Tracking": df["HasBMIData"].value_counts(normalize=True) * 100
    }

def compare_weight_tracking_vs_engagement(df: pd.DataFrame) -> dict:
    """Compares weight tracking engagement with other activity metrics.

    Args:
        df (pd.DataFrame): The dataset.

    Returns:
        dict: Average steps and sleep minutes grouped by weight tracking.
    """
    return {
        "Weight vs Activity": df.groupby("HasWeightData")["TotalSteps"].mean(),
        "Weight vs Sleep": df.groupby("HasWeightData")["TotalMinutesAsleep"].mean()
    }

def generate_marketing_visuals(df: pd.DataFrame) -> None:
    """Generates key visualizations to support marketing recommendations.

    Args:
        df (pd.DataFrame): The dataset.
    """
    _, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1️. Pie Chart: Percentage of Users Tracking Each Metric
    tracking_types = {
        "Activity Tracking": df["TotalSteps"].notna().sum(),
        "Sleep Tracking": df["HasSleepData"].sum(),
        "Heart Rate Tracking": df["HasHeartRateData"].sum(),
        "Weight Tracking": df["HasWeightData"].sum()
    }
    axes[0, 0].pie(tracking_types.values(), labels=tracking_types.keys(), autopct="%1.1f%%", colors=["blue", "green", "red", "orange"])
    axes[0, 0].set_title("Percentage of Users Tracking Each Metric")

    # 2️. Scatter Plot: Steps vs. Calories Burned
    sns.regplot(x=df["TotalSteps"], y=df["Calories"], ax=axes[0, 1], scatter_kws={"alpha": 0.5}, line_kws={"color": "red"})
    axes[0, 1].set_title("Steps vs. Calories Burned")
    axes[0, 1].set_xlabel("Total Steps")
    axes[0, 1].set_ylabel("Calories Burned")

    # 3️. Bar Chart: Tracking Engagement by User Group (Number of Metrics Tracked)
    df["TrackingCount"] = df[["HasSleepData", "HasHeartRateData", "HasWeightData"]].sum(axis=1)
    tracking_groups = df["TrackingCount"].value_counts().sort_index()
    tracking_groups.plot(kind="bar", color=["red", "orange", "green", "blue"], ax=axes[1, 0])
    axes[1, 0].set_title("Tracking Engagement by User Group")
    axes[1, 0].set_xlabel("Number of Metrics Tracked")
    axes[1, 0].set_ylabel("Number of Users")

    # 4️. Histogram: Tracking Consistency Per User
    user_tracking_consistency = df.groupby("Id")[["HasSleepData", "HasHeartRateData", "HasWeightData"]].mean()
    sns.histplot(user_tracking_consistency.mean(axis=1), bins=10, kde=True, ax=axes[1, 1])
    axes[1, 1].set_title("Tracking Consistency Per User")
    axes[1, 1].set_xlabel("Average Tracking Frequency")
    axes[1, 1].set_ylabel("Number of Users")

    plt.tight_layout()
    plt.show()

