import pandas as pd

# Đọc file CSV
type_file="Fake"

df = pd.read_csv(f'Data_Collect/data{type_file}/{type_file}.csv')

# Lấy ngẫu nhiên 300 dòng không phân biệt domain
df_sampled = df.sample(n=6000).reset_index(drop=True)

# Lưu kết quả mẫu vào file mới
df_sampled.to_csv(f'Train_data/Vietnamese/Train_{type_file}.csv', index=False)

df_remaining = df.drop(df_sampled.index)

# Lưu những data còn lại vào file Test_True.csv
df_remaining.to_csv(f'Train_data/Vietnamese/Test_{type_file}.csv', index=False)

print("Hoàn tất!")
