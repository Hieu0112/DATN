import joblib
from underthesea import word_tokenize
import re
import pandas as pd
import warnings
import os
from sklearn.metrics import accuracy_score
import time

from nltk.corpus import stopwords

warnings.filterwarnings("ignore")
stopword=list(stopwords.words('english'))

def tokenize(sentence):
    return word_tokenize(sentence, format = 'word')

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


    text=re.sub(r"[-()\"#!@$%^&*{}?.,:]"," ",text)
    text=re.sub(r"\s+"," ",text)

    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W", " ", text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)

    for word in text.split():
        if word not in stopword:
            update_text+=word+" "
    
    return update_text.strip()

def LoadLocation(_Vector):
    vectorizer_file=''
    DT_file=''
    NB_file=''
    DetailsPre=''
    Predict=''
    if _Vector=='CV': 
        vectorizer_file = os.path.abspath("Model/English/CV/English_vectorizer_CV.joblib")
        DT_file = os.path.abspath("Model/English/CV/English_DTC_model_CV.joblib")
        NB_file = os.path.abspath("Model/English/CV/English_NB_model_CV.joblib")
        RFC_file = os.path.abspath("Model/English/CV/English_RFC_model_CV.joblib")

        DetailsPre = os.path.abspath("Predict/English/DetailsPre_CV.csv")
        Predict = os.path.abspath("Predict/English/Predict_CV.csv")
    elif _Vector=='TF':
        vectorizer_file = os.path.abspath("Model/English/TF/English_vectorizer_TF.joblib")
        DT_file = os.path.abspath("Model/English/TF/English_DTC_model_TF.joblib")
        NB_file = os.path.abspath("Model/English/TF/English_NB_model_TF.joblib")
        RFC_file = os.path.abspath("Model/English/TF/English_RFC_model_TF.joblib")

        DetailsPre = os.path.abspath("Predict/English/DetailsPre_TF.csv")
        Predict = os.path.abspath("Predict/English/Predict_TF.csv")
    
    print("Load location: ")
    print(vectorizer_file)
    print(DT_file)
    print(NB_file)
    print(RFC_file)
    print(DetailsPre)
    print(Predict)

    vectorizer = joblib.load(vectorizer_file)
    DTC_model = joblib.load(DT_file)
    NB_model = joblib.load(NB_file)
    RFC_model = joblib.load(RFC_file)

    return vectorizer,DTC_model,NB_model,RFC_model,DetailsPre,Predict

test_data_path = os.path.abspath("Data_Test/Test_English.csv")
test_data = pd.read_csv(test_data_path)

# Prediction function
def predict(news, model,vectorizer):
    return manual_testing(news, model, vectorizer)

def manual_testing(news, _model, _vectorizer):
    testing_news = {"news": [news]}
    new_def_test = pd.DataFrame(testing_news)

    new_def_test["news"] = new_def_test["news"].apply(wordopt)

    new_x_test = new_def_test["news"]
    new_xv_test = _vectorizer.transform(new_x_test)
    pred = _model.predict(new_xv_test)
    return pred[0]

# Prepare for results collection
y_true = test_data['label']  # True labels for comparison

def Predict_Process(Type_Vector):

    vectorizer,DTC_model,NB_model,RFC_model,DetailsPre,Predict = LoadLocation(Type_Vector)

    y_pred_dt = []  # Decision Tree predictions
    y_pred_nb = []  # Naive Bayes predictions
    y_pred_rfc = []
    results = []

    for _, row in test_data.iterrows():
        # Combine 'title' and 'text' for the test input and preprocess the text
        news = ' |title| '+ row["title"] +' |text| '+  row["text"] 

        pred_dt = predict(news,DTC_model,vectorizer)
        y_pred_dt.append(pred_dt)

        # Predict using Naive Bayes
        pred_nb = predict(news,NB_model,vectorizer)
        y_pred_nb.append(pred_nb)

        pred_rfc = predict(news,RFC_model,vectorizer)
        y_pred_rfc.append(pred_rfc)

        # Collect the result
        results.append({
            'Title': row['title'],
            'True Label': row['label'],
            'DT Prediction': pred_dt,
            'NB Prediction': pred_nb,
            'RFC Prediction': pred_rfc,
        })
    

    # Convert results to DataFrame and save
    results_df = pd.DataFrame(results)

    results_df.to_csv(DetailsPre, index=False)

    # Calculate accuracy for both models
    accuracy_dt = accuracy_score(y_true, y_pred_dt)
    accuracy_nb = accuracy_score(y_true, y_pred_nb)
    accuracy_rfc = accuracy_score(y_true, y_pred_rfc)


    # Calculate the difference in predictions for each model
    difference_dt = (y_true != y_pred_dt).mean() * 100
    difference_nb = (y_true != y_pred_nb).mean() * 100
    difference_rfc = (y_true != y_pred_rfc).mean() * 100

    # Create a DataFrame to store the accuracy and prediction differences
    accuracy_results_df = pd.DataFrame({
    'Model': ['DT', 'NB','RFC'],
    'Accuracy (%)': [accuracy_dt * 100, accuracy_nb * 100, accuracy_rfc*100],
    'Difference in Predictions (%)': [difference_dt, difference_nb, difference_rfc]
    })

    # Save the accuracy results to a CSV file
    accuracy_results_df.to_csv(Predict, index=False)


if __name__ == "__main__":
    print('Bắt đầu xử lý CountVectorizer')
    Predict_Process('CV')
    print('Đã xử lý xong CountVectorizer')

    time.sleep(5)
    print()
    print('--------------------------------------')
    print()

    print('Bắt đầu xử lý CountVectorizer')
    Predict_Process('TF')
    print('Đã xử lý xong TfidfVectorizer')
