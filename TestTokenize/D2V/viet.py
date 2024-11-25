from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import numpy as np
import random
from pyvi import ViTokenizer

# Các chủ đề và cụm từ để tạo câu tiếng Việt
chude = [
    "Đội ngũ bảo mật", "Quản trị viên hệ thống", "Chuyên gia bảo mật", "Phần mềm", "Mạng máy tính",
    "Tường lửa", "Hệ thống phát hiện xâm nhập", "Dữ liệu nhạy cảm", "Quản lý rủi ro", "Bảo vệ quyền riêng tư"
]

dongtu = [
    "giám sát", "quản lý", "phát hiện", "mã hóa", "sao lưu", "vá lỗi", "tăng cường", "bảo vệ", "ngăn chặn",
    "đảm bảo", "phân tích", "đánh giá", "đề phòng", "phát triển", "triển khai"
]

doituong = [
    "lưu lượng mạng", "lỗ hổng bảo mật", "mạng nội bộ", "dữ liệu nhạy cảm", "quyền riêng tư", "hệ thống bảo mật",
    "nguy cơ tấn công mạng", "tấn công DoS", "xâm nhập trái phép", "tấn công mạng", "mối đe dọa bảo mật",
    "thông tin bảo mật", "hệ thống dữ liệu", "mã độc", "tấn công phishing"
]

tinhchat = [
    "định kỳ", "nâng cao", "quan trọng", "cần thiết", "mạnh mẽ", "an toàn", "tối ưu", "hiệu quả", "từ xa", "mới"
]

# Hàm tạo câu ngẫu nhiên
def tao_cau():
    chu_de = random.choice(chude)
    dong_tu = random.choice(dongtu)
    doi_tuong = random.choice(doituong)
    tinh_chat = random.choice(tinhchat)
    return f"{chu_de} {dong_tu} {tinh_chat} {doi_tuong}."

# Tạo 200 câu ngẫu nhiên
van_ban = [tao_cau() for _ in range(200)]
print(van_ban)

def tokenizerVN(text):
    return ViTokenizer.tokenize(text)

# Định nghĩa tokenize
def tokenize(sentence):
    # Tokenize và loại bỏ dấu câu
    tokens = tokenizerVN(sentence).split()
    return tokens

# Hàm tiền xử lý: Tokenize và loại bỏ stopwords
stopwords_vi = set([
    'a', 'ai', 'bao', 'bao_nhiêu', 'cái', 'có', 'cũng', 'để', 'đi', 'gì', 'hôm', 'không', 'là', 'làm', 'một', 
    'nào', 'người', 'như', 'nói', 'này', 'nên', 'thì', 'tôi', 'và', 'vậy'
])

def preprocess(doc):
    tokens = tokenize(doc)
    return [word for word in tokens if word not in stopwords_vi]

# Tiền xử lý văn bản
van_ban_tagged = [TaggedDocument(preprocess(doc), [i]) for i, doc in enumerate(van_ban)]

print(van_ban_tagged[10])

# Huấn luyện mô hình Doc2Vec
model = Doc2Vec(
    vector_size=100,       # Kích thước vector
    window=5,              # Kích thước cửa sổ ngữ cảnh
    min_count=1,           # Bỏ qua từ xuất hiện ít hơn min_count
    workers=4,             # Số luồng để huấn luyện
    epochs=20              # Số lần lặp để huấn luyện
)

model.build_vocab(van_ban_tagged)
model.train(van_ban_tagged, total_examples=model.corpus_count, epochs=model.epochs)

# Tìm 5 câu có độ tương quan cao nhất với một câu cụ thể
cau_mau = van_ban[2]  # Lấy câu thứ 3 làm ví dụ
print(f"Câu mẫu: {cau_mau}")
vector_cau_mau = model.infer_vector(preprocess(cau_mau))

# Tính toán độ tương quan giữa câu mẫu và các câu khác
diem_tuong_quan = []
for i, van_ban in enumerate(van_ban_tagged):
    vector_cau_khac = model.infer_vector(van_ban.words)
    tuong_quan = np.dot(vector_cau_mau, vector_cau_khac) / (np.linalg.norm(vector_cau_mau) * np.linalg.norm(vector_cau_khac))
    diem_tuong_quan.append((i, tuong_quan))

# Sắp xếp và lấy 5 câu liên quan nhất
cau_lien_quan = sorted(diem_tuong_quan, key=lambda x: x[1], reverse=True)[:5]

# Sửa dòng in kết quả
print("5 câu liên quan nhất:")
for index, diem in cau_lien_quan:
    print(f"Câu {index}: {' '.join(van_ban_tagged[index].words)} - Độ tương quan: {diem}")

