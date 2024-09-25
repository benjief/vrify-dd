import pandas as pd
import geopandas as gpd
import tkinter as tk
from tkinter import filedialog, simpledialog
import tkinter as tk
from tkinter import filedialog

def select_file(filetype=None):
    """
    Open a file dialog to allow the user to select a file based on specified file types.
    
    Parameters:
    filetype (list of tuples): Optional parameter to specify file types. 
                               Format: [("Description", "*.extension"), ...].
                               If None, defaults to CSV and Shapefiles.
    
    Returns:
    str: The file path of the selected file.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Default to CSV and Shapefiles if no filetype is provided
    if filetype is None:
        filetype = [("CSV and Shapefiles", "*.csv;*.shp")]
    
    # Open file dialog to select a file based on the provided or default file type
    file_path = filedialog.askopenfilename(
        title="Select a File", 
        filetypes=filetype)  # Limit selection to specified file types

    if file_path:
        print(f"Selected file: {file_path}")
    else:
        print("No file selected.")
    
    return file_path


def load_file(file_path):
    """Load the selected file into a DataFrame or GeoDataFrame."""
    if file_path.lower().endswith('.csv'):
        # Try reading the CSV with UTF-8 encoding first, and fallback to ISO-8859-1 if it fails
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            print(f"UTF-8 decoding failed for {file_path}, trying ISO-8859-1.")
            df = pd.read_csv(file_path, encoding='ISO-8859-1')
    elif file_path.lower().endswith('.shp'):
        # Load Shapefile into geopandas GeoDataFrame
        df = gpd.read_file(file_path)
    else:
        print(f"Unsupported file type: {file_path}")
        return None
    return df

def select_column(df, prompt):
    """Prompt the user to select a column."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # List the available columns vertically
    available_columns = '\n'.join(df.columns.tolist())  # Join columns with newlines
    column_name = simpledialog.askstring("Input", f"Available columns:\n\n{available_columns}\n\n{prompt}")
    
    if column_name is None or column_name == "":
        return None
    
    if column_name not in df.columns:
        print(f"Column '{column_name}' not found in DataFrame.")
        return None
    
    return column_name

def select_multiple_columns(df, prompt):
    """Prompt the user to select columns."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # List the available columns vertically
    available_columns = '\n'.join(df.columns.tolist())  # Join columns with newlines

    # Allow user to input columns separated by commas
    columns = simpledialog.askstring("Input", f"{prompt}\n\nAvailable columns:\n\n{available_columns}")
    
    # Handle cancel or empty input
    if columns is None or columns.strip() == "":
        print("No columns selected.")
        return None

    # Split and clean the input into a list of columns
    selected_columns = [col.strip() for col in columns.split(',') if col.strip() in df.columns]
    
    if not selected_columns:
        return None

    return selected_columns

