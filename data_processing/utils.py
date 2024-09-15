import os
import shutil
import xml.etree.ElementTree as ET
import xml.dom.minidom

# Global size tracker
total_size_kb = 0

def prettify_xml(xml_path):
    """Prettify and format an XML file."""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        rough_string = ET.tostring(root, 'utf-8')
        reparsed = xml.dom.minidom.parseString(rough_string)
        pretty_xml_as_string = reparsed.toprettyxml(indent="    ")
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(pretty_xml_as_string)
        print(f"Prettified XML: {xml_path}")
    except Exception as e:
        print(f"Failed to prettify XML file {xml_path}: {e}")

def move_files(file_path, associated_exts, target_folder, total_size_kb):
    """Move files associated with shapefiles, TIFFs, or other files to the target folder."""
    base_name = os.path.splitext(file_path)[0]

    # Iterate over possible associated extensions (including empty extension)
    for ext in associated_exts:
        associated_file = base_name if ext == '' else base_name + ext

        if os.path.exists(associated_file):
            destination_file = os.path.join(target_folder, os.path.basename(associated_file))
            if ext.endswith('.xml'):
                prettify_xml(associated_file)
            shutil.move(associated_file, target_folder)
            print(f"Moved {associated_file} to {destination_file}")
            total_size_kb += os.path.getsize(destination_file) / 1024  # KB
            
    return total_size_kb