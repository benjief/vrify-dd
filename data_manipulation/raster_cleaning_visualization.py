import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
from scipy.interpolate import griddata
import tkinter as tk
from tkinter import filedialog, simpledialog


def select_csv_file():
    """Open a file dialog to allow the user to select a CSV file."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # Open file dialog to select a CSV file
    file_path = filedialog.askopenfilename(
        title="Select CSV File", 
        filetypes=[("CSV files", "*.csv")])  # Limit selection to CSV files
    
    if file_path:
        print(f"Selected file: {file_path}")
    else:
        print("No file selected.")
    
    return file_path

def get_histogram_labels():
    """Prompt the user for x-label, y-label, and title."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # Prompt for the x-label, y-label, and title
    x_label = simpledialog.askstring("Input", "Enter x-label for the histogram:")
    y_label = simpledialog.askstring("Input", "Enter y-label for the histogram:")
    plot_title = simpledialog.askstring("Input", "Enter title for the histogram:")
    
    return x_label, y_label, plot_title

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

# Get rid of display limits
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Get the selected CSV file
csv_file_path = select_csv_file()

# Proceed only if a file was selected
if csv_file_path:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Display the first 5 rows of data
    print(df.head().to_markdown(index=False, numalign="left", stralign="left"))

    # Print the column names and their data types
    print(df.info())

    # Prompt the user for x-label, y-label, and title
    x_label, y_label, plot_title = get_histogram_labels()
    
    # Plot a histogram of values
    df['Value'].hist(bins=50, figsize=(8, 6))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(plot_title)
    plt.show()
    
    # Proceed with cleaning (or not, depending on what the user chooses)
    proceed_cleaning = simpledialog.askstring("Input", "Do you want to proceed with data cleaning? (yes/no):")

    if proceed_cleaning.lower() == 'yes':
        value_to_drop = -999999
        df = df[df['Value'] != value_to_drop]
    else:
        print("Skipping data cleaning.")

    # Create a GeoDataFrame
    geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry)
    
    # Extract longitude, latitude, and Bouguer gravity anomaly data
    lon = df['Longitude']
    lat = df['Latitude']
    values = df['Value']

    # Create a grid to interpolate the values onto
    grid_x, grid_y = np.mgrid[lon.min():lon.max():500j, lat.min():lat.max():500j]

    # Interpolate Bouguer anomaly values onto the grid
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
else:
    print("No CSV file was selected. Exiting...")
