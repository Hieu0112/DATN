import joblib
from underthesea import word_tokenize
import re
import pandas as pd
import warnings
import os
from sklearn.metrics import accuracy_score
import time
import numpy as np

from nltk.corpus import stopwords

warnings.filterwarnings("ignore")
stopword=list(stopwords.words('english'))

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

def sentence_vector(sentence, model):
    # Calculate average Word2Vec vector for each word in sentence if it exists in the vocabulary
    vectors = [model.wv[word] for word in sentence if word in model.wv]
    if len(vectors) > 0:
        return np.mean(vectors, axis=0)
    else:
        return np.zeros(model.vector_size)

def LoadLocation(_Vector):
    vectorizer_file=''
    DT_file=''
    NB_file=''
    RFC_file=''
    SVM_file=''
    DetailsPre=''
    Predict=''
    if _Vector=='CV': 
        vectorizer_file = os.path.abspath("Model/English/CV/English_vectorizer_CV.joblib")
        DT_file = os.path.abspath("Model/English/CV/English_DTC_model_CV.joblib")
        NB_file = os.path.abspath("Model/English/CV/English_NB_model_CV.joblib")
        RFC_file = os.path.abspath("Model/English/CV/English_RFC_model_CV.joblib")
        SVM_file = os.path.abspath("Model/English/CV/English_SVM_model_CV.joblib")

        DetailsPre = os.path.abspath("Predict/English/DetailsPre_CV.csv")
        Predict = os.path.abspath("Predict/English/Predict_CV.csv")
    elif _Vector=='TF':
        vectorizer_file = os.path.abspath("Model/English/TF/English_vectorizer_TF.joblib")
        DT_file = os.path.abspath("Model/English/TF/English_DTC_model_TF.joblib")
        NB_file = os.path.abspath("Model/English/TF/English_NB_model_TF.joblib")
        RFC_file = os.path.abspath("Model/English/TF/English_RFC_model_TF.joblib")
        SVM_file = os.path.abspath("Model/English/TF/English_SVM_model_TF.joblib")

        DetailsPre = os.path.abspath("Predict/English/DetailsPre_TF.csv")
        Predict = os.path.abspath("Predict/English/Predict_TF.csv")
    
    elif _Vector == 'W2V':
        vectorizer_file = os.path.abspath("Model/English/W2V/English_vectorizer_W2V.joblib")
        DT_file = os.path.abspath("Model/English/W2V/English_DTC_model_W2V.joblib")
        NB_file = os.path.abspath("Model/English/W2V/English_NB_model_W2V.joblib")
        RFC_file = os.path.abspath("Model/English/W2V/English_RFC_model_W2V.joblib")
        SVM_file = os.path.abspath("Model/English/W2V/English_SVM_model_W2V.joblib")

        DetailsPre = os.path.abspath("Predict/English/DetailsPre_W2V.csv")
        Predict = os.path.abspath("Predict/English/Predict_W2V.csv")

    elif _Vector == 'D2V':
        vectorizer_file = os.path.abspath("Model/English/D2V/English_vectorizer_D2V.joblib")
        DT_file = os.path.abspath("Model/English/D2V/English_DTC_model_D2V.joblib")
        NB_file = os.path.abspath("Model/English/D2V/English_NB_model_D2V.joblib")
        RFC_file = os.path.abspath("Model/English/D2V/English_RFC_model_D2V.joblib")
        SVM_file = os.path.abspath("Model/English/D2V/English_SVM_model_D2V.joblib")

        DetailsPre = os.path.abspath("Predict/English/DetailsPre_D2V.csv")
        Predict = os.path.abspath("Predict/English/Predict_D2V.csv")
    
    print("Load location: ")
    print(vectorizer_file)
    print(DT_file)
    if NB_file:
        print(NB_file)
    print(RFC_file)
    print(SVM_file)

    print(DetailsPre)
    print(Predict)

    vectorizer = joblib.load(vectorizer_file)
    DTC_model = joblib.load(DT_file)
    RFC_model = joblib.load(RFC_file)
    SVM_model = joblib.load(SVM_file)
    # Load NB_model only if NB_file is defined
    NB_model = joblib.load(NB_file) if NB_file else None

    return vectorizer, DTC_model, NB_model, RFC_model, SVM_model, DetailsPre, Predict

test_data_path = os.path.abspath("Data_Test/Test_English.csv")
test_data = pd.read_csv(test_data_path)

