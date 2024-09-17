import geopandas as gpd
import pandas as pd
import os

# Define the directories for vector and raster data
output_dir = "../data/processed"
vector_data_dir = "../data/processed/vector_data/EPSG_4326"
raster_data_dir = "../data/processed/raster_data/EPSG_4326"

# Store bounding boxes for comparison
bounding_boxes = []

def get_bounding_box(gdf):
    """Calculate the bounding box of a GeoDataFrame."""
    minx, miny, maxx, maxy = gdf.total_bounds
    return {'minx': minx, 'miny': miny, 'maxx': maxx, 'maxy': maxy}

def check_overlap(bbox1, bbox2):
    """Check if two bounding boxes overlap."""
    return not (bbox1['maxx'] < bbox2['minx'] or
                bbox1['minx'] > bbox2['maxx'] or
                bbox1['maxy'] < bbox2['miny'] or
                bbox1['miny'] > bbox2['maxy'])

def process_shapefile(file_path):
    """Process shapefile and calculate bounding box."""
    gdf = gpd.read_file(file_path)
    bbox = get_bounding_box(gdf)
    return bbox

def process_csv(file_path):
    """Process CSV file and calculate bounding box."""
    df = pd.read_csv(file_path)
    
    # Standardize column names to lowercase for case-insensitive checks
    df.columns = df.columns.str.lower()

    # Check for latitude/longitude or x/y columns
    if 'latitude' in df.columns and 'longitude' in df.columns:
        lat_col, lon_col = 'latitude', 'longitude'
    elif 'y' in df.columns and 'x' in df.columns:
        lat_col, lon_col = 'y', 'x'
    else:
        print(f"CSV file {file_path} does not contain Latitude/Longitude or X/Y columns.")
        return None

    # Calculate the bounding box
    min_lat = df[lat_col].min()
    max_lat = df[lat_col].max()
    min_lon = df[lon_col].min()
    max_lon = df[lon_col].max()

    return {'minx': min_lon, 'miny': min_lat, 'maxx': max_lon, 'maxy': max_lat}

# Traverse the vector data directory and process shapefiles and CSV files
for subdir, dirs, files in os.walk(vector_data_dir):
    for file in files:
        file_path = os.path.join(subdir, file)
        
        # Check if it's a shapefile
        if file.lower().endswith('.shp'):
            bbox = process_shapefile(file_path)
            if bbox:
                bounding_boxes.append({'file': file, 'bbox': bbox})  # Add just the filename
        
        # Check if it's a CSV file (for vector data)
        elif file.lower().endswith('.csv'):
            bbox = process_csv(file_path)
            if bbox:
                bounding_boxes.append({'file': file, 'bbox': bbox})  # Add just the filename

# Traverse the raster data directory and process CSV files (assuming these represent raster data)
for subdir, dirs, files in os.walk(raster_data_dir):
    for file in files:
        file_path = os.path.join(subdir, file)
        
        # Check if it's a CSV file (for raster data)
        if file.lower().endswith('.csv'):
            bbox = process_csv(file_path)
            if bbox:
                bounding_boxes.append({'file': file, 'bbox': bbox})  # Add just the filename

# Compare bounding boxes to find overlaps
overlap_results = []
for i in range(len(bounding_boxes)):
    for j in range(i+1, len(bounding_boxes)):
        file1 = bounding_boxes[i]['file']
        file2 = bounding_boxes[j]['file']
        bbox1 = bounding_boxes[i]['bbox']
        bbox2 = bounding_boxes[j]['bbox']
        
        if check_overlap(bbox1, bbox2):
            overlap_results.append((file1, file2)) # Avoids redundant entries

# Write the results to a text file
output_file = os.path.join(output_dir, "overlap_summary.txt")

with open(output_file, 'w') as f:
    if overlap_results:
        f.write("Overlapping files:\n")
        for file1, file2 in overlap_results:
            f.write(f"{file1} overlaps with {file2}\n")
    else:
        f.write("No overlapping files found.\n")

print(f"Overlap results written to {output_file}")
