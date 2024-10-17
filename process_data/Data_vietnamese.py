import csv
import re
import os

# Thư mục chứa các file CSV
directory = "Data_Collect/dataFake/Details_Fake/"
csv_file_data = "Data_Collect/dataFake/Fake.csv"


# directory = "Data_Collect/dataReal/Details_Real/"
# csv_file_data = "Data_Collect/dataReal/Real.csv"

def Update_label(csv_file, csv_file_data):
    # Đọc dữ liệu từ tệp CSV
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)  # Đọc tất cả các hàng vào danh sách
 
    for row in rows:
        title = row['title']
        text = row['text']
        author = row['author']
        source_domain= row['source_domain']
        label = '0'

        title = re.sub(r"[ '“,”\"]+", ' ', title).strip()  # Thay thế dấu ' “,”
        text = re.sub(r"[ '“,”\"]+", ' ', text).strip()  # Thay thế dấu ' “,”
        # Nếu file là file chứa tin thật, gán nhãn là 0
        # Nếu file là file chứa tin giả, gán nhãn là 1
        if 'fake' in csv_file.lower():
            label = '1'

        # Ghi dữ liệu bài báo khi độ dài text > độ dài của title
        if len(text) > 2 * len(title) and len(text) >= 300 and len(title) > 0:
            article_data = {
                'title': title.replace('\n', ' '),
                'text': text.replace('\n', ' '),
                'label': label
            }
    
    
            # Ghi dữ liệu vào file CSV
            with open(csv_file_data, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['title', 'text', 'label'])
                if file.tell() == 0:  # Nếu file trống thì ghi header
                    writer.writeheader()
                writer.writerow(article_data)

if __name__ == '__main__':
    # Duyệt qua tất cả các file trong thư mục
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):  # Chỉ xử lý các file CSV
            csv_file = os.path.join(directory, filename)
            if 'url' not in csv_file.lower():
            # if 'url' not in csv_file.lower() and csv_file !="Data_Collect/dataReal/dataset_real.csv":
                Update_label(csv_file, csv_file_data)
                print(f"đã xử lý file: {csv_file}")
