import pandas as pd
from sklearn.model_selection import train_test_split

# Load the cleaned dataset
df = pd.read_csv('cleaned_dataset.csv')

# Split into train and test
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Save training dataset with all columns
train_df.to_csv('train_data.csv')

# In testing dataset, keep only selected columns (for example, dropping the target or extra columns)
# Let's say you want to drop a column called 'target' and 'extra_feature' (adjust based on your data)
columns_to_keep_in_test = ['Airline','Flight Number','Aircraft','Dep_Temp','Dep_Humidity','Dep_Condition','Arr_Temp','Arr_Humidity','Arr_Condition','Departure Date','Arrival Date']  # <-- replace with the columns you want
test_df_reduced = test_df[columns_to_keep_in_test]

# Save the testing dataset
test_df_reduced.to_csv('test_data.csv')

print("Training and reduced Testing datasets have been created and saved.")
