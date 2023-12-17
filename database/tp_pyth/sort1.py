import os
import pandas as pd

# Function to process a single file
def process_file(file_path, database_df):
    # Read the BOM file
    bom_df = pd.read_excel(file_path)

    # Convert relevant columns to uppercase in bom_df
    bom_df['Value'] = bom_df['Value'].str.upper()
    bom_df['PCB Footprint'] = bom_df['PCB Footprint'].str.upper()

    # Merge the DataFrames based on 'Value' and 'PCB Footprint'
    merged_df = pd.merge(bom_df, database_df, how='left', on=['Value', 'PCB Footprint'])

    # Select the columns you want in the final result
    result_df = merged_df[['Quantity', 'Reference', 'Value', 'PCB Footprint', 'Part Number', 'Manufacturer', 'Description']]

    # Identify rows where data is not found in the database
    not_found_df = result_df[result_df['Part Number'].isnull()]

    # Save the result to a new CSV file with the file name
    result_file_name = f"result_{os.path.splitext(os.path.basename(file_path))[0]}.csv"
    result_df.to_csv(result_file_name, index=False)

    # Print the result
    print(f"\nProcessed file: {file_path}")
    print(result_df)

    # Print the values for parts where data is not found in the database
    if not_found_df.shape[0] > 0:
        print("\nRows where data is not found in the database:")
        print(not_found_df[['Value', 'PCB Footprint']])
    else:
        print("\nAll rows have matching data in the database.")

    # Return the result file name
    return result_file_name

# Read the database CSV file
database_df = pd.read_csv('database.csv', encoding='ISO-8859-1')

# Specify the folder containing .xlsx files
folder_path = 'file'

# Process each .xlsx file in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.xlsx'):
        file_path = os.path.join(folder_path, file_name)
        process_file(file_path, database_df)

# Read the result CSV files back and process duplicates
for file_name in os.listdir(folder_path):
    if file_name.startswith('result_') and file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)

        # Read the result CSV file
        result_df = pd.read_csv(file_path)

        # Identify and handle duplicates based on the 'Reference' column
        duplicate_reference_mask = result_df.duplicated(subset=['Reference'], keep=False)

        # Create a mapping for duplicate 'Reference' values
        reference_mapping = result_df.groupby('Reference').agg({
            'Part Number': lambda x: ', '.join(x.dropna().astype(str).unique()),
            'Manufacturer': lambda x: ', '.join(x.dropna().astype(str).unique())
        }).reset_index()

        # Merge the mapping back to the original dataframe
        result_df = pd.merge(result_df, reference_mapping, on='Reference', how='left', suffixes=('', '_alternative'))

        # Drop duplicate rows based on the 'Reference' column
        result_df = result_df.drop_duplicates(subset=['Reference'])

        # Remove duplicates between 'Part Number' and 'Alternative Part Number'
        result_df['Part Number'] = result_df['Part Number'].apply(lambda x: ', '.join(sorted(set(str(x).split(', ')))))
        result_df['Part Number_alternative'] = result_df['Part Number_alternative'].apply(lambda x: ', '.join(sorted(set(str(x).split(', ')))))

        # Save the final result to a new CSV file with the file name
        final_result_file_name = f"final_{file_name}"
        result_df.to_csv(final_result_file_name, index=False)

        # Print the final result
        print(f"\nProcessed final result file: {file_name}")
        print(result_df)
