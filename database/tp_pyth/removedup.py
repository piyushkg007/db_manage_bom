import pandas as pd

def remove_duplicates(input_file, output_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_file)

    # Remove duplicates from every column
    df_no_duplicates_col = df.apply(lambda x: x.drop_duplicates(), axis=0)

    # Remove duplicates from every row
    df_no_duplicates_row = df_no_duplicates_col.T.apply(lambda x: x.drop_duplicates(), axis=1).T

    # Save the cleaned DataFrame to a new CSV file
    df_no_duplicates_row.to_csv(output_file, index=False)

if __name__ == "__main__":
    # Specify the input and output file paths
    input_csv_file = "result.csv"
    output_csv_file = "output_no_duplicates.csv"

    # Call the function to remove duplicates
    remove_duplicates(input_csv_file, output_csv_file)

    print(f"Duplicates removed and saved to {output_csv_file}")
