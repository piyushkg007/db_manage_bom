import pandas as pd

# Read the CSV files into Pandas DataFrames with explicit encoding
bom_df = pd.read_csv('bom.csv', encoding='ISO-8859-1')
database_df = pd.read_csv('database.csv', encoding='ISO-8859-1')

# Merge the DataFrames based on 'value' and 'PCB Footprint'
merged_df = pd.merge(bom_df, database_df, how='inner', on=['Value', 'PCB_Footprint'])

# Select the columns you want in the final result
result_df = merged_df[['Quantity', 'Reference', 'Value', 'PCB_Footprint', 'Part Number', 'Manufacturer', 'Description']]

# Print or save the result
print(result_df)
# result_df.to_csv('result.csv', index=False)  # Uncomment to save the result to a new CSV file
result_df.to_csv('result.csv', index=False)