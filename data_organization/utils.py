import os
import shutil

def move_files(file_path, associated_exts, target_folder, total_size_kb):
    base_name = os.path.splitext(file_path)[0]

    # Iterate over possible associated extensions (including empty extension)
    for ext in associated_exts:
        associated_file = base_name if ext == '' else base_name + ext
        
        if os.path.exists(associated_file):
            destination_file = os.path.join(target_folder, os.path.basename(associated_file))
            # if ext.endswith('.xml'):
            #     prettify_xml(associated_file)
            shutil.move(associated_file, target_folder)
            print(f"Moved {associated_file} to {destination_file}")
            total_size_kb += os.path.getsize(destination_file) / 1024  # KB
            
    return total_size_kb


def count_folders(processed_folder_path):
    """
    Counts the number of distinct folders created inside the 'processed' folder.
    
    Args:
    processed_folder_path (str): The path to the 'processed' folder, relative or absolute. 
                                 Default is 'processed', assumed to be one level below the script's root.

    Returns:
    int: The total count of distinct folders created inside the 'processed' folder.
    """
    # Check if the processed folder exists
    if not os.path.exists(processed_folder_path):
        print(f"The folder '{processed_folder_path}' does not exist.")
        return 0

    # Count the number of directories inside the processed folder
    folder_count = sum(os.path.isdir(os.path.join(processed_folder_path, name)) for name in os.listdir(processed_folder_path))

    return folder_count
