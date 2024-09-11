import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse
# import re


def extract_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

# def format_date(date_str):
#     # Biểu thức chính quy để tìm ngày, tháng, năm
#     match = re.search(r'(\d{1,2})[^\d](\d{1,2})[^\d](\d{4})', date_str)
#     if match:
#         day, month, year = match.groups()
#         return f"{day}-{month}-{year}"
#     return 'Unknown'

def scrape_article(url):
    # Gửi yêu cầu đến trang web
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Lấy tiêu đề và ngày từ các thẻ khác ngoài <article>
    title = soup.find('h1', class_='title-detail').text.strip() if soup.find('h1', class_='title-detail') else 'Unknown'
    date_str = soup.find('span', class_='date').text.strip() if soup.find('span', class_='date') else 'Unknown'
    # date = format_date(date_str)
    
    # Tìm thẻ <article>
    article = soup.find('article')
    if not article:
        return {
            'title': title,
            'text': 'Unknown',
            # 'date': date,
            'author': 'Unknown',
            'source_domain': extract_domain(url)
        }
    
    # Lấy nội dung từ tất cả các thẻ <p> trừ thẻ <p> cuối cùng
    paragraphs = article.find_all('p')
    text = ' '.join([p.text for p in paragraphs[:-1]]).strip() if paragraphs else 'Unknown'
    
    # Lấy tác giả từ thẻ <p> cuối cùng nếu có thẻ <strong>
    author_p = paragraphs[-1] if paragraphs else None
    author = 'Unknown'
    if author_p and author_p.find('strong'):
        author = author_p.find('strong').text.strip()
    
    domain = extract_domain(url)

    return {
        'title': title,
        'text': text.replace('\n', '.'),
        # 'date': date,
        'author': author,
        'source_domain': domain
    }

urls_file = 'data/urls.csv'
real_file = 'data/real.csv'

# Đọc dữ liệu từ urls_file và chỉ xử lý các dòng có 'Processed' bằng 0
data = []
with open(urls_file, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['Processed'] == '0':  # Chỉ xử lý khi 'Processed' là 0
            article_data = scrape_article(row['link'])  # Gọi hàm để xử lý bài báo
            
            # Ghi dữ liệu vào file real.csv
            with open(real_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['title', 'text', 'date', 'author', 'source_domain'])
                
                # Nếu file trống thì ghi tiêu đề vào
                if file.tell() == 0:
                    writer.writeheader()
                
                # Ghi dữ liệu bài báo
                writer.writerow(article_data)
            
            # Sau khi xử lý xong, đánh dấu 'Processed' là 1
            row['Processed'] = '1'
        data.append(row)  # Lưu lại dữ liệu




with open(urls_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['title', 'link', 'Processed'])
    
    if file.tell() == 0:
        writer.writeheader()
    
    # Ghi các dòng dữ liệu đã được cập nhật
    writer.writerows(data)

print("Dữ liệu đã được xử lý và cập nhật.")