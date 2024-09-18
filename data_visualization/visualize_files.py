import folium
from folium.plugins import HeatMap
import pandas as pd
import geopandas as gpd
import tkinter as tk
from tkinter import filedialog, simpledialog
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def select_files(file_type):
    """Open a file dialog to select multiple files of a given type."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    file_paths = filedialog.askopenfilenames(title=f"Select {file_type} files", 
                                             filetypes=[(file_type, f"*.{file_type}")])
    return list(file_paths)

def select_column(df):
    """Prompt the user to select which column to visualize, excluding Latitude and Longitude."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # Filter out columns related to Latitude and Longitude
    excluded_columns = ['latitude', 'longitude', 'lat', 'lon', 'x', 'y']
    available_columns = [col for col in df.columns if col.lower() not in excluded_columns]
    
    # Prompt the user to select which column to visualize
    column_name = simpledialog.askstring("Input", f"Available columns: {', '.join(available_columns)}\nWhich column would you like to visualize?")
    
    if column_name not in available_columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    
    return column_name

def select_shapefile_column(gdf):
    """Prompt the user to select which column to visualize in the shapefile."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    available_columns = gdf.columns.tolist()  # Get all attribute columns
    
    # Prompt the user to select which column to visualize
    column_name = simpledialog.askstring("Input", f"Available columns: {', '.join(available_columns)}\nWhich column would you like to visualize?")
    
    if column_name not in available_columns:
        raise ValueError(f"Column '{column_name}' not found in the shapefile.")
    
    return column_name

def find_lat_lon_columns(df):
    """Find latitude and longitude (or equivalent) columns in the DataFrame."""
    possible_lat_columns = ['latitude', 'lat', 'y', 'Y']
    possible_lon_columns = ['longitude', 'lon', 'x', 'X']
    
    lat_column = next((col for col in df.columns if col.lower() in [name.lower() for name in possible_lat_columns]), None)
    lon_column = next((col for col in df.columns if col.lower() in [name.lower() for name in possible_lon_columns]), None)
    
    if lat_column is None or lon_column is None:
        raise ValueError("Error: Could not find Latitude and Longitude columns in the file.")
    
    return lat_column, lon_column

def plot_shapefiles(map_obj, shapefiles):
    """Plot multiple shapefiles on the map without custom styling."""
    for shapefile in shapefiles:
        gdf = gpd.read_file(shapefile)
        
        folium.GeoJson(
            gdf.to_json(), 
            name=shapefile.split('/')[-1]
        ).add_to(map_obj)

def plot_lines(map_obj, line_files):
    """Plot multiple line CSV files on the map, with proper handling of negative values."""
    for line_file in line_files:
        df = pd.read_csv(line_file)
        
        try:
            lat_column, lon_column = find_lat_lon_columns(df)
        except ValueError as e:
            print(f"{e} in file {line_file}.")
            continue
        
        # Ask the user to select which column to visualize
        try:
            value_column = select_column(df)
        except ValueError as e:
            print(f"{e} in file {line_file}.")
            continue
        
        values = df[value_column]

        # Handle negative values by shifting the range if necessary
        min_value = values.min()
        if min_value < 0:
            values += abs(min_value)  # Shift the values so they are all positive for color mapping

        # Normalize the selected column values to a range of 0-1 after shift
        norm = plt.Normalize(vmin=values.min(), vmax=values.max())

        # Use a diverging colormap (e.g., 'coolwarm') for more variability
        colormap = plt.get_cmap('coolwarm')

        # Plot the line segments, coloring each segment based on the normalized value
        for i in range(len(df) - 1):
            coords = [(df.iloc[i][lat_column], df.iloc[i][lon_column]), (df.iloc[i + 1][lat_column], df.iloc[i + 1][lon_column])]
            value = df.iloc[i][value_column]
            
            # Map the value to a color using the colormap
            color = mcolors.to_hex(colormap(norm(value)))  # Convert the color to hex for folium
            
            folium.PolyLine(locations=coords, color=color, weight=2.5, opacity=0.8, name=line_file.split('/')[-1]).add_to(map_obj)


def plot_heatmaps(map_obj, heatmap_files):
    """Plot heatmaps with negative values handled appropriately."""
    for heatmap_file in heatmap_files:
        df = pd.read_csv(heatmap_file)
        
        try:
            lat_column, lon_column = find_lat_lon_columns(df)
        except ValueError as e:
            print(f"{e} in file {heatmap_file}.")
            continue
        
        # Ask the user to select the column for heatmap visualization
        try:
            value_column = select_column(df)
        except ValueError as e:
            print(f"{e} in file {heatmap_file}.")
            continue
        
        values = df[value_column]
        
        # To handle negative values, shift the data by adding the absolute minimum value to all values if necessary
        min_value = values.min()
        if min_value < 0:
            values += abs(min_value)  # Shift values to ensure all are positive for heatmap generation

        # Create heatmap data using the adjusted value column
        heat_data = [[row[lat_column], row[lon_column], row[value_column]] for index, row in df.iterrows()]

        # Customize the heatmap for a smoother look
        heatmap = HeatMap(heat_data, name=heatmap_file.split('/')[-1], 
                          radius=20, blur=30, max_zoom=1, 
                          gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'})  # Adjust these values as needed
        
        map_obj.add_child(heatmap)

# Main execution
# Create a base map
base_map = folium.Map(location=[39.5, -119.5], zoom_start=8)  # Adjust location based on your data

# Ask the user to select shapefiles
shapefiles = select_files("shp")
if shapefiles:
    plot_shapefiles(base_map, shapefiles)

# Ask the user to select CSV files for line plotting
line_files = select_files("csv")
if line_files:
    plot_lines(base_map, line_files)

# Ask the user to select CSV files for heatmaps
heatmap_files = select_files("csv")
if heatmap_files:
    plot_heatmaps(base_map, heatmap_files)

# Add a layer control to toggle between different layers
folium.LayerControl().add_to(base_map)

# Save the map to an HTML file
base_map.save('interactive_map.html')
