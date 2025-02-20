"""Fitbit Data Pipeline Execution Script.

This script:
1. Orchestrates the full data processing and analysis workflow.

"""

from data_processing import handle_data_processing
from analysis import generate_marketing_visuals

def main() -> None:
    """
    Runs the Fitbit data processing and visualization pipeline.

    This function:
    - Calls `handle_data_processing()` to clean and preprocess the dataset.
    - Calls `generate_marketing_visuals()` to generate key visualizations.

    Args:
        None.
    """
    cleaned_df = handle_data_processing()
    generate_marketing_visuals(cleaned_df)

if __name__ == "__main__":
    main()