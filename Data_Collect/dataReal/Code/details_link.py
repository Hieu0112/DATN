import csv
import os
import time
import re
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

# Đường dẫn tới tệp CSV chứa URL
urls_file = 'Data_Collect/dataReal/Urls_Real/Urls.csv'
real_file = 'Data_Collect/dataReal/Details_Real/dataset_real.csv'

def clean_text(text):
    # Thay thế các ký tự xuống dòng và nhiều dấu cách bằng một dấu cách
    text = re.sub(r'\s+', ' ', text)
    return text.strip()+" "

def removeDate_author(text):
    # Định nghĩa mẫu cho định dạng ngày giờ
    pattern = r'\b\d{2}/\d{2}/\d{4} - \d{2}:\d{2}\b'
    
    # Kiểm tra nếu chuỗi chứa định dạng ngày giờ
    if re.search(pattern, text):
        return "N/A"
    else:
        return text

def process_url(url):
    try:
        print(f"Đang xử lý: {url}")
        # Gửi yêu cầu HTTP đến URL và lấy nội dung
        response = requests.get(url)
        # response = requests.get(url, timeout=30)  # Thời gian chờ tối đa là 30 giây
        response.raise_for_status()  # Kiểm tra trạng thái yêu cầu HTTP
        html_content = response.text
        # Phân tích nội dung HTML bằng BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        # Tìm thẻ <h1>
        h1_tag = soup.find('h1')

        # Trích xuất domain từ URL
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        # Tìm thẻ tác giả
        author_content = 'N/A'
            
        # Kiểm tra các thẻ <p> để tìm thông tin tác giả
        # Tìm thẻ có lớp chứa chữ 'author'
        author_paragraph = soup.find('p', class_=lambda x: x and 'author' in x)

        # Kiểm tra nếu thẻ author_paragraph không phải là None
        if author_paragraph:
            text = author_paragraph.get_text(strip=True)
            if len(text) > 0:
            # Xóa ký tự \n và thay thế \t bằng dấu cách
                author_content = text.replace('\n', ' ').replace('\t', ' ')

        # Nếu không tìm thấy trong thẻ <p>, kiểm tra thẻ có class chứa "author"
        if author_content == 'N/A':
            author_tag = soup.find(class_=lambda class_name: class_name and 'author' in class_name)
            if author_tag:
                a_tags = author_tag.find_all('a')
                for a_tag in a_tags:
                    if a_tag.get_text(strip=True):  # Kiểm tra nội dung không trống
                        author_content = a_tag.get_text(strip=True)
                        break

        if author_content == 'N/A':
            all_paragraphs = soup.find_all('p')

            # Chọn các thẻ <p> từ vị trí thứ 5 từ dưới lên
            if len(all_paragraphs) > 2:
                paragraphs_to_check = all_paragraphs[-2:]  # 5 thẻ cuối cùng
            else:
                paragraphs_to_check = all_paragraphs  # Nếu ít hơn 5 thẻ, lấy tất cả
            for p in paragraphs_to_check:
                if p.find('strong'):
                    text = p.get_text(strip=True)
                    if len(text) > 0:
                        # Xóa ký tự \n và thay thế \t bằng dấu cách
                        author_content = text.replace('\n', ' ').replace('\t', ' ')
        if author_content == 'N/A':
            author_paragraph = soup.find('div', class_=lambda x: x and 'author' in x)
            # Kiểm tra nếu thẻ author_paragraph không phải là None
            if author_paragraph:
                text = author_paragraph.get_text(strip=True)
                if len(text) > 0:
                # Xóa ký tự \n và thay thế \t bằng dấu cách
                    author_content = text.replace('\n', ' ').replace('\t', ' ')  
        if h1_tag:
            # Lấy nội dung của thẻ <h1>
            h1_text = h1_tag.get_text().strip()

            # Tìm thẻ cha của thẻ <h1>
            parent_tag = h1_tag.find_parent()

            if parent_tag:
                # Tìm tất cả các thẻ <p> bên trong thẻ cha, ngoại trừ các thẻ nằm trong thẻ author
                p_tags = parent_tag.find_all('p')
                p_texts = []
                for p_tag in p_tags:
                    # Kiểm tra nếu thẻ <p> không nằm trong thẻ có class chứa từ "author"
                    parent_author_tag = p_tag.find_parent(class_=lambda class_name: class_name and 'author' in class_name)
                    if not parent_author_tag:  # Nếu không tìm thấy thẻ cha với class chứa "author"
                        p_content = clean_text(p_tag.get_text().strip())
                        p_texts.append(p_content)

                # Nối nội dung các thẻ <p> bằng dấu chấm
                p_content = '. '.join(p_texts)
                #  đời sống pháp luật
                if len(p_content)==0:
                    p_tags = soup.find_all('p')
                    for p_tag in p_tags:
                        # Kiểm tra nếu thẻ <p> không có class chứa từ "author"
                        if not p_tag.has_attr('class') or not any('author' in class_name for class_name in p_tag['class']):
                            # Lấy và xử lý nội dung của thẻ <p>
                            p_content = clean_text(p_tag.get_text().strip())
                            p_texts.append(p_content)
                            doisongphapluat_web = 'uppercase bold color-blue-1'
                            tag = soup.find(class_=doisongphapluat_web)
                            if tag:
                                author_content = tag.get_text(strip=True)
                    # Sau khi lặp qua tất cả các thẻ <p>, nối nội dung các thẻ thành một chuỗi
                    p_content = '. '.join(p_texts)

            return{
                'title': h1_text,
                'text': p_content.replace('\n', ' '),
                'author': removeDate_author(author_content),
                'source_domain': domain
            }
    except requests.exceptions.Timeout:
        print(f"Request to {url} timed out.")
    except requests.RequestException as e:
        print(f'Yêu cầu thất bại với URL {url}. Lỗi: {e}')
        return None


# Kiểm tra sự tồn tại của tệp CSV
data = []
i=1
with open(urls_file, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    rows = list(reader)
    maxs_rows=min(1500,len(rows))
    for row in rows:
        if i<= maxs_rows:
            if row['Processed'] == '0':  # Chỉ xử lý khi 'Processed' là 0
                article_data = process_url(row['link'])  # Gọi hàm để xử lý bài báo
                i+=1
                # Ghi dữ liệu vào file real.csv
                if article_data:
                    with open(real_file, mode='a', newline='', encoding='utf-8') as file:
                        writer = csv.DictWriter(file, fieldnames=['title', 'text', 'author', 'source_domain'])
                    
                        # Nếu file trống thì ghi tiêu đề vào
                        if file.tell() == 0:
                            writer.writeheader()
                    
                        # Ghi dữ liệu bài báo
                        if article_data['text'].strip():  # Kiểm tra nếu 'text' không rỗng
                            # Ghi dữ liệu bài báo
                            writer.writerow(article_data)
                            # Sau khi xử lý xong, đánh dấu 'Processed' là 1
                            row['Processed'] = '1'
                            print("Dữ liệu số: "+str(i))
                    time.sleep(0.3)
                else:
                    print('x'+str(i))
        data.append(row)  # Lưu lại dữ liệu

with open(urls_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['title', 'link', 'Processed'])
    
    if file.tell() == 0:
        writer.writeheader()
    
    # Ghi các dòng dữ liệu đã được cập nhật
    writer.writerows(data)

print("Dữ liệu đã được xử lý và cập nhật.")
