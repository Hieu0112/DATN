from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import csv
import time
from urllib.parse import urljoin

# Tên file CSV
csv_file = 'Urls.csv'

# Đọc dữ liệu đã có trong file CSV (nếu có)
existing_data = set()

try:
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            existing_data.add((row['title'], row['link']))
except FileNotFoundError:
    # Nếu file chưa tồn tại, chúng ta sẽ tạo file mới
    pass

urls_page = [
    # {"url": "https://viettan.org/thoi-su/page/{page}/", "name_class_page": "elementor-post__title","data-item":"h3"},
    # {"url": "https://viettan.org/quan-diem/page/{page}/", "name_class_page": "elementor-post__title","data-item":"h3"},

    # {"url": "https://thoibao.de/blog/category/chinh-tri/page/{page}", "name_class_page": "entry-title","data-item":"h2"},
    # {"url": "https://thoibao.de/blog/category/xa-hoi/page/{page}", "name_class_page": "entry-title","data-item":"h2"},
    # {"url": "https://thoibao.de/blog/category/phap-luat-doi-song/page/{page}", "name_class_page": "entry-title","data-item":"h2"},

    {"url": "https://www.bbc.com/vietnamese/topics/ckdxnx1x5rnt?page={page}", "name_class_page": "bbc-110w6ng e47bds20","data-item":"h2"},

]
urls=[]
# Vòng lặp qua mảng urls
for item in urls_page:
    if "{page}" in item["url"]:
        # Thay {page} từ 1 đến 10 nếu có
        for x in range(0, 50):
            url = item["url"].replace("{page}", str(x))
            urls.append({"url": url, "name_class_page": item["name_class_page"]})
    else:
        # Giữ nguyên nếu không có {page}
        urls.append(item)

print(len(urls))

# set_up_web="https://viettan.org/"
# set_up_web="https://thoibao.de/blog/category/chinh-tri"
set_up_web="https://www.bbc.com/vietnamese/topics/ckdxnx1x5rnt?page=1"


# Cấu hình ChromeOptions
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Chạy Chrome ở chế độ không hiển thị (không bắt buộc)
chrome_options.add_argument("--ignore-certificate-errors")  # Bỏ qua lỗi SSL

# Khởi tạo trình điều khiển (ChromeDriver)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Dừng chương trình cho đến khi bạn hoàn thành việc giải reCAPTCHA
driver.get(set_up_web)

input("Vui lòng giải reCAPTCHA và nhấn Enter để tiếp tục...")

# Đọc dữ liệu đã có trong file CSV (nếu có)
existing_data = set()
csv_file = 'Urls.csv'

try:
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            existing_data.add((row['title'], row['link']))
except FileNotFoundError:
    # Nếu file chưa tồn tại, chúng ta sẽ tạo file mới
    pass

for item in urls:
    url=item["url"]
    name_class_page=item["name_class_page"]
    # Gửi yêu cầu đến trang web
    driver.get(item["url"])
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    time.sleep(0.2)

    # Tìm tất cả các thẻ <hx> với class 'ax'
    data = soup.find_all(item.get("data-item"), {'class': name_class_page})

    # Khởi tạo danh sách để lưu trữ dữ liệu
    link_data = []

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

        print(f"Dữ liệu mới đã được ghi vào file {csv_file} từ trang "+ item["url"])
    else:
        print(f"Not data tu trang "+item["url"])


driver.quit()
