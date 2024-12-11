from VietClass import Vietnamese
from EngClass import English
from pyvi import ViTokenizer
from nltk.tokenize import word_tokenize
from langdetect import detect
import os
import streamlit as st

def Language(text):
    return detect(text)

def tokenize(text):
    try:
        # Phát hiện ngôn ngữ của văn bản
        lang = Language(text)
        # Tokenize theo ngôn ngữ
        if lang == 'vi':  # Tiếng Việt
            return ViTokenizer.tokenize(text).split()
        else:
            return word_tokenize(text)
    except:
        return text.split()
    
vectorizer_Vietnamese = os.path.abspath("Vector/Vietnamese/Vietnamese_vectorizer_TF.joblib")
model_Vietnamese = os.path.abspath("Vector/Vietnamese/Vietnamese_SVM_model_TF.joblib")

vectorizer_English = os.path.abspath("Vector/English/English_vectorizer_TF.joblib")
model_english = os.path.abspath("Vector/English/English_SVM_model_TF.joblib")


# @st.cache
def Predict(title,text):
    lang = Language(text)
    if lang == 'vi':
        print(lang)
        return Vietnamese(title,text,vectorizer_Vietnamese,model_Vietnamese).Predict_Process()
    else:
        print(lang)
        return English(title,text,vectorizer_English,model_english).Predict_Process()


def checker(title,text):
    global title_checker
    global text_checker
    checker = True
    if title == "":
        title_checker.warning("Please input your text")
        checker = False
    if text == "":
        text_checker.warning("Please input your text")
        checker = False
    return checker


st.title("Fake News Detection")

title = st.text_area("Input your title here", "")
text = st.text_area("Input your text here", "")
title_checker = st.empty()
text_checker = st.empty()
if st.button("Predict now"):
    if checker(title, text):
        result = Predict(title,text) 
        lang = "Việt Nam" if Language(text) =='vi' else "English"
        true = "Đây là tin có thể tin tưởng " if Language(text) =='vi' else "This is not fake news"
        false = "Đây là tin không thể tin tưởng " if Language(text) =='vi' else "This is fake news"

        st.text("Loại ngôn ngữ đang dự đoán là: "+ lang)
        if result == 0:
            st.success(true)
        else:
            st.error(false)
