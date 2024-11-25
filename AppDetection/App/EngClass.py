import joblib
import re
import pandas as pd
import warnings
import os
from nltk.tokenize import word_tokenize

warnings.filterwarnings("ignore")
from nltk.corpus import stopwords

warnings.filterwarnings("ignore")
stopwords = list(stopwords.words('english'))

def tokenize(sentence):
    return word_tokenize(sentence)

import string
def wordopt(text):

    update_text =""
    text = text.lower()
    text=re.sub("reuters"," ",text)
    
    #simplifying text
    text=re.sub(r"i'm","i am",text)
    text=re.sub(r"he's","he is",text)
    text=re.sub(r"she's","she is",text)
    text=re.sub(r"that's","that is",text)
    text=re.sub(r"what's","what is",text)
    text=re.sub(r"where's","where is",text)
    text=re.sub(r"\'ll"," will",text)
    text=re.sub(r"\'ve"," have",text)
    text=re.sub(r"\'re"," are",text)
    text=re.sub(r"\'d"," would",text)
    text=re.sub(r"won't","will not",text)
    text=re.sub(r"can't","cannot",text)
    
    # Loại bỏ các dấu câu đặc biệt
    text = re.sub('[%s]' % re.escape("""!–"#$%&'()*+,،-./:;<=>؟?@[\]^`{|}~“”…؛"""), ' ', text)
    # Loại bỏ các liên kết URL
    text = re.sub('https?://\S+|www\.\S+|https?:\/\/.*[\r\n]*', ' ', text)
    # Loại bỏ các thẻ HTML
    text = re.sub('<.*?>+', '', text)
    # Loại bỏ các chuỗi nằm trong dấu ngoặc vuông
    text = re.sub('\[.*?\]', '', text)
    # Loại bỏ ký tự không phải chữ và số
    text = re.sub('\\W', ' ', text)
    # Loại bỏ các từ chứa chữ số
    text = re.sub('\w*\d\w*', '', text)
    # Loại bỏ dấu xuống dòng
    text = re.sub('\n', ' ', text)
    # Loại bỏ nhiều khoảng trắng liên tiếp
    text = re.sub('\s+', ' ', text)
    # Xóa khoảng trắng ở đầu và cuối văn bản
    text = text.strip()

    for word in text.split():
        if word not in stopwords:
            update_text += word+" "
    
    return update_text.strip()

class English:
    def __init__(self,title=None, text=None) -> None:
        self.title = title
        self.text = text
        self.vectorizer_file = os.path.abspath("Vector/English/English_vectorizer_TF.joblib")
        self.smv_file = os.path.abspath("Vector/English/English_SVM_model_TF.joblib")

    def set_title(self, title):
        self.title = title

    def set_text(self, text):
        self.text = text

    def LoadLocation(self):
        vectorizer = joblib.load(self.vectorizer_file)
        model = joblib.load(self.smv_file)
        return vectorizer, model
    
    def predict(self,news, model,vectorizer):
        testing_news = {"news": [news]}
        new_def_test = pd.DataFrame(testing_news)

        new_def_test["news"] = new_def_test["news"].apply(wordopt)
        new_x_test = new_def_test["news"]
        new_xv_test = vectorizer.transform(new_x_test)
        pred = model.predict(new_xv_test)
        return pred[0]

    def Predict_Process(self):
        vectorizer,SVM_model = self.LoadLocation()
        news =  self.title + " " +  self.text
        pred_svm = self.predict(news,SVM_model,vectorizer)
        return pred_svm