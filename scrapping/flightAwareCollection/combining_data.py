import pandas as pd

# Load both datasets
df1 = pd.read_csv('srapping/detailed_flight_data2.csv')
df2 = pd.read_csv('srapping/detailed_flight_data32.csv')

# Combine datasets by stacking rows
combined_df = pd.concat([df1, df2], axis=0, ignore_index=True)

# (Optional) Remove duplicate rows if needed
# combined_df = combined_df.drop_duplicates()

# Save the combined dataset
combined_df.to_csv('all_flight_data.csv', index=False)

print("Datasets combined and saved as 'combined_flight_data.csv'.")
