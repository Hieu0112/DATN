from VietClass import Vietnamese
from EngClass import English
from pyvi import ViTokenizer
from nltk.tokenize import word_tokenize
from langdetect import detect
import os
import streamlit as st
import pandas as pd

def Language(text):
    return detect(text)

def tokenize(text):
    try:
        lang = Language(text)
        if lang == 'vi':  
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
        title_checker.warning("Nhập tiêu đề bài viết")
    if text == "":
        text_checker.warning("Nhập nội dung bài viết")
        checker = False
    return checker


st.title("Phát hiện tin giả")

# Khởi tạo trạng thái cho title và text
if "title" not in st.session_state:
    st.session_state.title = ""
if "text" not in st.session_state:
    st.session_state.text = ""

# Tải lên tệp CSV
uploaded_file = st.file_uploader("Chọn một tệp .CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if 'title' in df.columns and 'text' in df.columns:
            # Kiểm tra nếu có dữ liệu trong tệp
            if not df.empty:
                # Gán giá trị từ dòng đầu tiên vào session state
                st.session_state.title = df.iloc[0]['title']
                st.session_state.text = df.iloc[0]['text']
            else:
                st.warning("Tệp CSV không có dữ liệu.")
        else:
            st.error("Tệp CSV không chứa cột 'title' và 'text'.")
    except Exception as e:
        st.error(f"Đã xảy ra lỗi khi đọc tệp: {e}")

title = st.text_area("Tiêu đề bài viết", key="title")
text = st.text_area("Nội dung bài viết", key="text")


title_checker = st.empty()
text_checker = st.empty()

if st.button("Dự đoán"):
    if checker(title, text):
        result = Predict(title,text) 
        lang = "Việt Nam" if Language(text) =='vi' else "English"
        true = "Đây là tin có thể tin tưởng." if Language(text) =='vi' else "This is trustworthy news."
        false = "Đây là tin không thể tin tưởng." if Language(text) =='vi' else "This is unreliable news."
        st.text("Loại ngôn ngữ đang dự đoán là: "+ lang)
        if result == 0:
            st.success(true)
        else:
            st.error(false)

