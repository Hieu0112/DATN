import string
from pyvi import ViTokenizer
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
# Stopwords ví dụ
stopwords = ['ai_ai', 'ai_nấy', 'ai_đó', 'bao_lâu', 'bao_nhiêu', 'biết', 'biết_bao', 'biết_chắc',]

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
data = ["Hà Nội là thủ đô của Việt Nam",
        "Hà Nội trong tim tôi",
        "Hà Nội Hà Nội ",
        "Hà nội lịch sử nghìn năm văn hiến."]
vectorized = vectorizerCV.fit_transform(data)

X_train = vectorizerCV.fit_transform(data)

# Set pandas options to display full data
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.width', None)  # Auto-detect width
pd.set_option('display.max_colwidth', None)  # Show full content of each column

# Convert to DataFrame to view the results
df = pd.DataFrame(X_train.toarray(), columns=vectorizerCV.get_feature_names_out())

# Print the DataFrame
print("Các câu")
for i in data:
    print(i)
# print("Từ vựng:", vectorizerCV.get_feature_names_out())


print(df)

# Kết quả

