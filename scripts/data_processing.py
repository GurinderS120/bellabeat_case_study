"""Fitbit Data Cleaning Script.

This script:
1. Compares folder structures to detect common & unique files.
2. Identifies and loads only relevant CSV files.

"""

import os
import glob
import logging
import pandas as pd
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Constants
RAW_DATA_DIR = Path("data/raw/")
PROCESSED_DATA_DIR = Path("data/processed/")
OUTPUT_FILE = PROCESSED_DATA_DIR / "merged_fitbit_data.csv"

# Folder names (assuming two subfolders)
FOLDER1 = RAW_DATA_DIR / "Fitabase Data 3.12.16-4.11.16"
FOLDER2 = RAW_DATA_DIR / "Fitabase Data 4.12.16-5.12.16"

# Files to keep
KEEP_FILES = {
    "dailyActivity_merged.csv",
    "sleepDay_merged.csv",
    "minuteIntensitiesNarrow_merged.csv",
    "minuteStepsNarrow_merged.csv",
    "minuteCaloriesNarrow_merged.csv",
    "heartrate_seconds_merged.csv",
    "hourlySteps_merged.csv",
    "hourlyCalories_merged.csv",
    "hourlyIntensities_merged.csv",
    "weightLogInfo_merged.csv"
}

# Files to remove
REMOVE_FILES = {
    "dailySteps_merged.csv",
    "dailyCalories_merged.csv",
    "dailyIntensities_merged.csv",
    "minuteIntensitiesWide_merged.csv",
    "minuteStepsWide_merged.csv",
    "minuteCaloriesWide_merged.csv"
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

    logging.info("Keeping These Files:")
    for file in files_to_keep:
        logging.info(file)

    logging.info("\nRemoving These Files:")
    for file in files_to_remove:
        logging.info(file)

    return files_to_keep, files_to_remove

def load_csv_files(file_list: list) -> dict:
    """Loads CSV files into a dictionary of pandas DataFrames.

    Args:
        file_list (list): List of CSV file paths to load.

    Returns:
        dict: Dictionary where keys are filenames and values are DataFrames.
    """
    dfs = {}
    for file in file_list:
        file_name = file.stem  # Remove ".csv" extension
        dfs[file_name] = pd.read_csv(file)
    return dfs


def main():
    """Main function to execute the Fitbit data cleaning process."""
    logging.info("Fitbit Data Cleaning Started.")

    # Compare file structures
    folder_comparison = compare_data_folders(FOLDER1, FOLDER2)

    logging.info("\nCommon Files in Both Folders:")
    logging.info("\n".join(folder_comparison["common_files"]) if folder_comparison["common_files"] else "None")

    logging.info("\nFiles Only in Folder 1:")
    logging.info("\n".join(folder_comparison["unique_to_folder1"]) if folder_comparison["unique_to_folder1"] else "None")

    logging.info("\nFiles Only in Folder 2:")
    logging.info("\n".join(folder_comparison["unique_to_folder2"]) if folder_comparison["unique_to_folder2"] else "None")

    # List all files
    all_files = list_all_files(RAW_DATA_DIR)

    # Categorize files into 'keep' and 'remove'
    files_to_keep, _ = categorize_files(all_files)

    # Load only the necessary files
    dfs = load_csv_files(files_to_keep)


if __name__ == "__main__":
    main()
