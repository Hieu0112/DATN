from gensim.models.doc2vec import Doc2Vec,\
    TaggedDocument
from nltk.tokenize import word_tokenize

from nltk.corpus import stopwords

# # Tải stopwords từ NLTK nếu chưa tải
# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')

# Danh sách stopwords
stopwords = set(stopwords.words('english'))
 
# define a list of documents.
data = ["This is the first document",
        "This is the second document",
        "This is the third document",
        "This is the fourth document"]
 
def preprocess(doc):
    words = word_tokenize(doc)
    return [word for word in words if word not in stopwords]

documents = [TaggedDocument(preprocess(doc), [i]) for i, doc in enumerate(data)]
print(documents)
# train the Doc2vec model
model = Doc2Vec(vector_size=20,
                min_count=2, epochs=50)
model.build_vocab(documents)
model.train(documents,
            total_examples=model.corpus_count,
            epochs=model.epochs)
 
# get the document vectors
document_vectors = [model.infer_vector(
    word_tokenize(doc.lower())) for doc in data]
 
#  print the document vectors
for i, doc in enumerate(data):
    print("Document", i+1, ":", doc)
    print("Vector:", document_vectors[i])
    print()