import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer

# # Tải dữ liệu từ NLTK
# nltk.download('stopwords')  # Tải stopwords
# nltk.download('punkt')       # Tải punkt
# nltk.download('punkt_tab')    # Tải punkt_tab nếu cần thiết

import nltk
from nltk.corpus import stopwords

# Tải stopwords từ NLTK nếu chưa tải
# nltk.download('stopwords')

# Sử dụng danh sách từ dừng (stopwords) của tiếng Anh từ NLTK
stopword_list = list(stopwords.words('english'))
stopwords = [word for word in stopword_list if word.strip() != '']

def tokenize(sentence):
    return word_tokenize(sentence)

vectorizerCV = CountVectorizer(
    stop_words = stopwords,
    tokenizer = tokenize,
)

# Dữ liệu mẫu
data = ["EPIC! CHECK OUT THE T-SHIRTS Two Guys Wore Behind Hillary During A Town Hall,This is really epic and just hysterical! It s also the second time someone has trolled one of Hillary s town halls. Remember Sticker Boy? He s the guy who stole the show from Hillary during her speech in Iowa by eating stickers. This takes the cake though:Several members of the audience at a New Hampshire campaign event for Hillary Clinton sported some creative t-shirts and they made sure TV cameras could capture their t-shirts while Hillary spoke. At least two men wore Settle For Hillary t-shirts that utilized the official logo and font of Hillary Clinton s presidential campaign.Check out the guy in the baseball cap: Settle for Hillary Jeff Bechdel the communications director for America Rising a Republican PAC focused on conducting and distributing opposition research posted a television screenshot of the t-shirts on Monday night. Bechdel screencapped ABC News footage of Hillary s event and posted a picture on Twitter:Via: The Federalist,1"]
vectorized = vectorizerCV.fit_transform(data)

# # In kết quả
print("Từ vựng:", vectorizerCV.get_feature_names_out())