# Prediction function
def predict(news, model,vectorizer,Type_Vector):
    if Type_Vector == 'CV' or Type_Vector =='TF':
        testing_news = {"news": [news]}
        new_def_test = pd.DataFrame(testing_news)

        new_def_test["news"] = new_def_test["news"].apply(wordopt)

        new_x_test = new_def_test["news"]
        new_xv_test = vectorizer.transform(new_x_test)
        pred = model.predict(new_xv_test)

    elif Type_Vector == 'W2V':
        preprocessed_news = wordopt(news)
        tokenized_news = preprocessed_news.split()  # Tokenize text into words

        news_vector = sentence_vector(tokenized_news, vectorizer).reshape(1, -1)
        pred = model.predict(news_vector)

    elif Type_Vector == 'D2V':
        preprocessed_news = wordopt(news)
        tokenized_news = preprocessed_news.split()  # Tokenize text into words

        news_vector = vectorizer.infer_vector(tokenized_news).reshape(1, -1)
        pred = model.predict(news_vector)
    return pred[0]

# Prepare for results collection
y_true = test_data['label']  # True labels for comparison

def Predict_Process(Type_Vector):

    vectorizer,DTC_model,NB_model,RFC_model,SVM_model,DetailsPre,Predict = LoadLocation(Type_Vector)

    y_pred_dt = []  # Decision Tree predictions
    y_pred_nb = []  # Naive Bayes predictions
    y_pred_rfc = []
    y_pred_svm = []
    results = []

    for _, row in test_data.iterrows():
        # Combine 'title' and 'text' for the test input and preprocess the text
        news = ' |title| '+ row["title"] +' |text| '+  row["text"] 

        pred_dt = predict(news,DTC_model,vectorizer,Type_Vector)
        y_pred_dt.append(pred_dt)

        if NB_model is not None:
            pred_nb = predict(news, NB_model, vectorizer,Type_Vector)
            y_pred_nb.append(pred_nb)
        else:
            pred_nb = None  # Assign None if the model is not available


        pred_rfc = predict(news,RFC_model,vectorizer,Type_Vector)
        y_pred_rfc.append(pred_rfc)

        pred_svm = predict(news,SVM_model,vectorizer,Type_Vector)
        y_pred_svm.append(pred_svm)


        # Collect the result
        results.append({
            'Title': row['title'],
            'True Label': row['label'],
            'DT Prediction': pred_dt,
            'NB Prediction': pred_nb,
            'RFC Prediction': pred_rfc,
            'SVM Prediction': pred_svm,
        })
    
    # Convert results to DataFrame and save
    results_df = pd.DataFrame(results)
    results_df.to_csv(DetailsPre, index=False)

    # Calculate accuracy for both models
    accuracy_dt = accuracy_score(y_true, y_pred_dt)
    
    if NB_model is not None:
        accuracy_nb = accuracy_score(y_true, y_pred_nb)
    else:
        accuracy_nb = None  # or set to some default value


    accuracy_rfc = accuracy_score(y_true, y_pred_rfc)
    accuracy_svm = accuracy_score(y_true, y_pred_svm)


    # Calculate the difference in predictions for each model
    difference_dt = (y_true != y_pred_dt).mean() * 100
    difference_nb = (y_true != y_pred_nb).mean() * 100 if NB_model is not None else None
    difference_rfc = (y_true != y_pred_rfc).mean() * 100
    difference_svm = (y_true != y_pred_svm).mean() * 100

    accuracy_results_data = {
    'Model': ['DT', 'RFC', 'SVM'],
    'Accuracy (%)': [accuracy_dt * 100, accuracy_rfc * 100, accuracy_svm * 100],
    'Difference in Predictions (%)': [difference_dt, difference_rfc, difference_svm]
    }

    # Only add NB to the results if it's available
    if NB_model is not None:
        accuracy_results_data['Model'].insert(1, 'NB')  # Insert NB model in the second position
        accuracy_results_data['Accuracy (%)'].insert(1, accuracy_nb * 100)
        accuracy_results_data['Difference in Predictions (%)'].insert(1, difference_nb)

    accuracy_results_df = pd.DataFrame(accuracy_results_data)
    # Save the accuracy results to a CSV file
    accuracy_results_df.to_csv(Predict, index=False)


if __name__ == "__main__":
    print('Bắt đầu xử lý CountVectorizer')
    Predict_Process('CV')
    print('Đã xử lý xong CountVectorizer')

    print()
    print('--------------------------------------')
    print()
    time.sleep(5)

    print('Bắt đầu xử lý TfidfVectorizer')
    Predict_Process('TF')
    print('Đã xử lý xong TfidfVectorizer')

    print()
    print('--------------------------------------')
    print()
    time.sleep(5)

    print('Bắt đầu xử lý Word2Vec')
    Predict_Process('W2V')
    print('Đã xử lý xong Word2Vec ')

    print()
    print('--------------------------------------')
    print()
    time.sleep(5)

    print('Bắt đầu xử lý Doc2Vec')
    Predict_Process('D2V')
    print('Đã xử lý xong Doc2Vec ')

    print()
    print('--------------------------------------')
    print()
