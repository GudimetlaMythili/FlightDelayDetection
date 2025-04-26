import pandas as pd
from sklearn.model_selection import train_test_split

# Step 1: Load the dataset
df = pd.read_csv('cleaned_dataset.csv')

# Step 2: Select only the required columns
selected_columns = ['Airline', 'Aircraft', 'Dep_Temp', 'Dep_Humidity', 'Dep_Condition',
                    'Arr_Temp', 'Arr_Humidity', 'Arr_Condition']
df_selected = df[selected_columns]

# Step 3: Split into training and testing sets (e.g. 80% train, 20% test)
train_df, test_df = train_test_split(df_selected, test_size=0.2, random_state=42)

# Step 4: Save the datasets
train_df.to_csv(r'C:\Users\imuda\OneDrive\Desktop\train_data.csv', index=False)
test_df.to_csv(r'C:\Users\imuda\OneDrive\Desktop\test_data.csv', index=False)

print("✅ Training and testing datasets saved successfully.")
