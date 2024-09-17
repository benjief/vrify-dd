import pandas as pd
import geopandas as gpd
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import matplotlib.pyplot as plt

def select_file():
    """Open a file dialog to allow the user to select a CSV or Shapefile."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open file dialog to select a CSV or Shapefile
    file_path = filedialog.askopenfilename(
        title="Select CSV or Shapefile", 
        filetypes=[("CSV and Shapefiles", "*.csv;*.shp")])  # Limit selection to CSV and Shapefiles

    if file_path:
        print(f"Selected file: {file_path}")
    else:
        print("No file selected.")
    
    return file_path

def load_file(file_path):
    """Load the selected file into a DataFrame or GeoDataFrame."""
    if file_path.lower().endswith('.csv'):
        # Load CSV into pandas DataFrame
        df = pd.read_csv(file_path)
    elif file_path.lower().endswith('.shp'):
        # Load Shapefile into geopandas GeoDataFrame
        df = gpd.read_file(file_path)
    else:
        print(f"Unsupported file type: {file_path}")
        return None
    return df