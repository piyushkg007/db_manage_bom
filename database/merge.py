import os
import pandas as pd

# Set the path to the folder containing Excel workbooks
folder_path = 'files'

# Initialize an empty list to store DataFrames
dfs = []

# Specify columns to extract
columns_to_extract = ['Value', 'Part Number', 'Manufacturer', 'Description', 'PCB Footprint']

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.xlsx'):  # Assuming your files are in Excel format
        file_path = os.path.join(folder_path, filename)
        
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path)
        
        # Check if all specified columns exist in the DataFrame
        if set(columns_to_extract).issubset(df.columns):
            # Extract specific columns
            df_subset = df[columns_to_extract]
            
            # Append the subset to the list of DataFrames
            dfs.append(df_subset)
        else:
            print(f"Columns not found in {filename}. Skipping.")

# Check if there are DataFrames to concatenate
if dfs:
    # Concatenate all DataFrames in the list
    consolidated_data = pd.concat(dfs, ignore_index=True)

    # Save the consolidated data to a new CSV file
    consolidated_data.to_csv('database.csv', index=False)

    print("Data has been successfully extracted and saved to database.csv.")
else:
    print("No data to process.")
