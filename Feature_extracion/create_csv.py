import pandas as pd

# File paths for the two CSV files
file1_path = 'data.csv'
file2_path = 'color_array.csv'

# Read the CSV files into pandas DataFrames
df1 = pd.read_csv(file1_path)
df2 = pd.read_csv(file2_path)

# Combine the DataFrames
combined_df = pd.concat([df1, df2], axis=1)

# Specify the file path for the combined CSV file
combined_csv_path = 'combined_file.csv'

# Write the combined DataFrame to a new CSV file
combined_df.to_csv(combined_csv_path, index=False)

print(f"Combined CSV file '{combined_csv_path}' has been created.")
