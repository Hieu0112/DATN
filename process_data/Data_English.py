import csv
import re
import os
so_luong = 1
# Thư mục chứa các file CSV
csv_file = "Data_Collect/data_English/True.csv"
# csv_file = "Data_Collect/data_English/Real.csv" 

csv_file_data = "Train_data/English.csv"
def Update_label(csv_file, csv_file_data):
    global so_luong  # Khai báo sử dụng biến toàn cục
    # Đọc dữ liệu từ tệp CSV
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)  # Đọc tất cả các hàng vào danh sách

    for row in rows:
        title = row['title']
        text = row['text']
        subject = row['subject']
        date= row['date']
        label = '0'

        title = re.sub(r"[ '“,”\"]+", ' ', title).strip()  # Thay thế dấu ' “,”
        text = re.sub(r"[ '“,”\"]+", ' ', text).strip()  # Thay thế dấu ' “,”
        # Nếu file là file chứa tin thật, gán nhãn là 0
        # Nếu file là file chứa tin giả, gán nhãn là 1
        if 'fake' in csv_file.lower():
            label = '1'

        if so_luong <=19500:
            # Ghi dữ liệu bài báo khi độ dài text > độ dài của title
            if len(text) > 2 * len(title) and len(text) >= 100 :
                article_data = {
                    'title': title.replace('\n', ' '),
                    'text': text.replace('\n', ' '),
                    'label': label
                }
                so_luong+=1
        
                # Ghi dữ liệu vào file CSV
                with open(csv_file_data, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=['title', 'text', 'label'])
                    if file.tell() == 0:  # Nếu file trống thì ghi header
                        writer.writeheader()
                    writer.writerow(article_data)

if __name__ == '__main__':
    # Duyệt qua tất cả các file trong thư mục
    so_luong = 1
    Update_label(csv_file, csv_file_data)
    print(f"đã xử lý file: {csv_file}")
