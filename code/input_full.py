import joblib
from underthesea import word_tokenize
import re
import pandas as pd
import streamlit as st
import warnings
warnings.filterwarnings("ignore")


# Function to clean the text
def wordopt(text):
    if pd.isnull(text):  # Handle NaN values for 'author'
        return "anonymous"
    text = text.lower()
    text = re.sub('https?:\/\/.*[\r\n]*', ' ', text)
    text = re.sub('[^\w\s]', ' ', text)
    text = re.sub('\n', ' ', text)
    return text


# Tokenization using underthesea
def tokenize(sentence):
    return word_tokenize(sentence, format='word')


# Load the model based on user selection
def getModel(model_type):
    if model_type == "Decision Tree":
        return joblib.load('DT_model.joblib')
    else:
        return joblib.load('NB_model.joblib')


# Prediction function
def predict(title, text, author, domain, model_type):
    # Load vectorizer and model
    vectorizer = joblib.load('vectorizer.joblib')
    return manual_testing(title, text, author, domain, getModel(model_type), vectorizer)


# Adjusted manual_testing function
@st.cache_data
def manual_testing(title, text, author, domain, _model, _vectorizer):
    # Combine fields like in training
    combined_input = f"{title} _ {text} _ {author} _ {domain}"
    
    # Preprocess the combined input
    testing_data = {"combined": [combined_input]}
    new_def_test = pd.DataFrame(testing_data)
    new_def_test["combined"] = new_def_test["combined"].apply(wordopt)
    
    # Transform using vectorizer
    new_xv_test = _vectorizer.transform(new_def_test["combined"])
    
    # Predict and return result
    pred = _model.predict(new_xv_test)
    return pred[0]


# Check if inputs are provided correctly
def checker(model_type, title, text, author, domain):
    global model_checker
    global text_checker
    checker = True
    if model_type == "None":
        model_checker.warning("Please choose a model")
        checker = False
    if title == "" or text == "" or author == "" or domain == "":
        text_checker.warning("Please input all fields")
        checker = False
    return checker


# Streamlit UI
st.title("Fake News Detection")
choices = ["None", "Decision Tree", "NaiveBayes"]

# Model selection
model_holder = st.empty()
model_type = model_holder.selectbox("Choose model", choices, index=0, key="model")
model_checker = st.empty()

# Input fields for title, text, author, and domain
title = st.text_input("Input title here", "")
text = st.text_area("Input your text here", "")
author = st.text_input("Input author here", "")
domain = st.text_input("Input source domain here", "")
text_checker = st.empty()

# Predict button
if st.button("Predict now"):
    if checker(model_type, title, text, author, domain):
        result = predict(title, text, author, domain, model_type)
        if result == 1:
            st.error("This is fake news")
        else:
            st.success("This is not fake news")
