import os
from utils import move_files

def process_other(folder, processed_folder, destination_folder, total_files, total_size_kb):
    for root, _, files in os.walk(folder):
        if processed_folder in root:
            continue
        for file in files:
            total_files += 1
            file_path = os.path.join(root, file)
            file_size_kb = os.path.getsize(file_path) / 1024  # KB
            total_size_kb += file_size_kb
        
            total_size_kb = move_files(file_path, ['.pdf', '.xslt', '.GeosoftMeta'], destination_folder, total_size_kb) # TODO: Add to this list if other files remain
                    
    # Return the updated totals
    return total_files, total_size_kb