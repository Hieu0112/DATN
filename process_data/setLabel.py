import csv
import re
csv_file="data_Json/dataset_real.csv"
csv_file="data_Json/dataset_fake.csv"

csv_file="dataFake/dataset_fake.csv"
csv_file="dataReal/dataset_real.csv"
csv_file_data="process_data/data_train.csv"

def Update_label(csv_file,csv_file_data):
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

        title= re.sub(r"[ '“,”\"]+", ' ', title)  # Thay thế dấu ' “,”
        text = re.sub(r"[ '“,”\"]+", ' ', text)  # Thay thế dấu ' “,”
        
        
        if 'fake' in csv_file:
            label = '1'
        # Ghi dữ liệu bài báo khi độ dài text > độ dài của title
        if len(text) > 2* len(title):
            article_data = {
                'title': title,
                'text': text.replace('\n', ' '),
                'author': author,
                'source_domain': source_domain,
                'label': label
            }
    
            # Ghi dữ liệu vào file CSV
            with open(csv_file_data, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['title', 'text', 'author', 'source_domain','label'])
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow(article_data)

if __name__ == '__main__':
    Update_label(csv_file,csv_file_data)
