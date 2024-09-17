import pandas as pd
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from utils import select_file, load_file

def select_column(df):
    """Prompt the user to select which column to clean."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    available_columns = df.columns.tolist()
    column_name = simpledialog.askstring("Input", f"Available columns: {', '.join(available_columns)}\nWhich column would you like to clean?")
    
    if column_name not in available_columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    
    return column_name

def get_cleaning_value(column_name):
    """Prompt the user for the value to clean from the selected column."""
    root = tk.Tk()
    root.withdraw()
    
    cleaning_value = simpledialog.askstring("Input", f"Enter the value to clean in the column '{column_name}':")
    
    if cleaning_value is None:
        messagebox.showerror("Error", "No value provided for cleaning.")
        return None
    
    # Remove leading/trailing spaces
    cleaning_value = cleaning_value.strip()

    return cleaning_value

def clean_data(df, column, cleaning_value):
    """Remove rows from the DataFrame where the selected column contains the specified value."""
    initial_count = len(df)
    
    # Try to convert the cleaning value to a numeric type if possible
    try:
        # Attempt to convert cleaning_value to a number (int or float)
        cleaning_value_numeric = pd.to_numeric(cleaning_value, errors='coerce')
    except ValueError:
        cleaning_value_numeric = cleaning_value  # Keep it as a string if conversion fails

    # Check if the column is numeric and convert cleaning_value to numeric if necessary
    if pd.api.types.is_numeric_dtype(df[column]):
        # Perform cleaning with numeric comparison
        df_cleaned = df[df[column] != cleaning_value_numeric]
    else:
        # Perform cleaning with string comparison
        df_cleaned = df[df[column] != cleaning_value]
    
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
        # Prompt the user to select a column
        column_to_clean = select_column(df)
        
        # Prompt the user to input a value to clean
        cleaning_value = get_cleaning_value(column_to_clean)
        
        if cleaning_value is not None:
            # Clean the data
            df_cleaned = clean_data(df, column_to_clean, cleaning_value)
            
            # Display first 5 rows of cleaned data
            print(df_cleaned.head().to_markdown(index=False, numalign="left", stralign="left"))

            # Save the cleaned file
            save_cleaned_file(df_cleaned, file_path)
else:
    print("No file selected. Exiting...")
