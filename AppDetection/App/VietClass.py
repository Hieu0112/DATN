import joblib
import re
import pandas as pd
import warnings
import os
warnings.filterwarnings("ignore")
from pyvi import ViTokenizer

def tokenizerVN(text):
        return ViTokenizer.tokenize(text)

# def tokenize(sentence):
#     return tokenizerVN(sentence).split()

file_stopword = os.path.join("Data_Train", "vietnamese-stopwords-dash.txt")
with open(file_stopword, 'r', encoding='utf-8') as file:
    stopwords = file.read().split('\n')

def wordopt(text):
    ## Remove punctuations
    text = text.lower()
    # Loại bỏ các dấu câu đặc biệt
    text = re.sub('[%s]' % re.escape("""!–"#$%&'()*+,،-./:;<=>؟?@[\]^`{|}~“”…؛"""), ' ', text)
    # Loại bỏ các liên kết URL
    text = re.sub('https?://\S+|www\.\S+|https?:\/\/.*[\r\n]*', ' ', text)
    # Loại bỏ các thẻ HTML
    text = re.sub('<.*?>+', '', text)
    # Loại bỏ các chuỗi nằm trong dấu ngoặc vuông
    text = re.sub('\[.*?\]', '', text)
    # Loại bỏ ký tự không phải chữ và số
    text = re.sub('\\W', ' ', text)
    # Loại bỏ các từ chứa chữ số
    text = re.sub('\w*\d\w*', '', text)
    # Loại bỏ dấu xuống dòng
    text = re.sub('\n', ' ', text)
    # Loại bỏ nhiều khoảng trắng liên tiếp
    text = re.sub('\s+', ' ', text)
    # Xóa khoảng trắng ở đầu và cuối văn bản
    text = text.strip()

    update_text = ""
    for word in text.split():
        if word not in stopwords:
            update_text += word+" "

    return update_text.strip()

