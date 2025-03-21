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


# Read log of modified files
log_path = "modified_log.txt"
if os.path.exists(log_path):
    with open(log_path, "r") as log_file:
        modified_files = set(log_file.read().splitlines())
else:
    modified_files = set()


# Toggle to filter edited files
col1, col2 = st.columns([3, 2])  # Width ratio can be adjusted

with col1:
    show_only_unedited = st.checkbox("Show only unedited CSV files", value=False)

with col2:
    if st.button("🔄 Reset Column Selections"):
        # Clear all session state keys related to rename/delete/select_all
        keys_to_clear = [k for k in st.session_state.keys() if k.startswith("rename_") or k.startswith("delete_")]
        for k in keys_to_clear:
            del st.session_state[k]
        st.session_state.select_all = False
        st.rerun()



# List all CSV files
all_csv_files = list_csv_files(data_folder)


# Initialize select_all in session state
if "select_all" not in st.session_state:
    st.session_state.select_all = False


# Filter files based on toggle
if show_only_unedited:
    csv_files = [f for f in all_csv_files if f.replace("\\", "/") not in modified_files]
else:
    csv_files = all_csv_files


if csv_files:
    # User selects a CSV file
    selected_file = st.selectbox("Select a CSV file:", csv_files)

    # Load selected CSV
    file_path = os.path.join(data_folder, selected_file)
    df = pd.read_csv(file_path, nrows=100)  # Load a small sample

    st.write(f"### Preview of {selected_file}")
    st.dataframe(df.head())  # Show sample data

    # Added a toggle button for selecting/unselecting all columns
    st.checkbox("Select All Columns for Deletion", key="select_all")
    select_all = st.session_state.select_all


    # Column selection and renaming
    st.write("### Select and Rename Columns")
    new_columns = {}
    delete_columns = []

    for col in df.columns:
        col1, col2 = st.columns([2, 1])

        # Dropdown for renaming
        new_name = col1.selectbox(
            f"Rename '{col}'",
            ["(Keep Original)"] + STANDARD_COLUMNS,
            key=f"rename_{col}"
        )

        # Logic: if user renamed the column, override deletion (uncheck)
        is_renamed = new_name != "(Keep Original)"

        # If renamed, we won't mark it for deletion even if 'select all' is on
        default_delete = select_all and not is_renamed

        # Checkbox for deletion
        delete = col2.checkbox(f"Delete '{col}'", value=default_delete, key=f"delete_{col}")

        # Save results
        if is_renamed:
            new_columns[col] = new_name
        if delete:
            delete_columns.append(col)


    # Optional categorization for saving in segmented_data
    st.write("### Optional: Categorize This Dataset")
    category = st.selectbox(
        "Categorize this file as:",
        options=["None", "Magnetic (MAG)", "Electromagnetic (EM)", "Radiometric (SPEC)", "Gravimetric (GRAV)"],
        index=0
    )


    # Apply Changes and Save Button
    if st.button("Apply Changes & Save"):
        # Reload the full CSV file
        full_df = pd.read_csv(file_path)

        # Remove unwanted columns
        full_df = full_df.drop(columns=delete_columns, errors="ignore")

        # Rename columns
        full_df = full_df.rename(columns=new_columns)

        # Save the processed file in Formatted_Data, maintaining folder structure
        if category == "None":
            base_folder = "formatted_data"
        else:
            category_folder_map = {
                "Magnetic (MAG)": "MAG",
                "Electromagnetic (EM)": "EM",
                "Radiometric (SPEC)": "SPEC",
                "Gravimetric (GRAV)": "GRAV"
            }
            base_folder = os.path.join("segmented_data", category_folder_map[category])

        # Final save path with preserved subfolder structure
        save_path = os.path.join(base_folder, selected_file)


        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        full_df.to_csv(save_path, index=False)

        # === LOG MODIFIED FILE ===
        log_path = "modified_log.txt"
        relative_path = selected_file.replace("\\", "/")  # Normalize path

        # Read existing log (if exists)
        if os.path.exists(log_path):
            with open(log_path, "r") as log_file:
                logged_files = log_file.read().splitlines()
        else:
            logged_files = []

        # Append only if not already logged
        if relative_path not in logged_files:
            with open(log_path, "a") as log_file:
                log_file.write(f"{relative_path}\n")

        st.success(f"File saved successfully: {save_path}")

else:
    st.warning("No CSV files found in the data folder.")
