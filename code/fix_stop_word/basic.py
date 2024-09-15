import pandas as pd
import re
from sklearn.model_selection import train_test_split
from underthesea import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer

# Đọc dữ liệu và danh sách stop words
data_df = pd.read_csv("code/fix_stop_word/data_train.csv", encoding='utf-8')

with open('code/fix_stop_word/vietnamese-stopwords.txt', 'r', encoding='utf-8') as file:
    stopWords = file.read().split('\n')

# Hàm tiền xử lý văn bản
def wordopt(text):
    text = text.lower()
    text = re.sub('https?:\/\/.*[\r\n]*', ' ', text)
    text = re.sub('[^\w\s]', ' ', text)
    text = re.sub('\n', ' ', text)
    return text

# Tiền xử lý văn bản trong DataFrame
data_df["text"] = data_df["text"].apply(wordopt)

# Tokenizer sử dụng underthesea
def tokenize(sentence):
    return word_tokenize(sentence, format='word')

# Token hóa danh sách stop words
tokenized_stopwords = [tokenize(word) for word in stopWords]
# Chuyển danh sách stopword token hóa thành một list đơn lẻ
tokenized_stopwords_flat = [item for sublist in tokenized_stopwords for item in sublist]

# Sử dụng CountVectorizer với stop words đã token hóa và tokenizer
vectorizer = CountVectorizer(
    stop_words=tokenized_stopwords_flat,  # Áp dụng stopword đã token hóa
    tokenizer=tokenize,
    token_pattern=None  # Bỏ qua tham số token_pattern
)

X = data_df["text"]
y = data_df["label"]
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=30)

# Fit CountVectorizer
# Xv_train = vectorizer.fit_transform(X_train)
# Xv_test = vectorizer.transform(X_test)

# In ra danh sách stopword đã token hóa
print("Danh sách stopwords đã token hóa:")
print(tokenized_stopwords_flat)
