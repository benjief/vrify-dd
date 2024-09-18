import os
from process_shapefile import process_shapefile
from process_tiff import process_tiff
from process_gdb import process_gdb
from process_xyz import process_xyz
from process_ers import process_ers
from process_csv import process_csv
from process_other import process_other
from utils import count_folders

# Define root folder and processed folders
root_folder = '../data'
processed_folder = os.path.join(root_folder, 'processed')
vector_data_folder = os.path.join(processed_folder, 'vector_data')
raster_data_folder = os.path.join(processed_folder, 'raster_data')
other_data_folder = os.path.join(processed_folder, 'other_data')
empty_data_folder = os.path.join(processed_folder, 'empty_data')

# Ensure directories exist
os.makedirs(processed_folder, exist_ok=True)
os.makedirs(vector_data_folder, exist_ok=True)
os.makedirs(raster_data_folder, exist_ok=True)
os.makedirs(other_data_folder, exist_ok=True)
os.makedirs(empty_data_folder, exist_ok=True)

# Initialize total counts
total_shapefiles = 0
total_tiffs = 0
total_gdb = 0
total_xyz = 0
total_ers = 0
total_csv = 0
total_pdf = 0
total_other = 0
new_folders = 1 # Accounts for the "processed" folder

# Initialize skipped counts and total size
total_skipped = 0
total_size_kb = 0

# Run processing functions and accumulate results
total_shapefiles, total_skipped, total_size_kb = process_shapefile(root_folder, processed_folder, empty_data_folder, vector_data_folder, total_shapefiles, total_skipped, total_size_kb)
total_tiffs, total_size_kb = process_tiff(root_folder, processed_folder, raster_data_folder, total_tiffs, total_size_kb)
total_gdb, total_size_kb = process_gdb(root_folder, processed_folder, vector_data_folder, total_gdb, total_size_kb)
total_xyz, total_skipped, total_size_kb = process_xyz(root_folder, processed_folder, empty_data_folder, vector_data_folder, total_xyz, total_skipped, total_size_kb)
total_ers, total_skipped, total_size_kb = process_ers(root_folder, processed_folder, empty_data_folder, raster_data_folder, total_ers, total_skipped, total_size_kb)
total_csv, total_skipped, total_size_kb = process_csv(root_folder, processed_folder, empty_data_folder, vector_data_folder, total_csv, total_skipped, total_size_kb)
total_other, total_size_kb = process_other(root_folder, processed_folder, other_data_folder, total_other, total_size_kb)

# Summary data
summary_data = {
    "Total shapefiles processed": total_shapefiles,
    "Total TIFF files processed": total_tiffs,
    "Total GDB files processed": total_gdb,
    "Total XYZ files processed": total_xyz,
    "Total ERS files processed": total_ers,
    "Total CSV files processed": total_csv,
    "Total other files processed": total_other,
    "Total size of processed files (kB)": f"{total_size_kb:.2f}",
    "New folders created": f"{count_folders(processed_folder)}",
    "Total files skipped (empty)": total_skipped
}

# Write the summary file
summary_file_path = os.path.join(processed_folder, 'summary.txt')
with open(summary_file_path, 'w') as summary_file:
    for label, value in summary_data.items():
        summary_file.write(f"{label}: {value}\n")

print(f"Summary written to {summary_file_path}")