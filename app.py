import streamlit as st
import pandas as pd
import os
from file_handler import list_csv_files, preview_csv

# Predefined column names
STANDARD_COLUMNS = ["Coord_X", "Coord_Y", "resistivity", "conductivity", "K_corr", "TH_corr", "U_corr", "mag_res", "mag_dev", "altitude"]

# Streamlit App
st.title("CSV Editor & Formatter")

# Select project folder
data_folder = "data"  # We can change data directory if needed

# List all CSV files
csv_files = list_csv_files(data_folder)

if csv_files:
    # User selects a CSV file
    selected_file = st.selectbox("Select a CSV file:", csv_files)

    # Load selected CSV
    file_path = os.path.join(data_folder, selected_file)
    df = pd.read_csv(file_path, nrows=100)  # Load a small sample

    st.write(f"### Preview of {selected_file}")
    st.dataframe(df.head())  # Show sample data

    # Column selection and renaming
    st.write("### Select and Rename Columns")
    new_columns = {}
    delete_columns = []

    for col in df.columns:
        col1, col2 = st.columns([2, 1])

        # Dropdown for renaming
        new_name = col1.selectbox(f"Rename '{col}'", ["(Keep Original)"] + STANDARD_COLUMNS, key=col)
        if new_name != "(Keep Original)":
            new_columns[col] = new_name

        # Checkbox for deletion
        delete = col2.checkbox(f"Delete '{col}'", key=f"del_{col}")
        if delete:
            delete_columns.append(col)

    # Apply Changes
    if st.button("Apply Changes & Save"):
        # Reload the full CSV file to apply changes to all rows
        full_df = pd.read_csv(file_path)  # Load full data

        # Remove unwanted columns
        full_df = full_df.drop(columns=delete_columns, errors="ignore")

        # Rename columns
        full_df = full_df.rename(columns=new_columns)

        # Save file in a new structured folder
        formatted_folder = "formatted_data"
        save_path = os.path.join(formatted_folder, selected_file)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        full_df.to_csv(save_path, index=False)  # Save without extra index column

        st.success(f"File saved successfully: {save_path}")
else:
    st.warning("No CSV files found in the data folder.")
