import os
import csv
from utils import move_files

def is_csv_empty(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        return not any(reader)  # Returns True if there are no rows
    

def process_csv(folder, processed_folder, empty_files_folder, destination_folder, total_files, total_skipped, total_size_kb, new_folders):
    for root, _, files in os.walk(folder):
        if processed_folder in root:
            continue
        for file in files:
            if file.lower().endswith('.csv'):
                total_files += 1
                csv_path = os.path.join(root, file)
                csv_size_kb = os.path.getsize(csv_path) / 1024  # KB
                total_size_kb += csv_size_kb
                
                if is_csv_empty(csv_path):
                    total_skipped += 1
                    total_size_kb = move_files(csv_path, ['.csv'], empty_files_folder, total_size_kb)

                total_size_kb = move_files(csv_path, ['.csv'], destination_folder, total_size_kb, new_folders)
                    
    # Return the updated totals
    return total_files, total_skipped, total_size_kb, new_folders
                