import os
from utils import move_files
import xml.etree.ElementTree as ET

# Extract CRS from .gdb.xml files
def extract_crs_from_xml(xml_file):
    """Extract the CRS (EPSG code) from a .gdb.xml file."""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Dynamically extract all namespaces from the XML file
        namespaces = extract_namespaces(xml_file)

        # Find the CRS information (EPSG code)
        projection = root.find('.//{*}projection', namespaces)
        if projection is not None:
            epsg_code = projection.attrib.get('wellknown_epsg')
            if epsg_code:
                return f"EPSG_{epsg_code}"
        
        return "CRS_unknown"
    
    except ET.ParseError as e:
        print(f"Error parsing {xml_file}: {e}")
        return "CRS_unknown"

def extract_namespaces(xml_file):
    """Extract all namespaces from the XML file dynamically."""
    events = "start", "start-ns"
    namespaces = {}
    for event, elem in ET.iterparse(xml_file, events):
        if event == "start-ns":
            prefix, uri = elem
            namespaces[prefix] = uri
    return namespaces

# Process gdb files
def process_gdb_files(folder, processed_folder, geosoft_gdbs_folder, total_gdb_files, total_size_kb):
    for root, _, files in os.walk(folder):
        # Skip files and directories inside of processed_folder
        if processed_folder in root:
            continue

        for file in files:
            if file.lower().endswith('.gdb.xml'):
                total_gdb_files += 1
                
                xml_file = os.path.join(root, file)

                # Extract CRS from the .gdb.xml file
                crs = extract_crs_from_xml(xml_file)
                crs_folder = crs if crs else "CRS_unknown"

                # Create folder based on the extracted CRS
                output_folder = os.path.join(geosoft_gdbs_folder, crs_folder)
                os.makedirs(output_folder, exist_ok=True)

                # Move the .gdb, .gdb.xml, and .csv files with the same prefix
                base_name = os.path.splitext(file)[0]  # Get the prefix without extension
                total_size_kb = move_files(os.path.join(root, base_name), ['.gdb', '.gdb.xml', '.csv'], output_folder, total_size_kb) 
                
    # Return updated totals
    return total_gdb_files, total_size_kb               