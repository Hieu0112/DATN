import pandas as pd
import re
import warnings
from sklearn.model_selection import train_test_split
from underthesea import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
import warnings
warnings.filterwarnings("ignore")

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

# Áp dụng tiền xử lý cho stop words và token hóa chúng
stopWords = [wordopt(word) for word in stopWords if len(word.strip()) > 0]

# Tokenize stop words
tokenized_stopwords = []
for word in stopWords:
    tokenized_stopwords.extend(tokenize(word))

# Sử dụng CountVectorizer với stop words đã token hóa và tokenizer
vectorizer = CountVectorizer(
    stop_words=tokenized_stopwords,
    tokenizer=tokenize,
    token_pattern=None  # Bỏ qua token_pattern
)

# Chia tập dữ liệu
X = data_df["text"]
y = data_df["label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=30)

# Áp dụng Vectorizer
Xv_train = vectorizer.fit_transform(X_train)
Xv_test = vectorizer.transform(X_test)
