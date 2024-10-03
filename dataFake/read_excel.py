import pandas as pd
import os
import re
import csv

# Đọc file Excel không có tiêu đề cột và chỉ lấy 3 cột đầu tiên
df = pd.read_excel('file_xlsx/bbc_com.xlsx', header=None, usecols=[0, 1, 2])

# Đặt tên cho các cột tương ứng với Title, Text, Author
df.columns = ['title', 'text', 'author']

# Tên file CSV bạn muốn tạo
csv_file = 'dataset_fake.csv'

# Kiểm tra nếu file CSV chưa tồn tại, tạo file và thêm tiêu đề
if not os.path.exists(csv_file) or os.stat(csv_file).st_size == 0:
    with open(csv_file, mode='w', encoding='utf-8', newline='') as file:
        file.write('title,text,author,source_domain\n')  # Viết tiêu đề (header) vào file CSV

# Đọc từng dòng và ghi vào CSV
for index, row in df.iterrows():
    title = row['title']
    text = row['text']
    author = row['author']
    source_domain= 'bbc.com'

    # Xử lý Text: Xóa \n và thay các chuỗi khoảng trắng thừa bằng dấu chấm.
    text = text.replace('\n', ' ')  # Thay thế \n bằng khoảng trắng
    text = re.sub(r'\s+', ' ', text)  # Thay thế nhiều khoảng trắng bằng dấu chấm

    article_data = {
        'title': title,
        'text': text.replace('\n', '.'),
        # 'date': date,
        'author': author,
        'source_domain': source_domain
    }
    
    # Ghi dữ liệu vào file CSV
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'text', 'author', 'source_domain'])
                
        # Ghi dữ liệu bài báo
        writer.writerow(article_data)
