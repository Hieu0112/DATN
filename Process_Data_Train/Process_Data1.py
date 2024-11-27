# Giảm số lượng data English về 19600 cả train cả test
import csv
import re
so_luong = 1
# Thư mục chứa các file CSV
# 0 tin thật, 1 tin giả
import sys

csv.field_size_limit(10**9)
check_2 = set()
check_3 = set()

def check_dup(file_name):
    with open(file_name, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        for row in rows:
            title = row['title']
            text = row['text']
            title_update = title.replace('\u2028', '').replace('\u2029', '').replace('\r', '').replace('\n', '')
            text_update = text.replace('\u2028', '').replace('\u2029', '').replace('\r', '').replace('\n', '').replace('Reuters','')
            check_2.add(title_update)
            check_3.add(text_update)

file1 = "Data_Collect/dataEnglish/Train_English/True.csv"
file2 = "Data_Collect/dataEnglish/Train_English/Fake.csv"


csv_file = "Data_Collect/dataEnglish/Details_English/Data_1.csv"
csv_file_data = "Data_Collect/dataEnglish/Train_English/Train1.csv"


def Update_label(csv_file, csv_file_data):
    global so_luong  
    check_dup(file1)
    check_dup(file2)

    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)  # Đọc tất cả các hàng vào danh sách

    for row in rows:
        title = row['title']
        text = row['text']
        label = row['label']

        title = re.sub(r"[ '“,”\"]+", ' ', title).strip()  # Thay thế dấu ' “,”
        text = re.sub(r"[ '“,”\"]+", ' ', text).strip()  # Thay thế dấu ' “,”

        if so_luong <=20000:
            # Ghi dữ liệu bài báo khi độ dài text > độ dài của title
            title_update = title.replace('\u2028', '').replace('\u2029', '').replace('\r', '').replace('\n', '')
            text_update = text.replace('\u2028', '').replace('\u2029', '').replace('\r', '').replace('\n', '').replace('Reuters','')

            len2=len(check_2)
            len3=len(check_3)

            check_2.add(title_update)
            check_3.add(text_update)
            if len(text) > 2 * len(title) and len(text) >= 100 and len2+1==len(check_2)and len3+1==len(check_3):
                article_data = {
                    'title': title_update,
                    'text': text_update,
                    'label': label
                }
                so_luong += 1
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
