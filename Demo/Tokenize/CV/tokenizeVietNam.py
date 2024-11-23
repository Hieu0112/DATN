import string
from pyvi import ViTokenizer
from sklearn.feature_extraction.text import CountVectorizer

# Stopwords ví dụ
stopwords = ['ai_ai', 'ai_nấy', 'ai_đó', 'bao_lâu', 'bao_nhiêu', 'biết', 'biết_bao', 'biết_chắc']

# Định nghĩa tokenizerVN
def tokenizerVN(text):
    return ViTokenizer.tokenize(text)

# Định nghĩa tokenize
def tokenize(sentence):
    # Tokenize và loại bỏ dấu câu
    tokens = tokenizerVN(sentence).split()
    tokens = [word for word in tokens if word not in string.punctuation]  # Loại bỏ dấu câu
    return tokens

# Tạo CountVectorizer
vectorizerCV = CountVectorizer(
    stop_words=stopwords,
    tokenizer=tokenize,
)

# Dữ liệu mẫu
data = ["Hà Nội là thủ đô của Việt Nam, nơi có lịch sử nghìn năm văn hiến."]
vectorized = vectorizerCV.fit_transform(data)

# Kết quả
print("Từ vựng:", vectorizerCV.get_feature_names_out())
