from VietClass import Vietnamese
from EngClass import English
from pyvi import ViTokenizer
from nltk.tokenize import word_tokenize
from langdetect import detect
import pandas as pd
import os
import csv

def tokenize(text):
    try:
        # Phát hiện ngôn ngữ của văn bản
        lang = detect(text)
        # Tokenize theo ngôn ngữ
        if lang == 'vi':  # Tiếng Việt
            return ViTokenizer.tokenize(text).split()
        else:
            return word_tokenize(text)
    except:
        return text.split()

# Dự đoán nhiều dữ liệu 1 lúc
# Tiếng anh

vectorizer_English = os.path.abspath("Vector/English/English_vectorizer_TF.joblib")
model_english = os.path.abspath("Vector/English/English_SVM_model_TF.joblib")

test_data_path = os.path.abspath("Data_Test/Test_English.csv")
test_data = pd.read_csv(test_data_path)
data=[]
for _,i in test_data.iterrows():
    title=i['title']
    text=i['text']
    label=i['label']
    pred = English(title,text,vectorizer_English,model_english).Predict_Process()
    data.append({"title": title, "label": label, "Prediction": pred})

file_path = os.path.abspath("AppDetection/App/Check_English.csv")

with open(file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["title","label", "Prediction"])
    writer.writeheader()
    for item in data:
        writer.writerow(item)

print(f'Data has been saved to {file_path}')

# Tiếng Việt

vectorizer_Vietnamese = os.path.abspath("Vector/Vietnamese/Vietnamese_vectorizer_TF.joblib")
model_Vietnamese = os.path.abspath("Vector/Vietnamese/Vietnamese_SVM_model_TF.joblib")
test_data_path = os.path.abspath("Data_Test/Test_Vietnamese200.csv")
test_data = pd.read_csv(test_data_path)
data=[]
for _,i in test_data.iterrows():
    title=i['title']
    text=i['text']
    label=i['label']
    pred = Vietnamese(title,text,vectorizer_Vietnamese,model_Vietnamese).Predict_Process()
    data.append({"title": title, "label": label, "Prediction": pred})

file_path = os.path.abspath("AppDetection/App/Check_Vietnamese.csv")

with open(file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["title","label", "Prediction"])
    writer.writeheader()
    for item in data:
        writer.writerow(item)

print(f'Data has been saved to {file_path}')


# Dự đoán 1 dữ liệu nhập