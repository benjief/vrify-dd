import os
import geopandas as gpd

def convert_shapefiles_to_26911(main_folder, target_crs=26911):
    # Define the output folder for the converted files
    target_folder = os.path.join(main_folder, 'EPSG_26911_example')
    os.makedirs(target_folder, exist_ok=True)

    # Iterate through all subfolders and files in the main folder
    for main_folder, _, files in os.walk(main_folder):
        # Skip the output folder to prevent recursion into it
        if target_folder in main_folder:
            continue

        for file in files:
            # Process only shapefiles
            if file.endswith('.shp'):
                file_path = os.path.join(main_folder, file)

                try:
                    # Read the shapefile with geopandas
                    gdf = gpd.read_file(file_path)

                    # Check the CRS
                    current_crs = gdf.crs.to_epsg()
                    if current_crs != target_crs:
                        # If CRS is not the target CRS, convert it
                        print(f"Converting {file_path} from EPSG:{current_crs} to EPSG:{target_crs}...")

                        # Convert the CRS to EPSG:26911
                        gdf_converted = gdf.to_crs(epsg=target_crs)

                        # Create the output directory structure mirroring the input
                        relative_path = os.path.relpath(main_folder, main_folder)
                        output_dir = os.path.join(target_folder, relative_path)
                        os.makedirs(output_dir, exist_ok=True)

                        # Save the converted shapefile
                        output_file_path = os.path.join(output_dir, file)
                        gdf_converted.to_file(output_file_path)
                        print(f"Saved converted file to {output_file_path}")
                    else:
                        print(f"{file_path} is already in EPSG:{target_crs}, skipping conversion.")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

# Call conversion function
main_folder = '../data/processed/point_data'
convert_shapefiles_to_26911(main_folder)
