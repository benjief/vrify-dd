import geopandas as gpd
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os

# Function to select a CSV file using tkinter
def select_csv_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    file_path = filedialog.askopenfilename(
        title="Select CSV File", 
        filetypes=[("CSV files", "*.csv")]
    )
    return file_path

# Function to convert CRS from EPSG:4267 to EPSG:4326 and save to a new CSV file
def convert_crs(csv_file_path):
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)

        # Check if 'Longitude' and 'Latitude' columns exist
        if 'Longitude' not in df.columns or 'Latitude' not in df.columns:
            raise ValueError("CSV file must contain 'Longitude' and 'Latitude' columns.")

        # Convert DataFrame to a GeoDataFrame
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']))

        # Set the original CRS to EPSG:4267 (NAD27)
        gdf.set_crs(epsg=4267, inplace=True)

        # Convert to EPSG:4326 (WGS84)
        gdf = gdf.to_crs(epsg=4326)

        # Create a new file name with "_WGS94" suffix
        base, ext = os.path.splitext(csv_file_path)
        new_file_path = base + "_WGS84" + ext

        # Extract the converted longitude and latitude from the geometry
        df['Longitude'], df['Latitude'] = gdf.geometry.x, gdf.geometry.y

        # Save the converted DataFrame to a new CSV file
        df.to_csv(new_file_path, index=False)
        print(f"Converted CSV saved as: {new_file_path}")

    except Exception as e:
        print(f"Failed to convert CRS: {e}")

# Main execution
csv_file_path = select_csv_file()

if csv_file_path:
    convert_crs(csv_file_path)
else:
    print("No file selected.")
