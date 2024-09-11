import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

# URL của trang cần thu thập dữ liệu
# url = "https://vietnamnet.vn/thoi-su-page2"
# url ="https://vietnamnet.vn/chinh-tri-page6"
# url= "https://thanhnien.vn/thoi-su/quyen-duoc-biet.htm"
# name_class_page = 'box-title-text'
# name_class_page = 'vnn-title'
# name_class_page='article-title'

# url = "https://baomoi.com/an-ninh-trat-tu.epi"

# name_class_page = "font-semibold block"
url="https://doisongphapluat.com.vn/tin-tuc-1.html"
name_class_page="title-1 b240 mb10 zone-theme-2 font18"

# Gửi yêu cầu đến trang web
r = requests.get(url)
xuly = BeautifulSoup(r.text, 'html.parser')

# Tìm tất cả các thẻ <h3> với class 'box-title-text'
data = xuly.find_all('h3', {'class': name_class_page})

# Khởi tạo danh sách để lưu trữ dữ liệu
link_data = []

# Đọc dữ liệu đã có trong file CSV (nếu có)
existing_data = set()
csv_file = 'dataChung/Urls1.csv'

try:
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            existing_data.add((row['title'], row['link']))
except FileNotFoundError:
    # Nếu file chưa tồn tại, chúng ta sẽ tạo file mới
    pass

# Duyệt qua các thẻ tìm thấy và lấy title, link từ thẻ <a> bên trong
for i in data:
    link = i.a  # Lấy thẻ <a> bên trong thẻ <h3>
    if link and link.get('href'):
        title = link.get('title', link.text.strip())  # Lấy title hoặc text của thẻ <a>
        href = urljoin(url, link.get('href'))  # Kết hợp link tương đối với URL
        
        # Kiểm tra nếu title và link chưa có trong dữ liệu đã tồn tại
        if (title, href) not in existing_data:
            link_data.append({'title': title, 'link': href, 'Processed': '0'})
            existing_data.add((title, href))  # Thêm vào tập dữ liệu đã có

# Ghi dữ liệu mới vào CSV nếu có dữ liệu mới
if link_data:
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['title', 'link', 'Processed']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Nếu file mới thì ghi header
        if file.tell() == 0:
            writer.writeheader()

        # Ghi từng dòng dữ liệu mới vào file
        for row in link_data:
            writer.writerow(row)

    print(f"Dữ liệu mới đã được ghi vào file {csv_file}")
else:
    print("Không có dữ liệu mới để thêm vào.")
