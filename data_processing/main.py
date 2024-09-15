import os
from process_shapefiles import process_shapefiles
# from process_shapefiles import process_tiffs
# from process_shapefiles import process_gdb_files
# from process_shapefiles import process_xyz_files
# from process_shapefiles import process_ers_files

# Define root folder and processed folders
root_folder = '../data'
processed_folder = os.path.join(root_folder, 'processed')
shapefiles_folder = os.path.join(processed_folder, 'shapefiles')
empty_shapefiles_folder = os.path.join(processed_folder, 'empty_shapefiles')
tiffs_folder = os.path.join(processed_folder, 'tiffs')
geosoft_gdbs_folder = os.path.join(processed_folder, 'geosoft_gdbs')
xyz_folder = os.path.join(processed_folder, 'xyz')
empty_xyz_files_folder = os.path.join(processed_folder, 'empty_xyz_files')
ers_folder = os.path.join(processed_folder, 'ers_grids')
empty_ers_files_folder = os.path.join(processed_folder, 'empty_ers_files')

# Ensure directories exist
os.makedirs(processed_folder, exist_ok=True)
os.makedirs(shapefiles_folder, exist_ok=True)
os.makedirs(empty_shapefiles_folder, exist_ok=True)
os.makedirs(tiffs_folder, exist_ok=True)
os.makedirs(geosoft_gdbs_folder, exist_ok=True)
os.makedirs(xyz_folder, exist_ok=True)
os.makedirs(empty_xyz_files_folder, exist_ok=True)
os.makedirs(ers_folder, exist_ok=True)
os.makedirs(empty_ers_files_folder, exist_ok=True)

# Initialize total counts
total_shapefiles, total_tiff_files, total_gdb_files, total_xyz_files, total_ers_files = 0, 0, 0, 0, 0
total_shapefiles_skipped, total_xyz_files_skipped, total_ers_files_skipped, total_size_kb = 0, 0, 0, 0

# Run processing functions and accumulate results
total_shapefiles, total_skipped, total_size_kb = process_shapefiles(root_folder, processed_folder, empty_shapefiles_folder, shapefiles_folder, total_shapefiles, total_shapefiles_skipped, total_size_kb)
# total_tiff_files, total_size_kb = process_tiffs(root_folder, processed_folder, tiffs_folder, total_tiff_files, total_size_kb)
# total_gdb_files, total_size_kb = process_gdb_files(root_folder, processed_folder, geosoft_gdbs_folder, total_gdb_files, total_size_kb)
# total_xyz_files, total_size_kb = process_xyz_files(root_folder, processed_folder, empty_xyz_files_folder, xyz_folder, total_xyz_files, total_xyz_files_skipped, total_size_kb)
# total_ers_files, total_size_kb = process_ers_files(root_folder, processed_folder, empty_ers_files_folder, ers_folder, total_ers_files, total_xyz_files_skipped, total_size_kb)

# Write the summary file
summary_file_path = os.path.join(processed_folder, 'summary.txt')
with open(summary_file_path, 'w') as summary_file:
    summary_file.write(f"Total shapefiles processed: {total_shapefiles}\n")
    summary_file.write(f"Total shapefiles skipped (empty): {total_shapefiles_skipped}\n")
    summary_file.write(f"Total TIFF files processed: {total_tiff_files}\n")
    summary_file.write(f"Total GDB files processed: {total_gdb_files}\n")
    summary_file.write(f"Total XYZ files processed: {total_xyz_files}\n")
    summary_file.write(f"Total XYZ skipped (empty): {total_xyz_files_skipped}\n")
    summary_file.write(f"Total ERS files processed: {total_ers_files}\n")
    summary_file.write(f"Total ERS skipped (empty): {total_ers_files_skipped}\n")
    summary_file.write(f"Total size of processed files (excluding CSVs): {total_size_kb:.2f} kB\n")

print(f"Summary written to {summary_file_path}")