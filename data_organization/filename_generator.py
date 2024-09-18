import os

def list_shapefiles_and_csvs(directory, output_file):
    """Traverse through the directory and list all shapefiles and CSV files."""
    shapefiles = []
    csv_files = []

    # Walk through the directory and its subdirectories
    for _, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".shp"):
                shapefiles.append(file)  # Add only the filename
            elif file.endswith(".csv"):
                csv_files.append(file)  # Add only the filename
    
    # Write the filenames to the output text file
    with open(output_file, 'w') as f:
        f.write("Shapefiles:\n")
        for shp in shapefiles:
            f.write(f"{shp}\n")
        
        f.write("\nCSV Files:\n")
        for csv in csv_files:
            f.write(f"{csv}\n")
    
    print(f"File listing completed. Results saved to {output_file}")

# Set the directory to search and the output file name
directory_to_search = "../data/processed/raster_data/EPSG_4326" 
output_file = "file_listing_2.txt"  # Output text file

# Run the function
list_shapefiles_and_csvs(directory_to_search, output_file)
