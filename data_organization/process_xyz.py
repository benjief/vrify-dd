import os
import csv
from utils import move_files

# Magnetic data headers (from metadata)
magnetic_headers = [
    'Flight line number', 'Fiducial number', 'Time (hhmmss)', 'Julian day', 'Year',
    'Latitude', 'Longitude', 'Radar Altimeter (meters)', 'Total magnetic field value (nanoTeslas)',
    'Residual magnetic field value (nanoTeslas)', 'Diurnal (nanoTeslas)', 'Geology (coded)', 
    'Residual magnetic field (comprehensive model CM4)'
]

# Radiometric data headers (from metadata)
radiometric_headers = [
    'Flight line number', 'Fiducial number', 'Time (hhmmss)', 'Julian day', 'Year', 'Latitude',
    'Longitude', 'Radar Altimeter (meters)', 'Residual magnetic field value (nanoTeslas)',
    'Geology (coded)', 'Quality flag', 'Apparent Potassium (%)', 'Apparent Uranium (ppm eU)',
    'Apparent Thorium (ppm eTh)', 'Uranium-Thorium ratio', 'Uranium-Potassium ratio',
    'Thorium-Potassium ratio', 'Total count (counts/second)', 'Atmospheric Bismuth 214 (counts/second)',
    'Air temperature (°C)', 'Air pressure (mmHg)'
]

# Convert XYZ to CSV with appropriate headers (based on metadata)
def xyz_to_csv(xyz_path, output_csv_path, headers):
    try:
        with open(xyz_path, 'r') as xyz_file, open(output_csv_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            
            # Write headers to CSV
            csv_writer.writerow(headers)

            # Write the XYZ data to CSV
            for line in xyz_file:
                # Strip any extra whitespace and split the line on whitespace (handling multiple spaces)
                row = line.strip().split()

                # Ensure valid rows (skip empty lines)
                if len(row) >= len(headers):
                    # Write row data (matching the number of headers)
                    csv_writer.writerow(row[:len(headers)])

        print(f"XYZ file {xyz_path} converted to {output_csv_path}.")
    
    except Exception as e:
        print(f"Failed to convert {xyz_path} to CSV: {e}")

# Check if file is empty
def is_xyz_file_empty(xyz_file):
    try:
        with open(xyz_file, 'r') as f:
            for line in f:
                if line.strip():  # Check if there's a non-empty line
                    return False
    except Exception as e:
        print(f"Error reading {xyz_file}: {e}")
        return True

    return True  # File is empty if no non-empty lines are found

# Process XYZ files
def process_xyz(folder, processed_folder, empty_files_folder, destination_folder, total_files, total_skipped, total_size_kb):
    for root, _, files in os.walk(folder):
        if processed_folder in root:
            continue

        for file in files:
            if file.lower().endswith('.xyz'):
                total_files += 1
                xyz_path = os.path.join(root, file)
                xyz_size_kb = os.path.getsize(xyz_path) / 1024  # KB
                total_size_kb += xyz_size_kb
                
                if is_xyz_file_empty(xyz_path):
                    total_skipped += 1
                    total_size_kb = move_files(xyz_path, ['.xyz'], empty_files_folder, total_size_kb)
                    continue
                
                # Determine which headers to use based on the filename
                if 'mag' in file.lower():
                    headers = magnetic_headers
                elif 'rad' in file.lower():
                    headers = radiometric_headers
                else:
                    print(f"Unknown file type for {file}, skipping.")
                    continue  # Skip if the file doesn't match known types

                # CRS for the XYZ file (NAD27 assumed from metadata)
                crs_folder = "EPSG_4267"

                # Create folder based on the extracted CRS
                output_folder = os.path.join(destination_folder, crs_folder)
                os.makedirs(output_folder, exist_ok=True)

                # Convert XYZ to CSV and move the original XYZ and CSV files
                csv_file_path = os.path.join(output_folder, f"{os.path.splitext(file)[0]}.csv")
                xyz_to_csv(xyz_path, csv_file_path, headers)
                total_size_kb = move_files(xyz_path, ['.xyz'], output_folder, total_size_kb)
                
                # Split file name to account for other files associated with XYZ files (JPG and TXT)
                xyz_path_without_data_suffix = xyz_path.rsplit('_', 1)[0]
                total_size_kb = move_files(xyz_path_without_data_suffix, ['.jpg'], output_folder, total_size_kb)
                total_size_kb = move_files(f"{xyz_path_without_data_suffix}_meta", ['.txt'], output_folder, total_size_kb)
                
    # Return updated totals
    return total_files, total_skipped, total_size_kb