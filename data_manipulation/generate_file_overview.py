import pandas as pd
import tkinter as tk
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt
from utils import select_file, load_file

def select_column(df):
    """Prompt the user to select which column to visualize, excluding Latitude and Longitude."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # Filter out columns related to Latitude and Longitude
    excluded_columns = ['latitude', 'longitude', 'lat', 'lon']
    available_columns = [col for col in df.columns if col.lower() not in excluded_columns]
    
    # Prompt for the column to visualize
    column_name = simpledialog.askstring("Input", f"Available columns: {', '.join(available_columns)}\nWhich column would you like to visualize?")
    
    if column_name not in available_columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    
    return column_name

def plot_histogram(df, column):
    """Plot a histogram of the selected column."""
    fig, ax = plt.subplots(figsize=(8, 6))
    df[column].hist(bins=50, ax=ax)
    
    # Label the axes
    ax.set_xlabel(column, fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    
    # Rotate the x-axis labels for better visibility
    plt.xticks(rotation=45, ha='right', fontsize=10)
    
    # Set title
    ax.set_title(f"Histogram of {column}", fontsize=14)
    
    # Automatically adjust layout to fit labels
    plt.tight_layout()
    
    # Show the plot
    plt.show()

def prompt_for_stats():
    """Ask the user if they want to generate key statistics."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    return messagebox.askyesno("Key Statistics", "Do you want to generate key statistics for any columns?")

def select_columns_for_stats(df):
    """Prompt the user to select columns for which to generate statistics."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Allow user to input columns separated by commas
    columns = simpledialog.askstring("Input", f"Enter columns (separated by commas) for which you want key statistics.\nAvailable columns: {', '.join(df.columns)}")

    # Split and clean the input into a list of columns
    selected_columns = [col.strip() for col in columns.split(',') if col.strip() in df.columns]
    return selected_columns

def generate_key_statistics(df, columns):
    """Generate key statistics (min, max, mean, median, mode, std, var) for selected columns."""
    for column in columns:
        print(f"\nStatistics for column: {column}")

        if pd.api.types.is_numeric_dtype(df[column]):
            print(f"Min: {df[column].min()}")
            print(f"Max: {df[column].max()}")
            print(f"Mean: {df[column].mean()}")
            print(f"Median: {df[column].median()}")
            print(f"Mode: {df[column].mode()[0] if not df[column].mode().empty else 'N/A'}")
            print(f"Standard Deviation: {df[column].std()}")
            print(f"Variance: {df[column].var()}")
            print(f"Skewness: {df[column].skew()}")
            print(f"Kurtosis: {df[column].kurt()}")
        elif pd.api.types.is_object_dtype(df[column]):
            print(f"Mode: {df[column].mode()[0] if not df[column].mode().empty else 'N/A'}")
        else:
            print(f"Column {column} is not numeric or categorical. Skipping...")

# Main execution
file_path = select_file()

if file_path:
    # Load the file into a DataFrame/GeoDataFrame
    df = load_file(file_path)
    
    if df is not None:
        # # Display the first 5 rows of data
        # print(df.head().to_markdown(index=False, numalign="left", stralign="left"))

        # Print the column names and their data types
        print(df.info())

        # Prompt the user to select the column to visualize
        column_to_visualize = select_column(df)

        # Plot a histogram of values for the selected column
        plot_histogram(df, column_to_visualize)

        # Ask the user if they want to generate key statistics
        if prompt_for_stats():
            # Let the user select columns for which to generate statistics
            columns_to_analyze = select_columns_for_stats(df)

            # Generate and display key statistics for the selected columns
            generate_key_statistics(df, columns_to_analyze)
else:
    print("No file selected. Exiting...")
