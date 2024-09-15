import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

# Đọc dữ liệu từ tệp Links.csv
links_df = pd.read_csv('dataReal/testAu.csv')

def get_authors_from_url(url):
    try:
        # Gửi yêu cầu HTTP để lấy nội dung trang
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Tìm tất cả các thẻ <p> trên trang
        all_paragraphs = soup.find_all('p')

        # Chọn các thẻ <p> từ vị trí thứ 5 từ dưới lên
        if len(all_paragraphs) > 2:
            paragraphs_to_check = all_paragraphs[-2:]  # 5 thẻ cuối cùng
        else:
            paragraphs_to_check = all_paragraphs  # Nếu ít hơn 5 thẻ, lấy tất cả

        authors = []
        for p in paragraphs_to_check:
            if p.find('strong'):
                text = p.get_text(strip=True)
                if len(text) > 0:
                    # Xóa ký tự \n và thay thế \t bằng dấu cách
                    author_content = text.replace('\n', ' ').replace('\t', ' ')
                    authors.append(author_content)

        return authors
    except Exception as e:
        print(f"Error fetching authors from {url}: {e}")
        return []

# Tạo danh sách lưu kết quả
results = []

# Xử lý từng liên kết trong DataFrame
for index, row in links_df.iterrows():
    url = row['link']
    authors = get_authors_from_url(url)
    result = {
        'title': row['title'],
        'link': url,
        'Processed': row['Processed'],
        'authors': ', '.join(authors)
    }
    results.append(result)

# Tạo DataFrame từ danh sách kết quả
results_df = pd.DataFrame(results)

# Tên tệp CSV đầu ra
output_csv_file = 'dataReal/Authors_Output.csv'

# Kiểm tra xem tệp CSV đã tồn tại chưa
if not os.path.isfile(output_csv_file):
    print(f"Tệp '{output_csv_file}' chưa tồn tại. Đang tạo mới.")

# Ghi kết quả vào tệp CSV
results_df.to_csv(output_csv_file, index=False)

print("Hoàn tất việc trích xuất tên tác giả và lưu vào tệp CSV.")
