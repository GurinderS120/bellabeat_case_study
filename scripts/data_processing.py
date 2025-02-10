from pathlib import Path

def compare_contrast_data_folders():
    # Get the project root
    script_dir = Path(__file__).resolve().parent  # scripts/
    project_root = script_dir.parent  # Move up one level to project root

    # Define folder paths relative to the project root
    folder1 = project_root / "data" / "raw" / "Fitabase Data 3.12.16-4.11.16"
    folder2 = project_root / "data" / "raw" / "Fitabase Data 4.12.16-5.12.16"

    # Ensure directories exist before listing files
    if not folder1.exists() or not folder2.exists():
        print("One or both data directories do not exist!")
        return

    # List all files in each folder
    files1 = set(f.name for f in folder1.iterdir() if f.is_file())
    files2 = set(f.name for f in folder2.iterdir() if f.is_file())

    # Find common and unique files
    common_files = files1.intersection(files2)
    unique_to_folder1 = files1 - files2
    unique_to_folder2 = files2 - files1

    # Print categorized files
    print("Common Files in Both Folders:")
    print("\n".join(common_files) if common_files else "None")

    print("\nFiles Only in Folder 1:")
    print("\n".join(unique_to_folder1) if unique_to_folder1 else "None")

    print("\nFiles Only in Folder 2:")
    print("\n".join(unique_to_folder2) if unique_to_folder2 else "None")

compare_contrast_data_folders()
