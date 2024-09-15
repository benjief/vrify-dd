import os
import csv
from utils import move_files
from osgeo import gdal

def get_tiff_crs(tiff_path):
    """Retrieve the CRS from a TIFF file using GDAL."""
    dataset = gdal.Open(tiff_path)
    if not dataset:
        print(f"Unable to open {tiff_path}")
        return None
    proj = dataset.GetProjection()
    spatial_ref = gdal.osr.SpatialReference(wkt=proj)
    authority = spatial_ref.GetAttrValue("AUTHORITY", 0)
    code = spatial_ref.GetAttrValue("AUTHORITY", 1)
    return f"{authority}_{code}" if authority and code else "CRS_unknown"

def tiff_to_csv(tiff_path, output_csv_path):
    """Convert a TIFF file to CSV."""
    dataset = gdal.Open(tiff_path)
    band = dataset.GetRasterBand(1)
    raster_data = band.ReadAsArray()
    geotransform = dataset.GetGeoTransform()
    with open(output_csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Longitude', 'Latitude', 'Value'])
        for row in range(raster_data.shape[0]):
            for col in range(raster_data.shape[1]):
                x = geotransform[0] + col * geotransform[1] + row * geotransform[2]
                y = geotransform[3] + col * geotransform[4] + row * geotransform[5]
                csv_writer.writerow([x, y, raster_data[row, col]])

def process_tiffs(folder, processed_folder, tiffs_folder, total_tiff_files, total_size_kb):
    """Process TIFF files and return updated totals."""
    for root, _, files in os.walk(folder):
        if processed_folder in root:
            continue
        for file in files:
            if file.lower().endswith('.tiff'):
                total_tiff_files += 1
                tiff_path = os.path.join(root, file)
                tiff_size_kb = os.path.getsize(tiff_path) / 1024  # KB
                total_size_kb += tiff_size_kb

                crs = get_tiff_crs(tiff_path)
                crs_folder = crs if crs else "CRS_unknown"
                output_folder = os.path.join(tiffs_folder, crs_folder)
                os.makedirs(output_folder, exist_ok=True)
                csv_file_path = os.path.join(output_folder, f"{os.path.splitext(file)[0]}.csv")
                tiff_to_csv(tiff_path, csv_file_path)
                total_size_kb = move_files(tiff_path, ['.tiff', '.tiff.aux.xml'], output_folder, total_size_kb)

    # Return updated totals
    return total_tiff_files, total_size_kb
