import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
from scipy.interpolate import griddata
import tkinter as tk
from tkinter import simpledialog, filedialog
import rasterio
from rasterio.transform import from_origin
from utils import select_file, select_column

def get_heatmap_label():
    """Prompt the user for x-label, y-label, title, and legend label."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # Prompt for the x-label, y-label, and title
    x_label = simpledialog.askstring("Input", "Enter x-label for the heatmap:")
    y_label = simpledialog.askstring("Input", "Enter y-label for the heatmap:")
    plot_title = simpledialog.askstring("Input", "Enter title for the heatmap:")
    legend_label = simpledialog.askstring("Input", "Enter label for the legend:")
    
    return x_label, y_label, plot_title, legend_label   

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
from scipy.interpolate import griddata
import tkinter as tk
from tkinter import simpledialog
from utils import select_file, select_column

def get_heatmap_label():
    """Prompt the user for x-label, y-label, title, and legend label."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # Prompt for the x-label, y-label, and title
    x_label = simpledialog.askstring("Input", "Enter x-label for the heatmap:")
    y_label = simpledialog.askstring("Input", "Enter y-label for the heatmap:")
    plot_title = simpledialog.askstring("Input", "Enter title for the heatmap:")
    legend_label = simpledialog.askstring("Input", "Enter label for the legend:")
    
    return x_label, y_label, plot_title, legend_label    

def save_as_geotiff(grid_x, grid_y, grid_z, lon_min, lat_max, output_path):
    """Save the heatmap as a GeoTIFF file."""
    transform = from_origin(lon_min, lat_max, (grid_x[1, 0] - grid_x[0, 0]), (grid_y[0, 1] - grid_y[0, 0]))
    
    # Fix issues with transform (the transform introduces a 90-degree clockwise rotation)
    grid_z = np.transpose(grid_z)
    grid_z = np.flipud(grid_z)  

    with rasterio.open(
        output_path, 'w', driver='GTiff',
        height=grid_z.shape[0], width=grid_z.shape[1],
        count=1, dtype=grid_z.dtype, crs='EPSG:4326',
        transform=transform) as dst:
        dst.write(grid_z, 1)
    print(f"GeoTIFF saved to {output_path}")
    
def prompt_for_export(grid_x, grid_y, grid_z):
    """Ask the user if they want to export the heatmap as GeoTIFF."""
    root = tk.Tk()
    root.withdraw()
    
    export_format = simpledialog.askstring("Export", "Would you like to export the heatmap as a GeoTIFF? (Enter 'Yes' or 'No'):")
    if export_format.lower() == 'yes':
        file_path = filedialog.asksaveasfilename(defaultextension=".tif", filetypes=[("GeoTIFF files", "*.tif")])
        if file_path:
            save_as_geotiff(grid_x, grid_y, grid_z, grid_x.min(), grid_y.max(), file_path)
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

    # Create a GeoDataFrame
    geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry)
    
    # Extract longitude, latitude, and the selected column's data
    lon = df['Longitude']
    lat = df['Latitude']
    values = df[column_to_visualize]

    # Create a grid to interpolate the values onto
    grid_x, grid_y = np.mgrid[lon.min():lon.max():500j, lat.min():lat.max():500j]

    # Interpolate the selected column's values onto the grid
    grid_z = griddata((lon, lat), values, (grid_x, grid_y), method='cubic')
    
    # Prompt the user for x-label, y-label, title, and legend label
    x_label, y_label, plot_title, legend_label = get_heatmap_label()

    # Plot the interpolated heatmap
    plt.figure(figsize=(10, 8))
    heatmap = plt.pcolormesh(grid_x, grid_y, grid_z, cmap='hsv', shading='auto')
    plt.colorbar(heatmap).set_label(legend_label)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(plot_title)
    plt.show()
    
    # Prompt the user to export the heatmap as GeoTIFF
    prompt_for_export(grid_x, grid_y, grid_z)
else:
    print("No CSV file was selected. Exiting...")
