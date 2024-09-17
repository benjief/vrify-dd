import os
import geopandas as gpd
import pandas as pd

# Define the root directory
root_dir = "../data/processed/vector_data"
output_dir = os.path.join(root_dir, "EPSG_4326")

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def convert_shapefiles_to_4326(shapefile_path, output_dir):
    """Convert shapefiles to EPSG:4326 and save them to the output directory."""
    try:
        # Load the shapefile
        gdf = gpd.read_file(shapefile_path)
        # Convert CRS to EPSG:4326
        gdf = gdf.to_crs(epsg=4326)
        # Save the converted shapefile in the output directory
        output_shapefile = os.path.join(output_dir, os.path.basename(shapefile_path))
        gdf.to_file(output_shapefile)
        print(f"Converted {shapefile_path} to EPSG:4326.")
    except Exception as e:
        print(f"Error converting {shapefile_path}: {e}")

def convert_csv_to_4326(csv_path, output_dir):
    """Convert CSV files with latitude/longitude or X/Y columns to EPSG:4326."""
    try:
        # Check if the CSV file is empty
        if os.stat(csv_path).st_size == 0:
            print(f"Skipped empty file: {csv_path}")
            return

        # Try reading the CSV with UTF-8 encoding first, and fallback to ISO-8859-1 if it fails
        try:
            df = pd.read_csv(csv_path, encoding='utf-8')
        except UnicodeDecodeError:
            print(f"UTF-8 decoding failed for {csv_path}, trying ISO-8859-1.")
            df = pd.read_csv(csv_path, encoding='ISO-8859-1')

        # Convert column names to lowercase for case-insensitive comparison
        columns_lower = [col.lower() for col in df.columns]

        # Check for columns (Latitude, Longitude) or (X, Y)
        if 'latitude' in columns_lower and 'longitude' in columns_lower:
            gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']))
        elif 'x' in columns_lower and 'y' in columns_lower:
            gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['X'], df['Y']))
        else:
            print(f"Skipped file with no coordinates: {csv_path}")
            return
        
        # Set the original CRS if known, e.g., EPSG:4267 or EPSG:26711. Adjust based on your knowledge of the input CRS.
        gdf.set_crs(epsg=4267, inplace=True)  # Assuming input is NAD27, adjust as needed
        
        # Convert to EPSG:4326
        gdf = gdf.to_crs(epsg=4326)
        
        # Extract the updated coordinates and save back as CSV
        df['Longitude'], df['Latitude'] = gdf.geometry.x, gdf.geometry.y
        output_csv = os.path.join(output_dir, os.path.basename(csv_path))
        df.to_csv(output_csv, index=False)
        print(f"Converted {csv_path} to EPSG:4326.")
        
    except Exception as e:
        print(f"Error converting {csv_path}: {e}")


# Traverse the root directory and process subdirectories
for subdir, dirs, files in os.walk(root_dir):
    # Skip the EPSG_4326 directory
    if "EPSG_4326" in subdir:
        continue
    
    # Process files in the subdirectory
    for file in files:
        file_path = os.path.join(subdir, file)
        
        # Check if it's a shapefile
        if file.lower().endswith('.shp'):
            convert_shapefiles_to_4326(file_path, output_dir)
        
        # Check if it's a CSV file
        elif file.lower().endswith('.csv'):
            convert_csv_to_4326(file_path, output_dir)

print("CRS conversion completed for all files.")
