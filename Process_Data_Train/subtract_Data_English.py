# Giảm số lượng data English về 19600 cả train cả test
import csv
import re
so_luong = 1
# Thư mục chứa các file CSV
Check_data = set()

Check="Fake"
csv_file = f"Data_Collect/dataEnglish/Details_English/{Check}.csv"
csv_file_data = f"Data_Collect/dataEnglish/Train_English/{Check}.csv"
def Update_label(csv_file, csv_file_data):
    global so_luong  # Khai báo sử dụng biến toàn cục
    # Đọc dữ liệu từ tệp CSV
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)  # Đọc tất cả các hàng vào danh sách

    for row in rows:
        title = row['title']
        text = row['text']
        label = '0'

        title = re.sub(r"[ '“,”\"]+", ' ', title)  # Thay thế dấu ' “,”
        text = re.sub(r"[ '“,”\"]+", ' ', text) # Thay thế dấu ' “,”
        title = title.replace(',', ' ')
        text = text.replace(',', ' ')

        if 'fake' in csv_file.lower():
            label = '1'

        if so_luong <=20500:
            # Ghi dữ liệu bài báo khi độ dài text > độ dài của title
            title_update = title.replace('\u2028', ' ').replace('\u2029', ' ').replace('\r', ' ').replace('\n', ' ')
            text_update = text.replace('\u2028', ' ').replace('\u2029', ' ').replace('\r', ' ').replace('\n', ' ').replace('Reuters',' ')

            lenSet=len(Check_data)

            Check_data.add(title_update +" "+ text_update)
            if len(text) > 2 * len(title) and len(text) >= 100 and lenSet+1==len(Check_data):
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
