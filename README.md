# CSV Editor & Formatter

## Overview
This interactive application allows users to **load, edit, and standardize large `.csv` files** efficiently.  
It enables:
- **Selecting only the required columns**
- **Renaming columns using predefined standard names**
- **Removing unnecessary columns**
- **Saving formatted files while maintaining the original folder structure**

Built using **Streamlit**, this tool was built to preprocess geophysics datasets for **machine learning models**.

---

## Features
- **Handles Large `.csv` Files Efficiently** – Works with large datasets without crashing  
- **Interactive UI with Dropdowns** – Easy selection & renaming of columns  
- **Preserves Folder Structure** – Saves formatted files in a structured way (`Formatted_Data/`)  
- **Quick Execution with Batch File** – Run the app with `run.bat`  

---

## Installation

### **1️. Clone the Repository**
```bash
git clone https://github.com/tashrifmahmud/CSV-Editor-App.git
cd CSV-Editor-App
```

### **2. Install Dependencies**
Make sure you have Python installed (preferably Python 3.10+).
Then, install required packages:
```bash
pip install -r requirements.txt
```
### **3. Run the Application**
Simply double-click `run.bat` to start the app.
Alternatively, you can run it manually:
```bash
streamlit run app.py
```
---

### How to Use
- Select a CSV file from the list.
- Choose which columns to keep or delete.
- Rename columns using the dropdown menu.
- Click "Apply Changes & Save" – The modified file is saved in formatted_data/, maintaining the folder structure.
