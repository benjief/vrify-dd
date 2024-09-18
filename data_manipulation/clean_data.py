import pandas as pd
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from utils import select_file, load_file, select_column

def get_cleaning_range(column_name):
    """Prompt the user for the inclusive range of values to keep in the selected column."""
    root = tk.Tk()
    root.withdraw()
    
    # Prompt for the lower bound
    lower_bound = simpledialog.askstring("Input", f"Enter the lower bound of the range for the column '{column_name}':")
    if lower_bound is None:
        messagebox.showerror("Error", "No lower bound provided.")
        return None, None
    
    # Prompt for the upper bound
    upper_bound = simpledialog.askstring("Input", f"Enter the upper bound of the range for the column '{column_name}':")
    if upper_bound is None:
        messagebox.showerror("Error", "No upper bound provided.")
        return None, None
    
    # Remove leading/trailing spaces and convert to numeric if possible
    lower_bound = lower_bound.strip()
    upper_bound = upper_bound.strip()

    # Convert to numeric values
    try:
        lower_bound = pd.to_numeric(lower_bound, errors='raise')
        upper_bound = pd.to_numeric(upper_bound, errors='raise')
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter numeric values for the range.")
        return None, None

    return lower_bound, upper_bound

def clean_data_by_range(df, column, lower_bound, upper_bound):
    """Remove rows from the DataFrame where the selected column is outside the specified inclusive range."""
    initial_count = len(df)
    
    # Check if the column is numeric
    if not pd.api.types.is_numeric_dtype(df[column]):
        messagebox.showerror("Error", f"Column '{column}' is not numeric.")
        return df
    
    # Remove rows outside the specified range (inclusive)
    df_cleaned = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    
    final_count = len(df_cleaned)
    rows_removed = initial_count - final_count
    
    print(f"Rows removed: {rows_removed}")
    return df_cleaned

def save_cleaned_file(df, file_path):
    """Save the cleaned DataFrame or GeoDataFrame to a file."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # Prompt the user to select a save location
    save_path = filedialog.asksaveasfilename(
        defaultextension=".csv" if file_path.endswith(".csv") else ".shp",
        filetypes=[("CSV files", "*.csv"), ("Shapefiles", "*.shp")],
        title="Save Cleaned File"
    )
    
    if save_path:
        if file_path.lower().endswith(".csv"):
            # Save as CSV
            df.to_csv(save_path, index=False)
        elif file_path.lower().endswith(".shp"):
            # Save as Shapefile
            df.to_file(save_path)
        print(f"File saved as: {save_path}")
    else:
        print("Save operation cancelled.")

# Main execution
file_path = select_file()

if file_path:
    # Load the file into a DataFrame/GeoDataFrame
    df = load_file(file_path)
    
    if df is not None:
        # Ask if the user wants to clean the data or skip to statistics
        root = tk.Tk()
        root.withdraw()
        user_choice = messagebox.askyesno("Data Cleaning", "Would you like to clean the data before proceeding to statistics?")
        
        if user_choice:
            # Prompt the user to select a column
            column_to_clean = select_column(df, "Which column would you like to clean?")
            
            # Prompt the user to input a range of values to keep
            lower_bound, upper_bound = get_cleaning_range(column_to_clean)
            
            if lower_bound is not None and upper_bound is not None:
                # Clean the data by the specified range
                df_cleaned = clean_data_by_range(df, column_to_clean, lower_bound, upper_bound)
                
                # Save the cleaned file
                save_cleaned_file(df_cleaned, file_path)
                df = df_cleaned  # Update df with the cleaned version
else:
    print("No file selected. Exiting...")
