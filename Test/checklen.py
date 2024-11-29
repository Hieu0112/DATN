import pandas as pd
import os
import re
from collections import Counter
# Đọc tệp CSV vào DataFrame (thay 'your_file.csv' bằng tên tệp CSV của bạn)
file1 = os.path.join("Data_Train", "train1.csv")
file2 = os.path.join("Data_Train", "train2.csv")
file3 = os.path.join("Data_Train", "train3.csv")

data_df1 = pd.read_csv(file1, encoding='utf-8')
data_df2 = pd.read_csv(file2, encoding='utf-8')
data_df3 = pd.read_csv(file3, encoding='utf-8')

# Ghép ba DataFrame lại với nhau
data_df = pd.concat([data_df1, data_df2, data_df3], ignore_index=True)

# Tạo cột 'combined' kết hợp 'title' và 'text'
data_df['combined'] = data_df['title'].fillna('') + ' ' + data_df['text'].fillna('')

# Tách chuỗi thành các từ và loại bỏ dấu câu
all_words = data_df['combined'].str.split().explode().apply(lambda x: re.sub(r'\W+', '', x))

# Đếm số lần xuất hiện của mỗi từ
word_counts = Counter(all_words)

# Chuyển kết quả thành DataFrame
word_counts_df = pd.DataFrame(word_counts.items(), columns=['Word', 'Count'])

# Sắp xếp DataFrame theo cột 'Count' (số lần xuất hiện) giảm dần
word_counts_df = word_counts_df.sort_values(by='Count', ascending=False)

# Lưu DataFrame vào một tệp CSV
word_counts_df.to_csv('word_counts.csv', index=False)
