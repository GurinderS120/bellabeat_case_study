"""Fitbit Data Cleaning Script.

This script:
1. Compares folder structures to detect common & unique files.
2. Identifies and loads only relevant CSV files.
3. Standardizes date and time formats.
4. Standardizes column names.
5. Converts time-based data (minute & second-level) to a daily summary.
6. Merges related datasets and consolidates them into a unified dataset.
7. Implements a data cleaning pipeline to address issues like missing values.

"""

import logging
from pathlib import Path
from typing import Dict
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Constants

# Moves two levels up (from scripts/ to root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent 

# Define the raw data directory relative to the root
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

PROCESSED_DATA_DIR = Path("data/processed/")
OUTPUT_FILE = PROCESSED_DATA_DIR / "merged_fitbit_data.csv"

# Folder names (assuming two subfolders)
FOLDER1 = RAW_DATA_DIR / "Fitabase Data 3.12.16-4.11.16"
FOLDER2 = RAW_DATA_DIR / "Fitabase Data 4.12.16-5.12.16"

# Files to keep - some files may get dropped upon further data exploration
KEEP_FILES = {
    "dailyActivity_merged.csv",
    "sleepDay_merged.csv",
    "heartrate_seconds_merged.csv",
    "weightLogInfo_merged.csv",
    "minuteSleep_merged.csv",
}

# Files to remove
REMOVE_FILES = {
    "dailySteps_merged.csv",
    "dailyCalories_merged.csv",
    "dailyIntensities_merged.csv",
    "minuteIntensitiesWide_merged.csv",
    "minuteStepsWide_merged.csv",
    "minuteCaloriesWide_merged.csv",
    "minuteIntensitiesNarrow_merged.csv",
    "minuteStepsNarrow_merged.csv",
    "minuteCaloriesNarrow_merged.csv",
    "hourlySteps_merged.csv",
    "hourlyCalories_merged.csv",
    "hourlyIntensities_merged.csv",
    "minuteMETsNarrow_merged.csv",
}

def compare_data_folders(folder1: Path, folder2: Path) -> dict:
    """Compares two data folders and identifies common and unique files.

    Args:
        folder1 (Path): First data folder path.
        folder2 (Path): Second data folder path.

    Returns:
        dict: A dictionary containing common and unique files.
    """
    if not folder1.exists() or not folder2.exists():
        logging.error("One or both data directories do not exist!")
        return {}

    files1 = {f.name for f in folder1.iterdir() if f.is_file()}
    files2 = {f.name for f in folder2.iterdir() if f.is_file()}

    return {
        "common_files": files1.intersection(files2),
        "unique_to_folder1": files1 - files2,
        "unique_to_folder2": files2 - files1,
    }

def list_all_files(directory: Path) -> list:
    """Lists all CSV files in a directory and its subdirectories.

    Args:
        directory (Path): Root data directory.

    Returns:
        list: List of all file paths.
    """
    return list(directory.glob("**/*.csv"))

def categorize_files(file_list: list) -> tuple:
    """Categorizes files into 'keep' and 'remove' groups.

    Args:
        file_list (list): List of file paths.

    Returns:
        tuple: (files_to_keep, files_to_remove)
    """
    files_to_keep = [f for f in file_list if f.name in KEEP_FILES]
    files_to_remove = [f for f in file_list if f.name in REMOVE_FILES]

    return files_to_keep, files_to_remove

def load_data() -> dict:
    """Loads relevant CSV files into a dictionary of pandas DataFrames.

    Args:
        None.

    Returns:
        dict: Dictionary where keys are modified filenames and values are DataFrames.
    """

    # List all files
    all_files = list_all_files(RAW_DATA_DIR)

    # Categorize files into 'keep' and 'remove'
    files_to_keep, _ = categorize_files(all_files)

    dfs = {}
    for file in files_to_keep:
        folder_name = file.parts[-2]  # Get the parent folder name
        time_period = "3_12" if "3.12.16-4.11.16" in folder_name else "4_12"
        
        file_name = f"{file.stem}_{time_period}"  # Append time period to filename
        
        dfs[file_name] = pd.read_csv(file)

    return dfs