class Vietnamese:
    def __init__(self,title=None, text=None,vectorizer_file = None,smv_file = None) -> None:
        self.title = title
        self.text = text
        self.vectorizer_file = vectorizer_file
        self.smv_file = smv_file

    def LoadLocation(self):
        vectorizer = joblib.load(self.vectorizer_file)
        model = joblib.load(self.smv_file)
        return vectorizer, model
    
    def predict(self,news, model,vectorizer):
        testing_news = {"news": [news]}
        new_def_test = pd.DataFrame(testing_news)

        new_def_test["news"] = new_def_test["news"].apply(tokenizerVN)
        new_def_test["news"] = new_def_test["news"].apply(wordopt)
        
        new_x_test = new_def_test["news"]

        new_xv_test = vectorizer.transform(new_x_test)
        pred = model.predict(new_xv_test)
        return pred[0]

    def Predict_Process(self):
        vectorizer,SVM_model = self.LoadLocation()
        news =  self.title + " " +  self.text
        pred_svm = self.predict(news,SVM_model,vectorizer)
        return pred_svm

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)
# title="Bao giờ Diễn tập phương án xử lý tình huống đối tượng sử dụng vũ khí nóng cướp ngân hàng"
# text="Các đại biểu tham dự buổi diễn tập . Đại tá Huỳnh Ngọc Liêm phát biểu tại buổi diễn tập . Cuộc diễn tập huy động lực lượng gồm cán bộ chiến sĩ thuộc nhiều lực lượng trong Công an tỉnh Công an thành phố Phan Thiết Công an cơ sở bảo vệ ngân hàng lực lượng y tế và chó nghiệp vụ cùng nhiều trang thiết bị phương tiện công cụ hỗ trợ đặc chủng để tiến hành diễn tập tình huống. . Lực lượng tham gia buổi diễn tập . Theo đó tình huống giả định đặt ra: Vào hồi 8 giờ 30 tại trụ sở Ngân hàng TMCP Ngoại thương Việt Nam – Chi nhánh Bình Thuận thuộc phường Bình Hưng TP. Phan Thiết 5 đối tượng mang theo dao và súng đi xe ô tô đến trụ sở ngân hàng. Bọn chúng giả vờ làm khách hàng vào bên trong rồi tiến hành khống chế người dân vào giao dịch và nhân viên ngân hàng. Các đối tượng đã lấy được một số tiền lớn sau đó bỏ vào ba lô và nhanh chóng tẩu thoát. Khi vừa ra đến tiền sảnh ngân hàng thì phát hiện có lực lượng công an bao vây truy bắt nên đối tượng đã quay trở lại quầy giao dịch khống chế 12 con tin đưa lên tầng 3 để cố thủ đòi yêu sách chống trả lực lượng làm nhiệm vụ. . Tình huống giả định 5 đối tượng sử dụng vũ khí nóng cướp ngân hàng . Sau khoảng 1 giờ thương thuyết dưới sự chỉ đạo trực tiếp của Đại tá Huỳnh Ngọc Liêm Phó Giám đốc – Thủ trưởng Cơ quan CSĐT Công an tỉnh các lực lượng Công an tỉnh đã tổ chức các mũi đánh bắt đồng loạt tấn công khống chế và bắt giữ thành công 5 đối tượng giải cứu an toàn các con tin . Sau khi khống chế thành công các đối tượng lực lượng Cảnh sát phòng cháy chữa cháy và cứu nạn cứu hộ nhanh chóng tiếp cận triển khai các đội hình chữa cháy dập tắt hoàn toàn đám cháy hạn chế thấp nhất thiệt hại do vụ cháy gây ra. Các lực lượng điều tra viên kỹ thuật hình sự của Công an tỉnh phối hợp Công an TP. Phan Thiết nhanh chóng phong tỏa bảo vệ hiện trường tổ chức khám nghiệm thu thập dấu vết . . Lực lượng Công an phường nhanh chóng có mặt tại trụ sở ngân hàng . Lực lượng Cảnh sát Cơ động triển khai lực lượng đột nhập vào bên trong . Phát biểu tại buổi diễn tập Đại tá Huỳnh Ngọc Liêm – Phó Giám đốc Công an tỉnh ghi nhận đánh giá cao sự cố gắng nỗ lực sự phối hợp nhịp nhàng giữa các lực lượng tham gia diễn tập; việc bố trí lực lượng phương tiện và phương án triển khai để giải quyết tình huống diễn tập một cách nhanh chóng bài bản chính xác đảm bảo an toàn đáp ứng được mục tiêu yêu cầu đã đề ra. . Sử dụng quả nổ lựu đạn khói . Khống chế thành công các đối tượng . Thời gian qua Tỉnh ủy UBND tỉnh đã lãnh đạo chỉ đạo Công an tỉnh chủ trì triển khai quyết liệt nhiều biện pháp công tác kể cả phòng ngừa nghiệp vụ phòng ngừa xã hội để đấu tranh trấn áp mạnh với các loại tội phạm hành vi vi phạm pháp luật. Trong đó tội phạm cướp ngân hàng là một trong những loại tội phạm đặc biệt nguy hiểm đe dọa trực tiếp đến tính mạng sức khỏe của nhân viên và khách hàng. Các vụ cướp thường diễn ra rất mạnh động liều lĩnh sử dụng các loại hung khí vũ khí nguy hiểm. Từ đó đặt ra yêu cầu lớn cấp bách cho lực lượng bảo vệ và công an trong đấu tranh phòng chống tội phạm. Chính vì vậy buổi diễn tập đã giúp cho các lực lượng tham gia trang bị thêm kiến thức cách xử lý tình huống về ANTT có thể xảy ra; nâng cao cảnh giác trước các phương thức thủ đoạn của các loại tội phạm; tạo điều kiện giúp cán bộ chiến sĩ lực lượng nghiệp vụ Công an tỉnh thuần thục hơn với các phương án tác chiến đấu tranh tấn công trấn áp tội phạm giữ vững bình yên cuộc sống người dân. . NGUYỄN LUÂN"
# pred = Vietnamese(title,text).Predict_Process()
# print(pred)