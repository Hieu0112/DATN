import pandas as pd

# Đọc file CSV
df = pd.read_csv('Data_Collect/dataReal/dataset_real.csv')

# Nhóm theo 'source_domain' và lấy tối đa 300 dòng cho mỗi domain
df_sampled = df.groupby('source_domain').apply(lambda x: x.sample(n=min(len(x), 1290))).reset_index(drop=True)

# Lưu kết quả vào file mới
df_sampled.to_csv('Data_Collect/dataReal/random_data.csv', index=False)

print("Hoàn tất!")