def standardize_date_format(dfs: Dict[str, pd.DataFrame]) -> None:
    """
    Renames the second column in each DataFrame to 'Date' and standardizes it to 'yyyy-mm-dd' format.

    Modifies dfs in-place.

    Args:
        dfs (Dict[str, pd.DataFrame]): Dictionary of DataFrames.
    """
    for _, df in dfs.items():
        if df.shape[1] > 1:  # Ensure at least two columns exist
            date_col = df.columns[1]  # Get the date column (index 1)

            # Rename to 'Date' if it's not already named 'Date'
            if date_col != "Date":
                df.rename(columns={date_col: "Date"}, inplace=True)
                date_col = "Date"

            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
            df[date_col] = df[date_col].dt.strftime("%Y-%m-%d")

def convert_minute_sleep_to_daily(dfs: Dict[str, pd.DataFrame]) -> None:
    """
    Converts 'minuteSleep_merged_3_12' to daily sleep format like 'sleepDay_merged_4_12'
    and removes unnecessary columns.

    Args:
        dfs (Dict[str, pd.DataFrame]): Dictionary of DataFrames.

    """
    if "minuteSleep_merged_3_12" in dfs:
        df_minute_sleep = dfs["minuteSleep_merged_3_12"].copy()

        date_col = df_minute_sleep.columns[1]  # Get the date column (index 1)

        # Remove 'logId' column
        df_minute_sleep.drop(columns=["logId"], inplace=True, errors="ignore")

        # Compute TotalTimeInBed (Count all rows per Id, SleepDay)
        sleep_summary = df_minute_sleep.groupby(["Id", date_col], as_index=False).size()
        sleep_summary.rename(columns={"size": "TotalTimeInBed"}, inplace=True)

        # Compute TotalMinutesAsleep (Count rows where 'value' == 1)
        asleep_summary = df_minute_sleep[df_minute_sleep["value"] == 1].groupby(["Id", date_col], as_index=False).size()
        asleep_summary.rename(columns={"size": "TotalMinutesAsleep"}, inplace=True)

        # Merge both summaries
        sleep_summary = sleep_summary.merge(asleep_summary, on=["Id", date_col], how="left")
        sleep_summary.fillna(0, inplace=True)  # Replace NaN with 0 (for cases where no sleep was recorded)

        # Ensure column order matches 'sleepDay_merged_4_12'
        sleep_summary = sleep_summary[["Id", date_col, "TotalMinutesAsleep", "TotalTimeInBed"]]

        # Save as 'sleepDay_merged_3_12' for consistency
        dfs["sleepDay_merged_3_12"] = sleep_summary

    # Remove unnecessary DataFrames
    dfs.pop("minuteSleep_merged_3_12", None)
    dfs.pop("minuteSleep_merged_4_12", None)

def convert_second_heartrate_to_daily(dfs: Dict[str, pd.DataFrame]) -> None:
    """
    Converts 'heartrate_seconds_merged_3_12' and 'heartrate_seconds_merged_4_12'
    into daily average heart rate format, renames them to 'heartrateDay_merged',
    and removes the original second-level files.

    Modifies dfs in-place.

    Args:
        dfs (Dict[str, pd.DataFrame]): Dictionary of DataFrames.
    """
    rename_map = {
        "heartrate_seconds_merged_3_12": "heartrateDay_merged_3_12",
        "heartrate_seconds_merged_4_12": "heartrateDay_merged_4_12"
    }

    for old_key, new_key in rename_map.items():
        if old_key in dfs:
            df = dfs[old_key].copy()
            
            date_col = df.columns[1]  # Get the date column (index 1)

            # Aggregate to get the daily average heart rate per user
            df = df.groupby(["Id", date_col], as_index=False).agg(
                AvgHeartRate=("Value", "mean")
            )

            # Store in dfs with the new name
            dfs[new_key] = df

            # Remove the old file
            del dfs[old_key]

