from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import time
import re
from urllib.parse import urlparse

# Cấu hình ChromeOptions
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")  # Bỏ qua lỗi SSL

# Khởi tạo trình điều khiển (ChromeDriver)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

set_up_web="https://thoibao.de/blog/category/chinh-tri"
# set_up_web="https://viettan.org/tai-sao-csvn-e-ngai-viet-tan/"

# Mở một trang chứa reCAPTCHA để người dùng tự giải
driver.get(set_up_web)
input("Vui lòng giải reCAPTCHA và nhấn Enter để tiếp tục...")  # Dừng lại cho đến khi reCAPTCHA được giải

# Hàm làm sạch văn bản
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Loại bỏ khoảng trắng thừa
    return text.strip() + " "

# Hàm xử lý từng URL
def process_url(url):
    try:
        driver.get(url)
        time.sleep(1)  # Đợi trang tải
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        title_text = "N/A"
        text_content = "N/A"
        author = "N/A"
        all_content = []

        if "thoibao.de" in domain:
            article = soup.find('article')
            if article:
                # Lấy Title từ thẻ <h1>
                title = article.find('h1').get_text()
                title_text = title.strip().replace('\n', ' ').replace('\t', ' ') if title else "N/A"
                # Duyệt qua tất cả các thẻ <p> trong <article>
                for p in article.find_all('p'):
                    # Kiểm tra nếu thẻ <p> có <strong> thì là tác giả (Author)
                    if p.find('strong'):
                        author = p.get_text().strip().replace('\n', ' ').replace('\t', ' ')
                    else:
                        # Nếu không có <strong> thì lấy nội dung làm Text
                        all_content.append(clean_text(p.get_text()))
                full_content = ' '.join(all_content)
                text_content = clean_text(full_content)
        elif "bbc.com" in domain:
            main_content = soup.find('main', class_='bbc-fa0wmp')

            # Kiểm tra xem thẻ <main> có tồn tại
            if main_content:
                # Lấy tiêu đề từ thẻ <h1>
                title = main_content.find('h1').get_text()
                title_text = title.strip().replace('\n', ' ').replace('\t', ' ') if title else "N/A"
                for p in main_content.find_all('p'):
                    all_content.append(clean_text(p.get_text()))
                
                full_content = ' '.join(all_content)
                text_content = clean_text(full_content)
                
                author_span = main_content.find('span', class_='bbc-18ttg5u')
    
                # Kiểm tra nếu thẻ <span> chứa tác giả tồn tại
                if author_span:
                    author = author_span.get_text().strip().replace('\n', ' ').replace('\t', ' ')
        else:
            # Lấy tiêu đề (thẻ h1)
            title = soup.find('h1', class_='elementor-heading-title elementor-size-default')
            title_text = title.text.strip().replace('\n', ' ').replace('\t', ' ') if title else "N/A"
            # Lấy nội dung các thẻ <p> và tiêu đề <h>
            content_block = soup.find('div', attrs={'class': ['elementor-widget-theme-post-content']})
            if content_block:
                for element in content_block.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
                    all_content.append(clean_text(element.get_text()))
                full_content = ' '.join(all_content)
                text_content = clean_text(full_content)
            else:
                text_content = "N/A"
            # Lấy thông tin tác giả
            author_info = soup.find('span', class_='elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-author')
            author = author_info.text.strip() if author_info else "N/A"
        


        # Trả về dữ liệu đã lấy
        return {
            'title': title_text,
            'text': text_content.replace('\n', ' '),
            'author': author,
            'source_domain': domain
        }
    except Exception as e:
        print(f'Yêu cầu thất bại với URL {url}. Lỗi: {e}')
        return None

# Đường dẫn đến file chứa URL và file lưu dữ liệu đã xử lý
urls_file = 'Urls.csv'
fake_file = 'dataset_fake.csv'

# Đọc URL từ file CSV và ghi dữ liệu đã xử lý
with open(urls_file, mode='r', newline='', encoding='utf-8') as url_file:
    reader = csv.DictReader(url_file)
    rows = list(reader)  # Đọc tất cả các dòng vào danh sách
maxs_rows = min(500,len(rows))
i=1
# Lặp qua từng URL trong file CSV
for row in rows:
    if i <= maxs_rows:
        url = row['link']  # Giả sử file CSV có cột 'link' chứa các URL
        processed = row.get('Processed', '0')  # Kiểm tra xem URL đã được xử lý chưa

        if processed == '0':  # Chỉ xử lý các URL chưa được xử lý
            print(f"Đang xử lý: {url}")
            i+=1
            # Xử lý từng URL
            article_data = process_url(url)
            
            if article_data:
                # Ghi dữ liệu vào file CSV
                with open(fake_file, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=['title', 'text', 'author', 'source_domain']) 
                    
                    # Nếu file trống, ghi tiêu đề vào
                    if file.tell() == 0:
                        writer.writeheader()
                    
                    # Ghi dữ liệu bài báo nếu 'text' không rỗng
                    if article_data['text'].strip():
                        writer.writerow(article_data)
                    else:
                        print(f"Không có nội dung hợp lệ tại {url}")

                # Sau khi xử lý xong, đánh dấu 'Processed' là 1
                row['Processed'] = '1'

            time.sleep(0.3)  # Đợi một chút giữa các yêu cầu

# Ghi lại file CSV với cột 'Processed' đã được cập nhật
with open(urls_file, mode='w', newline='', encoding='utf-8') as url_file:
    writer = csv.DictWriter(url_file, fieldnames=reader.fieldnames)
    writer.writeheader()  # Ghi tiêu đề
    writer.writerows(rows)  # Ghi lại toàn bộ các hàng, bao gồm cả cột 'Processed' đã cập nhật

print(f"Dữ liệu đã được lưu vào {fake_file}")
driver.quit()
