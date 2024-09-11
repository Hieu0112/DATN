import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# URL của trang cần thu thập dữ liệu
url = ""  # Bạn cần điền URL vào đây

# Hàm trích xuất dữ liệu từ các thẻ <article>
def extract_links_and_titles(url):
    # Gửi yêu cầu đến trang web
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Tìm tất cả các thẻ <article>
    articles = soup.find_all('article')
    
    data = []
    domain = url.split('/')[2]  # Lấy domain từ URL
    
    for article in articles:
        # Lấy thẻ <a> đầu tiên trong thẻ <article>
        link = article.find('a')
        if link and link.get('href'):
            href = urljoin(url, link.get('href'))
            title = link.get('title', link.text.strip())  # Lấy tiêu đề từ thuộc tính title hoặc nội dung thẻ
            
            # Lấy tác giả
            author_tag = article.find('span', class_='elementor-post-author')
            author = author_tag.text.strip() if author_tag else "Unknown"
            
            # Lấy ngày đăng
            date_tag = article.find('span', class_='elementor-post-date')
            date = date_tag.text.strip() if date_tag else "Unknown"
            
            # Lấy mô tả (excerpt)
            excerpt_tag = article.find('div', class_='elementor-post__excerpt')
            description = excerpt_tag.text.strip() if excerpt_tag else "No description"
            
            # Thêm dữ liệu vào danh sách
            data.append({
                'title': title,
                'link': href,
                'author': author,
                'date': date,
                'domain': domain,
                'description': description,
                'Processed': '0'
            })
    
    return data

# Đọc dữ liệu đã có trong CSV
def read_existing_data(csv_file):
    existing_data = set()
    try:
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Lưu tiêu đề và liên kết vào một tập hợp
                existing_data.add((row['title'], row['link']))
    except FileNotFoundError:
        # Nếu file chưa tồn tại, tạo file mới
        pass
    
    return existing_data

# Kiểm tra và ghi dữ liệu vào CSV nếu chưa tồn tại
def write_new_data_to_csv(new_data, csv_file):
    existing_data = read_existing_data(csv_file)
    
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'link', 'author', 'date', 'domain', 'description', 'Processed'])
        
        # Nếu file trống thì ghi tiêu đề vào
        if file.tell() == 0:
            writer.writeheader()

        for row in new_data:
            # Chỉ thêm dữ liệu mới nếu chưa có trong CSV
            if (row['title'], row['link']) not in existing_data:
                writer.writerow(row)
                existing_data.add((row['title'], row['link']))

# Lấy dữ liệu tiêu đề và liên kết từ các thẻ <article>
data = extract_links_and_titles(url)

# Ghi dữ liệu vào file CSV nếu chưa tồn tại
csv_file = 'data/Fake1.csv'
write_new_data_to_csv(data, csv_file)

print("Dữ liệu mới đã được ghi vào file Fake1.csv")
