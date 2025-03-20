import os

def list_csv_files(data_folder="data"):
    csv_files = []

    # Loop through each subfolder inside 'data'
    for root, _, files in os.walk(data_folder):
        for file in files:
            if file.endswith(".csv"):  # Only include .csv files, we can add more file types if needed
                relative_path = os.path.relpath(os.path.join(root, file), data_folder)
                csv_files.append(relative_path)

    return csv_files

# Run the function and print the output
csv_list = list_csv_files()
print("Found CSV files:")
for csv in csv_list:
    print(f"- {csv}")

import pandas as pd

def preview_csv(file_path, num_rows=5):
    """Loads and previews the first few rows of a CSV file."""
    try:
        df = pd.read_csv(file_path, nrows=num_rows)  # Load only first few rows
        print(f"\nPreviewing: {file_path}")
        print("Columns:", list(df.columns))  # Print column names
        print("\nSample Data:")
        print(df.head())  # Print first few rows
    except Exception as e:
        print(f"Error loading {file_path}: {e}")

# Example usage for file load testing
if __name__ == "__main__":
    file_to_preview = "data/folder_1/file_1.csv"  # Testing with a specific file
    preview_csv(file_to_preview)