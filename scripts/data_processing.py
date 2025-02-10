"""Fitbit Data Cleaning Script.

This script:

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

def main():
    """Main function to execute the Fitbit data cleaning process."""
    logging.info("Fitbit Data Cleaning Started.")


if __name__ == "__main__":
    main()