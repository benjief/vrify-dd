import os
import geopandas as gpd
import matplotlib.pyplot as plt
import random
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import textwrap
import tkinter as tk
from tkinter import filedialog

def get_column_for_classification(gdf, filename):
    """Prompt user to select a column for classification/coloring polygons."""
    print(f"Columns available in shapefile '{filename}' for classification:")
    for i, col in enumerate(gdf.columns):
        print(f"{i}. {col}")
    
    # Ask user to choose a column by index
    column_index = int(input(f"Enter the column number you'd like to use for coloring polygons in '{filename}': "))
    selected_column = gdf.columns[column_index]
    print(f"Selected column for classification: {selected_column}")
    
    return selected_column

def generate_random_colors(num_colors):
    """Generate a list of random colors."""
    colors = []
    for _ in range(num_colors):
        color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])  # Random HEX color
        colors.append(color)
    return colors

def select_shapefiles():
    """Open a file dialog to allow the user to select shapefiles."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # Open file dialog to select multiple shapefiles
    file_paths = filedialog.askopenfilenames(
        title="Select Shapefiles", 
        filetypes=[("Shapefiles", "*.shp")])  # Limit selection to shapefiles
    
    if file_paths:
        print(f"Selected files: {file_paths}")
    else:
        print("No files selected.")
    
    return file_paths

def plot_shapefiles_with_classification(shapefile_paths):
    """
    Opens shapefiles selected by the user, applies classification, and plots polygons, lines, and points with random colors.
    Uses file names for line and point data legend labels (without "Point" and "Line" descriptors).
    
    Parameters:
    - shapefile_paths: A list of shapefile paths selected by the user.
    """
    
    # Initialize separate lists for polygons, lines, and points
    polygon_gdfs = []
    line_gdfs = []
    point_gdfs = []

    # Iterate through each selected shapefile
    for file_path in shapefile_paths:
        print(f"Loading shapefile: {file_path}")
        
        try:
            # Load the shapefile into a GeoDataFrame
            gdf = gpd.read_file(file_path)
            filename = os.path.basename(file_path)
            
            # Separate layers by geometry type
            geom_type = gdf.geometry.type.unique()
            if 'Polygon' in geom_type or 'MultiPolygon' in geom_type:
                polygon_gdfs.append((gdf, filename))  # Add to polygons
            elif 'LineString' in geom_type or 'MultiLineString' in geom_type:
                line_gdfs.append((gdf, filename))  # Add to lines
            elif 'Point' in geom_type or 'MultiPoint' in geom_type:
                point_gdfs.append((gdf, filename))  # Add to points
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    # If there are no shapefiles, exit
    if not (polygon_gdfs or line_gdfs or point_gdfs):
        print("No shapefiles found.")
        return
    
    # Plot all the GeoDataFrames together with custom classification and symbology
    _, ax = plt.subplots(figsize=(12, 10))  # Increased the width for better display of the legend
    
    # Initialize lists for legend elements
    legend_elements = []

    # Plot polygons first (background layer)
    for gdf, filename in polygon_gdfs:
        # Prompt user for classification column
        column_for_classification = get_column_for_classification(gdf, filename)
        
        # Get unique values in the classification column
        unique_values = gdf[column_for_classification].unique()
        
        # Generate random colors for each unique value
        colors = generate_random_colors(len(unique_values))
        
        # Create a color map for the unique values
        color_map = dict(zip(unique_values, colors))
        
        # Plot polygons with colors based on the classification column and store in legend
        for value, color in color_map.items():
            wrapped_label = "\n".join(textwrap.wrap(f"{column_for_classification} ({filename}): {value}", width=50))
            gdf[gdf[column_for_classification] == value].plot(ax=ax, color=color, edgecolor='black', linewidth=0.5)
            legend_elements.append(Patch(facecolor=color, edgecolor='black', label=wrapped_label))

    # Plot lines next (middle layer)
    for gdf, filename in line_gdfs:
        # Automatically use the filename for line data (without "Line" label)
        line_description = filename.replace('.shp', '')  # Remove the file extension for labeling
        
        # Generate a random color for the lines
        line_color = generate_random_colors(1)[0]
        gdf.plot(ax=ax, color=line_color, linewidth=1.5)

        # Add lines to the legend using only the filename
        wrapped_label = "\n".join(textwrap.wrap(line_description, width=50))
        legend_elements.append(Line2D([0], [0], color=line_color, lw=2, label=wrapped_label))

    # Plot points last (top layer)
    for gdf, filename in point_gdfs:
        # Automatically use the filename for point data (without "Point" label)
        point_description = filename.replace('.shp', '')  # Remove the file extension for labeling
        
        # Generate a random color for the points
        point_color = generate_random_colors(1)[0]
        gdf.plot(ax=ax, color=point_color, marker='o', markersize=5)

        # Add points to the legend using only the filename
        wrapped_label = "\n".join(textwrap.wrap(point_description, width=50))
        legend_elements.append(Line2D([0], [0], marker='o', color='w', markerfacecolor=point_color, markersize=8, label=wrapped_label))

    # Create a combined legend and position it outside the plot (with more room)
    ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5))

    # Adjust the layout to give more room to the legend and move the map to the left
    plt.subplots_adjust(left=0.02, right=0.75, top=0.95, bottom=0.05)  # Push the map to the left and expand legend space on the right
    plt.show()

shapefile_paths = select_shapefiles()

plot_shapefiles_with_classification(shapefile_paths)