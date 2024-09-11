import csv
import os
csv_file="data/data_real.csv"
csv_file_data="data/data_train_update.csv"

def reset_processed_field(csv_file,csv_file_data):
    # Đọc dữ liệu từ tệp CSV
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)  # Đọc tất cả các hàng vào danh sách

    for row in rows:
        title = row['title']
        text = row['text']
        author = row['author']
        source_domain= row['source_domain']
        label='0'
        
        if 'fake' in csv_file:
            label = '1'

        if source_domain == 'nhandan.vn':
            author = "nhandan"

        article_data = {
            'title': title,
            'text': text.replace('\n', '.'),
            # 'date': date,
            'author': author,
            'source_domain': source_domain,
            'label': label
        }
    
        # Ghi dữ liệu vào file CSV
        with open(csv_file_data, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['title', 'text', 'author', 'source_domain','label'])
            if file.tell() == 0:
                writer.writeheader()
            # Ghi dữ liệu bài báo
            writer.writerow(article_data)

if __name__ == '__main__':
    reset_processed_field(csv_file,csv_file_data)
