import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from scipy.interpolate import griddata
import tkinter as tk
from tkinter import simpledialog, filedialog
import rasterio
from rasterio.crs import CRS
from rasterio.transform import from_origin
from utils import select_file, select_column

def get_heatmap_labels():
    """Prompt the user for x-label, y-label, title, and legend label."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # Prompt for the x-label, y-label, and title
    x_label = simpledialog.askstring("Input", "Enter x-label for the heatmap:")
    y_label = simpledialog.askstring("Input", "Enter y-label for the heatmap:")
    plot_title = simpledialog.askstring("Input", "Enter title for the heatmap:")
    legend_label = simpledialog.askstring("Input", "Enter label for the legend:")
    
    return x_label, y_label, plot_title, legend_label    

def save_as_geotiff(x, y, Zi, output_path):
    """Save the heatmap as a GeoTIFF file."""
    transform = from_origin(x.min(), y.min(), (x.max() - x.min()) / Zi.shape[1], (y.min() - y.max()) / Zi.shape[0])
    
    # Fix issues with transform (the transform introduces a 90-degree clockwise rotation)
    # grid_z = np.transpose(grid_z)
    # grid_z = np.flipud(grid_z)  

    with rasterio.open(
        output_path, 'w', driver='GTiff',
        height=Zi.shape[0], width=Zi.shape[1],
        count=1, dtype=Zi.dtype, crs=CRS.from_epsg(4326),
        transform=transform) as dst:
        dst.write(Zi, 1)
    print(f"GeoTIFF saved to {output_path}")
    
def prompt_for_export(x, y, Zi):
    """Ask the user if they want to export the heatmap as GeoTIFF."""
    root = tk.Tk()
    root.withdraw()
    
    export_format = simpledialog.askstring("Export", "Would you like to export the heatmap as a GeoTIFF? (Enter 'Yes' or 'No'):")
    if export_format.lower() == 'yes':
        file_path = filedialog.asksaveasfilename(defaultextension=".tif", filetypes=[("GeoTIFF files", "*.tif")])
        if file_path:
            save_as_geotiff(x, y, Zi, file_path)
    else:
        print("No export requested.")

# Get the selected CSV file
csv_file_path = select_file([("CSV Files", "*.csv")])

# Proceed only if a file was selected
if csv_file_path:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Prompt the user to select the column to visualize
    column_to_visualize = select_column(df, "Which column would you like to generate a heatmap for?")

    if column_to_visualize:
        # Create a GeoDataFrame
        df.rename(columns={'Longitude': 'longitude', 'Latitude': 'latitude'}, inplace=True)
        df['geometry'] = gpd.points_from_xy(df.longitude, df.latitude)
        gdf = gpd.GeoDataFrame(df, geometry='geometry')
        gdf.crs = CRS.from_epsg(4326)
        
        # Extract longitude, latitude, and the selected column's data
        x = gdf.geometry.x.values
        y = gdf.geometry.y.values
        z = gdf[column_to_visualize].values

        # Create a grid to interpolate the values onto
        xi = np.linspace(x.min(), x.max(), 500)
        yi = np.linspace(y.min(), y.max(), 500)
        Xi, Yi = np.meshgrid(xi, yi)

        # Interpolate the selected column's values onto the grid
        Zi = griddata((x, y), z, (Xi, Yi), method='cubic')
        
        # Prompt the user for x-label, y-label, title, and legend label
        x_label, y_label, plot_title, legend_label = get_heatmap_labels()

        # Plot the interpolated heatmap
        plt.figure(figsize=(10, 8))
        heatmap = plt.pcolormesh(xi, yi, Zi, cmap='hsv', shading='auto')
        plt.colorbar(heatmap).set_label(legend_label)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(plot_title)
        plt.show()
        
        # Prompt the user to export the heatmap as GeoTIFF
        prompt_for_export(x, y, Zi)
    else:
        print("No column was selected. Exiting...")
else:
    print("No CSV file was selected. Exiting...")
