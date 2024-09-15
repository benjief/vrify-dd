import os
import geopandas as gpd
from utils import move_files

def get_shapefile_crs(shapefile):
    crs = shapefile.crs.to_string().replace(":", "_").replace("/", "_") if shapefile.crs else 'CRS_unknown'
    return crs

def process_shapefiles(folder, processed_folder, empty_shapefiles_folder, shapefiles_folder, total_shapefiles, total_shapefiles_skipped, total_size_kb):
    """Process shapefiles and return updated totals."""
    for root, _, files in os.walk(folder):
        if processed_folder in root:
            continue
        for file in files:
            if file.lower().endswith('.shp'):
                total_shapefiles += 1
                shapefile_path = os.path.join(root, file)
                shapefile_size_kb = os.path.getsize(shapefile_path) / 1024  # KB
                total_size_kb += shapefile_size_kb

                try:
                    gdf = gpd.read_file(shapefile_path)
                except Exception as e:
                    print(f"Error reading {shapefile_path}: {e}")
                    continue

                if gdf.empty:
                    total_shapefiles_skipped += 1
                    total_size_kb = move_files(shapefile_path, ['.shp', '.shx', '.dbf', '.prj', '.cpg', '.sbn', '.sbx', '.shp.xml'], empty_shapefiles_folder, total_size_kb)
                    continue

                crs = get_shapefile_crs(gdf)
                output_folder = os.path.join(shapefiles_folder, crs)
                os.makedirs(output_folder, exist_ok=True)

                csv_file_path = os.path.join(output_folder, f"{os.path.splitext(file)[0]}.csv")
                gdf.to_csv(csv_file_path, index=False)
                print(f"Processed {shapefile_path} into {csv_file_path}")

                total_size_kb = move_files(shapefile_path, ['.shp', '.shx', '.dbf', '.prj', '.cpg', '.sbn', '.sbx', '.shp.xml'], output_folder, total_size_kb)

    # Return the updated totals
    return total_shapefiles, total_shapefiles_skipped, total_size_kb