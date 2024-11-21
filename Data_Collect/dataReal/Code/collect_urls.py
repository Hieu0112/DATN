import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import time

# URL của trang cần thu thập dữ liệu

# Tạo mảng urls với mỗi phần tử là một dictionary chứa url và author
urls_page = [

    {"url": "https://www.sggp.org.vn/chinhtri/", "name_class_page": "story__heading","data-item":"h2"},
    {"url": "https://www.sggp.org.vn/xahoi/", "name_class_page": "story__heading","data-item":"h2"},

    # {"url": "https://vnexpress.net/thoi-su-p{page}", "name_class_page": "title-news","data-item":"h3"},
    # {"url": "https://vnexpress.net/phap-luat-p{page}", "name_class_page": "title-news","data-item":"h3"},


    # {"url": "https://vnexpress.net/thoi-su-p{page}", "name_class_page": "title-news","data-item":"h3"},
    # {"url": "https://vnexpress.net/phap-luat-p{page}", "name_class_page": "title-news","data-item":"h3"},

    # {"url": "https://dantri.com.vn/phap-luat/trang-{page}.htm", "name_class_page": "article-title","data-item":"h3"},
    # {"url": "https://dantri.com.vn/xa-hoi/chinh-tri/trang-{page}.htm", "name_class_page": "title-news","data-item":"h3"},

    {"url": "https://nhandan.vn/chinhtri/", "name_class_page": "story__heading","data-item":"h3"},
    {"url": "https://nhandan.vn/xay-dung-dang/", "name_class_page": "story__heading","data-item":"h3"},
    {"url": "https://nhandan.vn/xa-luan/", "name_class_page": "story__heading","data-item":"h3"},
    {"url": "https://nhandan.vn/phapluat/", "name_class_page": "story__heading","data-item":"h3"},

    # {"url": "https://tuoitre.vn/thoi-su/trang-{page}.htm", "name_class_page": "box-title-text","data-item":"h3"},
    # {"url": "https://tuoitre.vn/phap-luat/trang-{page}.htm", "name_class_page": "box-title-text","data-item":"h3"},

    # {"url": "https://vietnamnet.vn/thoi-su-page{page}", "name_class_page": "vnn-title","data-item":"h3"},
    # {"url": "https://vietnamnet.vn/chinh-tri-page{page}", "name_class_page": "vnn-title","data-item":"h3"},

    {"url": "https://thanhnien.vn/thoi-su.htm", "name_class_page": "box-title-text","data-item":"h3"},
    {"url": "https://thanhnien.vn/thoi-su/chinh-tri.htm", "name_class_page": "box-title-text","data-item":"h3"},

    {"url": "https://baomoi.com/an-ninh-trat-tu.epi", "name_class_page": "font-semibold block","data-item":"h3"},
    {"url": "https://baomoi.com/thoi-su.epi", "name_class_page": "font-semibold block","data-item":"h3"},
    {"url": "https://baomoi.com/xa-hoi.epi", "name_class_page": "font-semibold block","data-item":"h3"},
    

    # {"url": "https://doisongphapluat.com.vn/tin-tuc-1/trang-{page}.html", "name_class_page": "title-1 b240 mb10 zone-theme-2 font18","data-item":"h3"},
    # {"url": "https://doisongphapluat.com.vn/phap-luat-3/trang-{page}.html", "name_class_page": "title-1 b240 mb10 zone-theme-2 font18","data-item":"h3"},
]
urls=[]
# Vòng lặp qua mảng urls
for item in urls_page:
    if "{page}" in item["url"]:
        # Thay {page} từ 1 đến 10 nếu có
        for x in range(0, 40):
            url = item["url"].replace("{page}", str(x))
            urls.append({"url": url, "name_class_page": item["name_class_page"]})
    else:
        # Giữ nguyên nếu không có {page}
        urls.append(item)

print(len(urls))

for item in urls:
    url=item["url"]
    name_class_page=item["name_class_page"]
    # Gửi yêu cầu đến trang web
    r = requests.get(url)
    time.sleep(0.2)
    xuly = BeautifulSoup(r.text, 'html.parser')

    # Tìm tất cả các thẻ <hx> với class 'ax'
    data = xuly.find_all(item.get("data-item"), {'class': name_class_page})

    # Khởi tạo danh sách để lưu trữ dữ liệu
    link_data = []

    # Đọc dữ liệu đã có trong file CSV (nếu có)
    existing_data = set()
    csv_file = 'Data_Collect/dataReal/Urls.csv'

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

        print(f"Dữ liệu mới đã được ghi vào file {csv_file} từ trang "+ item["url"])
    else:
        print(f"Not data tu trang " + item["url"])
