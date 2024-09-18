import os
import csv
from utils import move_files
from osgeo import gdal, osr

# Extract CRS from ERS file
def get_ers_crs(ers_file):
    """Retrieve the CRS from an ERS file using GDAL."""
    dataset = gdal.Open(ers_file)
    if not dataset:
        print(f"Unable to open {ers_file}")
        return None

    # Get the spatial reference (CRS) from the ERS file
    proj = dataset.GetProjection()
    if not proj:
        print(f"No CRS information found in {ers_file}")
        return None

    # Use the spatial reference system to parse the projection
    spatial_ref = osr.SpatialReference(wkt=proj)

    # Extract the authority and code (e.g., EPSG, IAU, etc.)
    authority = spatial_ref.GetAttrValue("AUTHORITY", 0)
    code = spatial_ref.GetAttrValue("AUTHORITY", 1)

    # Handle the case where authority or code is missing
    if authority and code:
        return f"{authority}_{code}"
    else:
        return "CRS_unknown"

# Convert ERS to CSV
def ers_to_csv(ers_path, output_csv_path):
    """Convert an ERS file to CSV format."""
    try:
        dataset = gdal.Open(ers_path)
        if not dataset:
            print(f"Unable to open {ers_path}")
            return None

        band = dataset.GetRasterBand(1)
        raster_data = band.ReadAsArray()
        geotransform = dataset.GetGeoTransform()

        # Write raster data to CSV
        with open(output_csv_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Longitude', 'Latitude', 'Value'])
            for row in range(raster_data.shape[0]):
                for col in range(raster_data.shape[1]):
                    x = geotransform[0] + col * geotransform[1] + row * geotransform[2]
                    y = geotransform[3] + col * geotransform[4] + row * geotransform[5]
                    value = raster_data[row, col]
                    csv_writer.writerow([x, y, value])

        print(f"ERS file {ers_path} converted to {output_csv_path}.")
    
    except Exception as e:
        print(f"Failed to convert {ers_path} to CSV: {e}")

# Check if file is empty
def is_ers_file_empty(ers_path):
    """Check if the ERS file is empty by inspecting its raster bands."""
    dataset = gdal.Open(ers_path)
    if not dataset:
        print(f"Unable to open {ers_path}")
        return True  # Consider it empty if it cannot be opened

    band = dataset.GetRasterBand(1)  # Get the first band
    if band is None:
        return True  # No raster data in the band
    
    raster_data = band.ReadAsArray()
    if raster_data is None or raster_data.size == 0:  # No data in the array
        return True

    return False  # File is not empty
        
# Process ERS files
def process_ers(folder, processed_folder, empty_files_folder, destination_folder, total_files, total_skipped, total_size_kb):
    for root, _, files in os.walk(folder):
        if processed_folder in root:
            continue

        for file in files:
            if file.lower().endswith('.ers'):
                total_files += 1
                ers_path = os.path.join(root, file)
                ers_size_kb = os.path.getsize(ers_path) / 1024  # KB
                total_size_kb += ers_size_kb
                
                if is_ers_file_empty(ers_path):
                    total_skipped += 1
                    total_size_kb = move_files(ers_path, ['.ERS', '', '.ERS.gi', '.ERS.aux.xml', '.ERS.xml', '.map', '.map.xml'], empty_files_folder, total_size_kb)
                    continue

                # Get CRS for the ERS file
                crs = get_ers_crs(ers_path)
                crs_folder = crs if crs else "CRS_unknown"

                # Create folder based on the extracted CRS
                output_folder = os.path.join(destination_folder, crs_folder)
                os.makedirs(output_folder, exist_ok=True)

                # Convert ERS to CSV and move the original ERS and CSV files
                csv_file_path = os.path.join(output_folder, f"{os.path.splitext(file)[0]}.csv")
                ers_to_csv(ers_path, csv_file_path)
                total_size_kb = move_files(ers_path, ['.ERS', '', '.ERS.gi', '.ERS.aux.xml', '.ERS.xml'], output_folder, total_size_kb)
        
    # Return updated totals
    return total_files, total_skipped, total_size_kb