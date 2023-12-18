import pandas as pd

# Read the CSV files into Pandas DataFrames with explicit encoding
bom_df = pd.read_csv('bom.csv', encoding='ISO-8859-1')

# Convert relevant columns to uppercase in bom_df
bom_df['Value'] = bom_df['Value'].str.upper()
bom_df['PCB Footprint'] = bom_df['PCB Footprint'].str.upper()

database_df = pd.read_csv('database.csv', encoding='ISO-8859-1')

# Convert relevant columns to uppercase in database_df
database_df['Value'] = database_df['Value'].str.upper()
database_df['PCB Footprint'] = database_df['PCB Footprint'].str.upper()

# Merge the DataFrames based on 'Value' and 'PCB Footprint'
merged_df = pd.merge(bom_df, database_df, how='left', on=['Value', 'PCB Footprint'])

# Select the columns you want in the final result
result_df = merged_df[['Quantity', 'Reference', 'Value', 'PCB Footprint', 'Part Number', 'Manufacturer', 'Description']]

# Identify rows where data is not found in the database
not_found_df = result_df[result_df['Part Number'].isnull()]

# Save the result to a new CSV file
result_df.to_csv('result.csv', index=False)

# Print the result
print(result_df)

# Print the values for parts where data is not found in the database
if not_found_df.shape[0] > 0:
    print("\nRows where data is not found in the database:")
    print(not_found_df[['Value', 'PCB Footprint']])
else:
    print("\nAll rows have matching data in the database.")
import pandas as pd

# Read the result CSV file
result_df = pd.read_csv('result.csv')

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

# Print the result
print(result_df)

# Save the updated result to a new CSV file
result_df.to_csv('result_updated.csv', index=False)
import pandas as pd

# Read the updated result CSV file
result_df = pd.read_csv('result_updated.csv')

# Remove duplicates between 'Part Number' and 'Alternative Part Number'
result_df['Part Number'] = result_df['Part Number'].apply(lambda x: ', '.join(sorted(set(str(x).split(', ')))))
result_df['Part Number_alternative'] = result_df['Part Number_alternative'].apply(lambda x: ', '.join(sorted(set(str(x).split(', ')))))

# Print the updated result
print(result_df)

# Save the final result to a new CSV file
result_df.to_csv('final_Bom'+' '+'.csv', index=False)