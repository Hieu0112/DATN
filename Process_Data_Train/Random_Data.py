import pandas as pd
import os

# Đọc file CSV ban đầu


# train_file = 'Data_Train/Vietnamese.csv'
# test_file = 'Data_Test/Test_Vietnamese.csv'

# df = pd.read_csv(f'Data_Collect/dataFake/Fake.csv')


train_file = 'Data_Train/English.csv'
test_file = 'Data_Test/Test_English.csv'

df = pd.read_csv(f'Data_Collect/dataEnglish/Train_English/True.csv')


df_sampled = df.sample(n=19500).reset_index(drop=True)

# Function to append data with header logic
def append_data(df_sampled, output_file):
    if not os.path.isfile(output_file) or os.stat(output_file).st_size == 0:
        # File chưa tồn tại hoặc trống, ghi với header
        df_sampled.to_csv(output_file, mode='a', header=True, index=False)
    else:
        # File đã tồn tại và có dữ liệu, ghi tiếp mà không thêm header
        df_sampled.to_csv(output_file, mode='a', header=False, index=False)

# Ghi dữ liệu mẫu vào file Train và kiểm tra tiêu đề
append_data(df_sampled, train_file)

# Lấy những dòng còn lại
df_remaining = df.drop(df_sampled.index)

# Ghi dữ liệu còn lại vào file Test và kiểm tra tiêu đề
append_data(df_remaining, test_file)

print("Hoàn tất ghi thêm dữ liệu vào file!")
