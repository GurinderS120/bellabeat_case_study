"""Fitbit Data Analysis Script.

This script:
1. Summarizes key health metrics, including activity, sleep, heart rate, and weight.
2. Segments users based on activity, sleep tracking, and other key behaviors.
3. Compares relationships between different health metrics (e.g., sleep vs. activity).
4. Generates visualizations to identify trends and support marketing insights.
5. Runs a comprehensive analysis pipeline to extract meaningful insights from the cleaned dataset.

"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
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
    fig = plt.figure(figsize=(20, 25))
    spec = gridspec.GridSpec(3, 2, width_ratios=[2, 2], height_ratios=[1, 1, 1.2])

    # Descriptions for each visualization
    descriptions = [
        "This pie chart shows the percentage of users tracking each metric (Activity, Sleep, Heart Rate, Weight). "
        "It highlights gaps in engagement and potential areas for improvement.",
        
        "This scatter plot illustrates the positive correlation between step count and calories burned. "
        "Users who track their activity tend to burn more calories, supporting the importance of activity tracking.",
        
        "This histogram shows how consistently users log their data. It helps identify whether users track metrics daily, "
        "occasionally, or rarely, which can guide strategies for increasing engagement."
    ]

    # 1. Pie Chart: Percentage of Users Tracking Each Metric
    ax1 = fig.add_subplot(spec[0, 0])
    tracking_types = {
        "Activity Tracking": df["TotalSteps"].notna().sum(),
        "Sleep Tracking": df["HasSleepData"].sum(),
        "Heart Rate Tracking": df["HasHeartRateData"].sum(),
        "Weight Tracking": df["HasWeightData"].sum()
    }

    colors = ["blue", "green", "red", "orange"]
    
    ax1.pie(
        tracking_types.values(), 
        labels=tracking_types.keys(), 
        autopct="%1.1f%%", 
        colors=colors, 
        radius=1.6
    )

    # Add a legend to the right of the pie chart
    ax1.legend(
        tracking_types.keys(),
        loc="center left",  # Position it to the left of the bounding box
        bbox_to_anchor=(1.8, 0.8),
        fontsize=10,
        frameon=False
    )

    ax1.set_title("Percentage of Users Tracking Each Metric", fontweight="bold", pad=40)

    ax2 = fig.add_subplot(spec[0, 1])
    ax2.text(0, 0.5, descriptions[0], fontsize=14, verticalalignment="center", horizontalalignment="left", wrap=True)
    ax2.axis("off")

    # 2️. Scatter Plot: Steps vs. Calories Burned
    ax3 = fig.add_subplot(spec[1, 0])
    sns.regplot(x=df["TotalSteps"], y=df["Calories"], ax=ax3, scatter_kws={"alpha": 0.5}, line_kws={"color": "red"})
    ax3.set_title("Steps vs. Calories Burned", fontweight="bold", pad=20)
    ax3.set_xlabel("Total Steps")
    ax3.set_ylabel("Calories Burned")

    ax4 = fig.add_subplot(spec[1, 1])
    ax4.text(0, 0.5, descriptions[1], fontsize=14, verticalalignment="center", horizontalalignment="left", wrap=True)
    ax4.axis("off")

    # 3️. Histogram: Tracking Consistency Per User
    ax5 = fig.add_subplot(spec[2, 0])
    user_tracking_consistency = df.groupby("Id")[["HasSleepData", "HasHeartRateData", "HasWeightData"]].mean()
    sns.histplot(user_tracking_consistency.mean(axis=1), bins=10, kde=True, ax=ax5)
    ax5.set_title("Tracking Consistency Per User", fontweight="bold", pad=20)
    ax5.set_xlabel("Average Tracking Frequency")
    ax5.set_ylabel("Number of Users")

    ax6 = fig.add_subplot(spec[2, 1])
    ax6.text(0, 0.5, descriptions[2], fontsize=14, verticalalignment="center", horizontalalignment="left", wrap=True)
    ax6.axis("off")

    plt.subplots_adjust(hspace=1.2)
    plt.show()

def analyze_data(df: pd.DataFrame) -> None:
    """Runs the full analysis pipeline for user activity tracking.

    Args:
        df (pd.DataFrame): The dataset.
    """

    # Activity Tracking Analysis
    activity_summary = summarize_activity(df)
    df = segment_users_by_activity(df)
    activity_vs_calories = compare_activity_vs_calories(df)

    visualize_activity_distribution(df)
    
    # Display results
    print("Activity Summary:")
    print(activity_summary)

    print("\nActivity Level vs Calories:")
    print(activity_vs_calories)

    # Sleep Tracking Analysis
    sleep_summary = summarize_sleep(df)
    sleep_tracking_segments = segment_users_by_sleep_tracking(df)
    sleep_vs_activity = compare_sleep_vs_activity(df)
    
    visualize_sleep_distribution(df)

    # Display results
    print("Sleep Summary:")
    print(sleep_summary)

    print("\nSleep Tracking Segments:")
    print(sleep_tracking_segments)

    print("\nSleep vs Activity:")
    print(sleep_vs_activity)

    # Heart Rate Tracking Analysis
    heart_rate_summary = summarize_heart_rate(df)
    heart_rate_tracking_segments = segment_users_by_heart_rate_tracking(df)
    heart_rate_vs_activity = compare_heart_rate_vs_activity(df)

    visualize_heart_rate_distribution(df)

    # Display results
    print("Heart Rate Summary:")
    print(heart_rate_summary)

    print("\nHeart Rate Tracking Segments:")
    print(heart_rate_tracking_segments)

    print("\nHeart Rate Tracking Segments:")
    print(heart_rate_vs_activity)

    # Weight Tracking Analysis
    weight_summary = summarize_weight(df)
    weight_tracking_segments = segment_users_by_weight_tracking(df)
    weight_vs_engagement = compare_weight_tracking_vs_engagement(df)

    visualize_weight_distribution(df)

    # Display results
    print("Weight Summary")
    print(weight_summary)

    print("\nWeight Tracking Segments")
    print(weight_tracking_segments["Weight Tracking"])

    print("\nBMI Tracking Segments")
    print(weight_tracking_segments["BMI Tracking"])

    print("\nWeight vs Activity")
    print(weight_vs_engagement["Weight vs Activity"])

    print("\nWeight vs Sleep")
    print(weight_vs_engagement["Weight vs Sleep"])
