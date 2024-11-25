from gensim.models import Word2Vec
import string
from pyvi import ViTokenizer
from nltk.corpus import stopwords
import numpy as np

# # Tải stopwords từ NLTK nếu chưa tải
# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')

import random

# Các chủ đề và cụm từ để tạo câu tiếng Việt
subjects = [
    "Đội ngũ bảo mật", "Quản trị viên hệ thống", "Chuyên gia bảo mật", "Phần mềm", "Mạng máy tính", 
    "Tường lửa", "Hệ thống phát hiện xâm nhập", "Dữ liệu nhạy cảm", "Quản lý rủi ro", "Bảo vệ quyền riêng tư"
]

verbs = [
    "giám sát", "quản lý", "phát hiện", "mã hóa", "sao lưu", "vá lỗi", "tăng cường", "bảo vệ", "ngăn chặn", 
    "đảm bảo", "phân tích", "đánh giá", "đề phòng", "phát triển", "triển khai"
]

objects = [
    "lưu lượng mạng", "lỗ hổng bảo mật", "mạng nội bộ", "dữ liệu nhạy cảm", "quyền riêng tư", "hệ thống bảo mật", 
    "nguy cơ tấn công mạng", "tấn công DoS", "xâm nhập trái phép", "tấn công mạng", "mối đe dọa bảo mật", 
    "thông tin bảo mật", "hệ thống dữ liệu", "mã độc", "tấn công phishing"
]

adjectives = [
    "định kỳ", "nâng cao", "quan trọng", "cần thiết", "mạnh mẽ", "an toàn", "tối ưu", "hiệu quả", "từ xa", "mới"
]

# Hàm tạo câu ngẫu nhiên
def generate_sentence():
    subject = random.choice(subjects)
    verb = random.choice(verbs)
    obj = random.choice(objects)
    adjective = random.choice(adjectives)
    
    # Tạo câu hoàn chỉnh
    return f"{subject} {verb} {adjective} {obj}."

# Tạo 200 câu ngẫu nhiên
documents = [generate_sentence() for _ in range(200)]

def tokenizerVN(text):
    return ViTokenizer.tokenize(text)

# Định nghĩa tokenize
def tokenize(sentence):
    # Tokenize và loại bỏ dấu câu
    tokens = tokenizerVN(sentence).split()
    tokens = [word for word in tokens if word not in string.punctuation]  # Loại bỏ dấu câu
    return tokens

# Danh sách stopwords tiếng Việt
stopwords_vi = set([
    'a', 'ai', 'bao', 'bao_nhiêu', 'cái', 'có', 'cũng', 'để', 'đi', 'gì', 'hôm', 'không', 'là', 'làm', 'một', 'nào', 'người', 'như', 'nói', 'này', 'nên', 'thì', 'tôi', 'và', 'vậy'
    # Bạn có thể thêm nhiều stopwords khác vào danh sách này
])

# Hàm tiền xử lý văn bản: tokenization và loại bỏ stopwords
def preprocess(sentences):
    wordList = []
    for sentence in sentences:
        words = tokenize(sentence)
        filtered_words = [word for word in words if word not in stopwords_vi]
        wordList.append(filtered_words)  # Loại bỏ stopwords và ký tự không phải chữ
    return wordList
processed_documents = preprocess(documents)
model = Word2Vec(
    sentences=processed_documents,  # Cung cấp tài liệu đã được token hóa
    vector_size=100,                # Kích thước vector
    window=5,                       # Kích thước cửa sổ ngữ cảnh
    min_count=1,                    # Bỏ qua từ xuất hiện ít hơn 1 lần
    workers=4,                      # Số luồng
    sg=0,                           # Skip-gram (sg=1) hoặc CBOW (sg=0)
    epochs=20                       # Số lần huấn luyện
)

# Tìm từ ít liên quan nhất với một từ cụ thể (ví dụ: "bảo mật")
word_to_check = 'bảo_mật'

# Kiểm tra nếu từ có trong từ điển
if word_to_check in model.wv:
    # Lấy danh sách tất cả các từ trong mô hình
    all_words = list(model.wv.index_to_key)
    
    # Tính cosine similarity giữa từ 'word_to_check' và tất cả các từ khác trong từ điển
    similarity_scores = []
    for word in all_words:
        similarity = model.wv.similarity(word_to_check, word)
        similarity_scores.append((word, similarity))
    
    # Sắp xếp các từ theo độ tương quan tăng dần và lấy từ có độ tương quan thấp nhất
    least_related_word = min(similarity_scores, key=lambda x: x[1])
    print(f"Từ ít liên quan nhất với '{word_to_check}' là '{least_related_word[0]}' với độ tương quan {least_related_word[1]}")
else:
    print(f"Từ '{word_to_check}' không có trong từ điển.")
# Biểu diễn câu bằng trung bình vector
def sentence_vector(sentence, model):
    tokens = preprocess(sentence)
    vectors = [model.wv[word] for word in tokens if word in model.wv]
    if vectors:
        return np.mean(vectors, axis=0)
    else:
        return np.zeros(model.vector_size)
    
similar_words = model.wv.most_similar(word_to_check, topn=5)

# In kết quả
print(f"5 từ có độ liên quan nhiều nhất với '{word_to_check}':")
for word, similarity in similar_words:
    print(f"{word}: {similarity}")


