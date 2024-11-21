## Tách data train và data test
import pandas as pd
import os

# Đọc file CSV ban đầu


# train_file = 'Data_Train/Vietnamese.csv'
# test_file = 'Data_Test/Test_Vietnamese.csv'

# df = pd.read_csv(f'Data_Collect/dataFake/Fake.csv')
# df = pd.read_csv(f'Data_Collect/dataReal/Real.csv')
max_data=19500


train_file = 'Data_Train/English.csv'
test_file = 'Data_Test/Test_English.csv'

df = pd.read_csv(f'Data_Collect/dataEnglish/Train_English/Fake.csv')


# Sample without replacement and set a random seed
df_sampled = df.head(max_data)
# Function to append data with header logic
def append_data(df_to_append, output_file):
    if not os.path.isfile(output_file) or os.stat(output_file).st_size == 0:
        # Write with header if file doesn't exist or is empty
        df_to_append.to_csv(output_file, mode='a', header=True, index=False)
    else:
        # Append without header if file already exists with data
        df_to_append.to_csv(output_file, mode='a', header=False, index=False)

# Write sampled data to the training file
append_data(df_sampled, train_file)

# Get the remaining rows for the test dataset
df_remaining = df.tail(len(df) - max_data)

# Write remaining data to the test file
append_data(df_remaining, test_file)