def convert_minute_weight_to_daily(dfs: Dict[str, pd.DataFrame]) -> None:
    """
    Cleans and aggregates 'weightLogInfo_merged_3_12' and 'weightLogInfo_merged_4_12'
    by removing unnecessary columns and averaging weight-related metrics per day.

    Modifies dfs in-place.

    Args:
        dfs (Dict[str, pd.DataFrame]): Dictionary of DataFrames.
    """
    for key in ["weightLogInfo_merged_3_12", "weightLogInfo_merged_4_12"]:
        if key in dfs:
            df = dfs[key].copy()

            date_col = df.columns[1]  # Get the date column (index 1)
            
            # Drop unnecessary columns
            df.drop(columns=["Fat", "IsManualReport", "LogId"], inplace=True, errors="ignore")

            # Aggregate to get daily averages
            df = df.groupby(["Id", date_col], as_index=False).agg(
                AvgWeightKg=("WeightKg", "mean"),
                AvgWeightPounds=("WeightPounds", "mean"),
                AvgBMI=("BMI", "mean")
            )

            # Save back to dfs
            dfs[key] = df

def convert_time_data_to_daily(dfs: Dict[str, pd.DataFrame]) -> None:
    """
    Converts time-based data (minute and second-level) into daily summaries.

    Args:
        dfs (Dict[str, pd.DataFrame]): Dictionary of DataFrames to be modified.
    """
    
    # Convert sleep data from minute format to day format
    convert_minute_sleep_to_daily(dfs)

    # Convert heartrate data from seconds format to day format
    convert_second_heartrate_to_daily(dfs)

    # Convert weight data from minute format to day format
    convert_minute_weight_to_daily(dfs)

