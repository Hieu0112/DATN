import joblib
from underthesea import word_tokenize
import re
import pandas as pd
import warnings
import os
from sklearn.metrics import accuracy_score
warnings.filterwarnings("ignore")
from pyvi import ViTokenizer




def wordopt(text):
    text = text.lower()
    text = re.sub('https?:\/\/.*[\r\n]*', ' ', text)
    text = re.sub('[^\w\s]', ' ', text) 
    text = re.sub('\n', ' ', text)
    return text

#delete numbers
def delete_numbers(text):
    return re.sub(r'\d+', ' ', text)
#lower case
def lower(text):
    return text.lower()
#delete special characters
def remove_special_characters(text):
    ## Remove punctuations
    text = re.sub('[%s]' % re.escape("""!–"#$%&'()*+,،-./:;<=>؟?@[\]^`{|}~“”…"""), ' ', text)
    text = text.replace('؛',"", )
    text = re.sub('\s+', ' ', text)
    text =  " ".join(text.split())
    return text.strip()
#delete stop words
# def remove_stopwords(text):
#     # words = text.split()
#     # mean_word = [word for word in words if word not in stopwords]
#     # mean_text = " ".join(mean_word)
#     clean_tokens = ' '.join([word for word in text.split() if word not in stopwords])
#     return clean_tokens

def preprocess_nostop(text):
    text = delete_numbers(text)
    text = lower(text)
    text = remove_special_characters(text)
    return text


# Compound Vietnamese word
def tokenizerVN(text):
    return ViTokenizer.tokenize(text)
# Tokenizer
def tokenizer(text):
    return word_tokenize(text)
# Count token
def count_token(text):
    word = tokenizerVN(str(text))
    return len(word.split())

def tokenize(sentence):
    return tokenizerVN(sentence).split()


vectorizer_file = os.path.abspath("Model/Vietnamese/vectorizer.joblib")
vectorizer = joblib.load(vectorizer_file)

DT_file = os.path.abspath("Model/Vietnamese/DT_model.joblib")
DTC_model = joblib.load(DT_file)

NB_file = os.path.abspath("Model/Vietnamese/NB_model.joblib")
NB_model = joblib.load(NB_file)

# Load the test data from test.csv
test_data_path = os.path.abspath("Data_Test/Test_Vietnamese.csv")
test_data = pd.read_csv(test_data_path)

DetailsPre = os.path.abspath("Predict/Vietnamese/DetailsPre.csv")
Predict = os.path.abspath("Predict/Vietnamese/Predict.csv")

# Prediction function
def predict(news, model):
    return manual_testing(news, model, vectorizer)

def manual_testing(news, _model, _vectorizer):
    testing_news = {"news": [news]}
    new_def_test = pd.DataFrame(testing_news)

    new_def_test["news"] = new_def_test["news"].apply(tokenizerVN)
    new_def_test["news"] = new_def_test["news"].apply(preprocess_nostop)

    new_x_test = new_def_test["news"]
    new_xv_test = _vectorizer.transform(new_x_test)
    pred = _model.predict(new_xv_test)
    return pred[0]

# Prepare for results collection
y_true = test_data['label']  # True labels for comparison
y_pred_dt = []  # Decision Tree predictions
y_pred_nb = []  # Naive Bayes predictions

results = []



for _, row in test_data.iterrows():
    # Combine 'title' and 'text' for the test input and preprocess the text
    news = ' |title| '+ row["title"] +' |text| '+  row["text"] 

    pred_dt = predict(news,DTC_model)
    y_pred_dt.append(pred_dt)

    # Predict using Naive Bayes
    pred_nb = predict(news,NB_model)
    y_pred_nb.append(pred_nb)

    # Collect the result
    results.append({
        'Title': row['title'],
        'True Label': row['label'],
        'Decision Tree Prediction': pred_dt,
        'Naive Bayes Prediction': pred_nb
    })



# Convert results to DataFrame and save
results_df = pd.DataFrame(results)

results_df.to_csv(DetailsPre, index=False)

# Calculate accuracy for both models
accuracy_dt = accuracy_score(y_true, y_pred_dt)
accuracy_nb = accuracy_score(y_true, y_pred_nb)

print(f"Accuracy of Decision Tree: {accuracy_dt * 100:.2f}%")
print(f"Accuracy of Naive Bayes: {accuracy_nb * 100:.2f}%")



# Calculate the difference in predictions for each model
difference_dt = (y_true != y_pred_dt).mean() * 100
difference_nb = (y_true != y_pred_nb).mean() * 100

print(f"Difference in predictions for Decision Tree: {difference_dt:.2f}%")
print(f"Difference in predictions for Naive Bayes: {difference_nb:.2f}%")

print(f"Predictions saved to {DetailsPre}")

# Create a DataFrame to store the accuracy and prediction differences
accuracy_results_df = pd.DataFrame({
    'Model': ['Decision Tree', 'Naive Bayes'],
    'Accuracy (%)': [accuracy_dt * 100, accuracy_nb * 100],
    'Difference in Predictions (%)': [difference_dt, difference_nb]
})

# Save the accuracy results to a CSV file
accuracy_results_df.to_csv(Predict, index=False)

print(f"Accuracy results saved to {Predict}")