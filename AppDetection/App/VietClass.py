import joblib
import re
import pandas as pd
import warnings
import os
warnings.filterwarnings("ignore")
from pyvi import ViTokenizer

def tokenizerVN(text):
        return ViTokenizer.tokenize(text)

def tokenize(sentence):
    return tokenizerVN(sentence).split()

def remove_special_characters(text):
    ## Remove punctuations
    text = text.lower()
    text = re.sub('[%s]' % re.escape("""!–"#$%&'()*+,،-./:;<=>؟?@[\]^`{|}~“”…"""), ' ', text)
    text = text.replace('؛',"", )
    text = re.sub('https?:\/\/.*[\r\n]*', ' ', text)
    text = re.sub('[^\w\s]', ' ', text) 
    text = re.sub('\n', ' ', text)
    text = re.sub('\s+', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text =  " ".join(text.split())
    return text.strip()

def preprocess_nostop(text):
    text = remove_special_characters(text)
    return text

class Vietnamese:
    def __init__(self,title=None, text=None) -> None:
        self.title = title
        self.text = text
        self.vectorizer_file = os.path.abspath("Vector/Vietnamese/Vietnamese_vectorizer_TF.joblib")
        self.smv_file = os.path.abspath("Vector/Vietnamese/Vietnamese_SVM_model_TF.joblib")

    def set_title(self, title):
        self.title = title

    def set_text(self, text):
        self.text = text

    def LoadLocation(self):
        vectorizer = joblib.load(self.vectorizer_file)
        SVM_model = joblib.load(self.smv_file)
        return vectorizer, SVM_model
    
    def predict(self,news, model,vectorizer):
        testing_news = {"news": [news]}
        new_def_test = pd.DataFrame(testing_news)

        new_def_test["news"] = new_def_test["news"].apply(tokenizerVN)
        new_def_test["news"] = new_def_test["news"].apply(preprocess_nostop)
        new_x_test = new_def_test["news"]
        new_xv_test = vectorizer.transform(new_x_test)
        pred = model.predict(new_xv_test)
        return pred[0]

    def Predict_Process(self):
        vectorizer,SVM_model = self.LoadLocation()
        news = ' |title| '+ self.title +' |text| '+  self.text
        pred_svm = self.predict(news,SVM_model,vectorizer)
        return pred_svm