def merge_activity_data(dfs: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Merges daily activity data from both time periods and drops unnecessary columns.

    Args:
        dfs (Dict[str, pd.DataFrame]): Dictionary containing DataFrames.

    Returns:
        pd.DataFrame: Merged daily activity dataset with unnecessary columns removed.
    """
    activity_merged = pd.concat([dfs["dailyActivity_merged_3_12"], dfs["dailyActivity_merged_4_12"]], ignore_index=True)

    return activity_merged

def merge_sleep_data(dfs: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Merges sleep data from both time periods and drops unnecessary columns.

    Args:
        dfs (Dict[str, pd.DataFrame]): Dictionary containing DataFrames.

    Returns:
        pd.DataFrame: Merged sleep dataset with unnecessary columns removed.
    """
    sleep_merged = pd.concat([dfs["sleepDay_merged_3_12"], dfs["sleepDay_merged_4_12"]], ignore_index=True)

    sleep_merged.drop(columns=["TotalSleepRecords"], errors="ignore", inplace=True)

    return sleep_merged

def merge_weight_data(dfs: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Merges weight data from both time periods and drops unnecessary columns.

    Args:
        dfs (Dict[str, pd.DataFrame]): Dictionary containing DataFrames.

    Returns:
        pd.DataFrame: Merged weight dataset with unnecessary columns removed.
    """
    weight_merged = pd.concat([dfs["weightLogInfo_merged_3_12"], dfs["weightLogInfo_merged_4_12"]], ignore_index=True)

    return weight_merged

def merge_heart_rate_data(dfs: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Merges heart rate data from both time periods and drops unnecessary columns.

    Args:
        dfs (Dict[str, pd.DataFrame]): Dictionary containing DataFrames.

    Returns:
        pd.DataFrame: Merged heart rate dataset with unnecessary columns removed.
    """
    heartrate_merged = pd.concat([dfs["heartrateDay_merged_3_12"], dfs["heartrateDay_merged_4_12"]], ignore_index=True)

    return heartrate_merged

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handles missing values by dropping essential missing rows and imputing others.

    Args:
        df (pd.DataFrame): The dataset.

    Returns:
        pd.DataFrame: The dataset with missing values handled.
    """
    # Drop rows only if essential data is missing (TotalSteps, Calories)
    df.dropna(subset=["TotalSteps", "Calories"], inplace=True)
    
    # Flag users who track sleep data
    df["HasSleepData"] = df["TotalMinutesAsleep"].notna().astype(int)

    # Fill missing weight, BMI, and heart rate values with the user's average
    df["AvgWeightKg"] = df["AvgWeightKg"].fillna(df.groupby("Id")["AvgWeightKg"].transform("mean"))

    df["AvgBMI"] = df["AvgBMI"].fillna(df.groupby("Id")["AvgBMI"].transform("mean"))

    df["AvgHeartRate"] = df["AvgHeartRate"].fillna(df.groupby("Id")["AvgHeartRate"].transform("mean"))

    # Fill missing Calories based on Calories per Step ratio
    avg_calories_per_step = df["Calories"].sum() / df["TotalSteps"].sum()
    
    df["Calories"].fillna(df["TotalSteps"] * avg_calories_per_step)

    return df

def flag_weight_tracking(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flags users who track weight and BMI:
        HasWeightData -> 1 if the user has AvgWeightKg, else 0.
        HasBMIData -> 1 if the user has AvgBMI, else 0.

    Args:
        df (pd.DataFrame): The dataset.

    Returns:
        pd.DataFrame: The dataset with tracking flags.
    """
    df["HasWeightData"] = df["AvgWeightKg"].notna().astype(int)
    df["HasBMIData"] = df["AvgBMI"].notna().astype(int)

    return df

def handle_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detects and removes rows with extreme outliers using the IQR method.

    Args:
        df (pd.DataFrame): The dataset.

    Returns:
        pd.DataFrame: The dataset with outlier rows removed.
    """

   # Define key columns for outlier removal (excluding less critical ones)
    outlier_columns = ["TotalSteps", "Calories", "VeryActiveMinutes", "TotalDistance"]

    for col in outlier_columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - (1.5 * IQR)
        upper_bound = Q3 + (1.5 * IQR)

        # Remove entire rows where any column has extreme outlier values
        df = df[(df[col].isna()) | ((df[col] >= lower_bound) & (df[col] <= upper_bound))]

    # Remove biologically implausible heart rate values
    df = df[(df["AvgHeartRate"].isna()) | ((df["AvgHeartRate"] >= 30) & (df["AvgHeartRate"] <= 250))]

    # Flag users who track heart rate data
    df["HasHeartRateData"] = df["AvgHeartRate"].notna().astype(int)

    return df

def add_derived_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds new columns for additional insights.

    Args:
        df (pd.DataFrame): The dataset.

    Returns:
        pd.DataFrame: The dataset with derived metrics added.
    """
    df = df.copy()

    df["SleepEfficiency"] = np.where(df["TotalTimeInBed"] > 0, df["TotalMinutesAsleep"] / df["TotalTimeInBed"], np.nan)

    df["VeryActiveRatio"] = np.where(df["TotalDistance"] > 0, df["VeryActiveDistance"] / df["TotalDistance"], np.nan)

    return df

def drop_unnecessary_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drops columns that are redundant or not useful for analysis.

    Args:
        df (pd.DataFrame): The dataset.

    Returns:
        pd.DataFrame: The dataset with unnecessary columns removed.
    """
    df.drop(columns=["SedentaryActiveDistance", "AvgWeightPounds"], errors="ignore", inplace=True)

    return df

def handle_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes duplicate records and ensures only one entry per user per day.

    Args:
        df (pd.DataFrame): The dataset.

    Returns:
        pd.DataFrame: The dataset with duplicates handled.
    """
    # Remove exact duplicate rows
    df.drop_duplicates(inplace=True)

    return df

def handle_negative_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensures all numerical values are non-negative by replacing negative values with NaN.

    Args:
        df (pd.DataFrame): The dataset.

    Returns:
        pd.DataFrame: The dataset with no negative values.
    """
    # Identify all numerical columns
    numeric_cols = df.select_dtypes(include=["number"]).columns

    # Replace negative values with NaN
    df[numeric_cols] = df[numeric_cols].apply(lambda col: col.map(lambda x: np.nan if x < 0 else x))

    return df

def round_decimal_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rounds all numerical columns to 2 decimal places, except for 'Id' and binary flag columns.

    Args:
        df (pd.DataFrame): The dataset.

    Returns:
        pd.DataFrame: The dataset with rounded numerical values.
    """

    # Identify numerical columns excluding 'Id' and binary flag columns
    exclude_cols = ["Id", "HasSleepData", "HasWeightData", "HasBMIData", "HasHeartRateData"]

    decimal_cols = df.select_dtypes(include=["number"]).columns.difference(exclude_cols)

    # Round only the selected decimal columns
    df[decimal_cols] = df[decimal_cols].round(2)

    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the dataset by handling missing values, removing outliers,
    adding derived metrics, and dropping unnecessary columns.

    Args:
        df (pd.DataFrame): The dataset.

    Returns:
        pd.DataFrame: The fully cleaned dataset.
    """

    df = handle_duplicates(df)
    df = handle_missing_values(df)
    df = flag_weight_tracking(df)
    df = handle_outliers(df)
    df = add_derived_metrics(df)
    df = drop_unnecessary_columns(df)
    df = handle_negative_values(df)
    df = round_decimal_values(df)

    return df

def merge_all_data(dfs: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Merges all related datasets and consolidates them into a unified dataset.

    Args:
        dfs (Dict[str, pd.DataFrame]): Dictionary containing DataFrames.

    Returns:
        pd.DataFrame: Fully merged dataset containing daily activity, sleep, weight, and heart rate data.
    """
    # Merge related datasets
    activity_data = merge_activity_data(dfs)
    sleep_data = merge_sleep_data(dfs)
    weight_data = merge_weight_data(dfs)
    heartrate_data = merge_heart_rate_data(dfs)

    # Merge everything together into one DataFrame
    merged_df = activity_data \
        .merge(sleep_data, on=["Id", "Date"], how="left") \
        .merge(weight_data, on=["Id", "Date"], how="left") \
        .merge(heartrate_data, on=["Id", "Date"], how="left")
    
    return merged_df

def handle_data_processing() -> pd.DataFrame:
    """
    Executes the full Fitbit data processing pipeline.

    This function:
    - Compares file structures to detect common and unique files.
    - Loads relevant data files and standardizes date formats.
    - Converts time-based data (minute- and second-level) into daily summaries.
    - Merges related datasets into a consolidated DataFrame.
    - Cleans the merged dataset to handle missing values, outliers, and inconsistencies.

    Args:
        None.
    
    Returns:
        pd.DataFrame: Fully cleaned dataset ready to be used in data analysis.
    """

    # Load the necessary data
    dfs = load_data()

    # Standardize all date columns into yyyy-mm-dd format
    standardize_date_format(dfs)

    # Convert time-based data (minute & second-level) to a daily summary
    convert_time_data_to_daily(dfs)

    # Merge related datasets and combine them into one DataFrame
    merged_df = merge_all_data(dfs)

    # Save the final dataset for analysis
    # merged_df.to_csv(f"{PROCESSED_DATA_DIR}/merged_pre_cleaned_data.csv", index=False)

    # Clean the merged dataset
    cleaned_df = clean_data(merged_df)

    return cleaned_df
