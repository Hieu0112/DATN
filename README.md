# 1, Thông tin
- Đồ án tốt nghiệp: Nghiên cứu phát hiện tin giả độc hại
- Người thực hiện: Trịnh Viết Hiếu
- Mã sinh Viên: B20DCAT063
- Lớp: D20CQAT03-B

# 2, Lý thuyết
- Tìm hiểu tin giả(đã xong)
- Tìm hiểu học máy, học sâu(đã xong)
- Báo cáo đã xong mục lý thuyết, khái quát

# 3, Thu thập dữ liệu
- Các thư mục trong demo
    + Data_Collect: Thu thập dữ liệu trên github và code lấy dữ liệu từ các trang web
        * DataEnglish: Các file csv đã thu thập được > tiếng anh
        * DataFake: Các file csv đã thu thập được: các đường link, chi tiết bài báo, dữ liệu github, code để lấy dữ liệu > tiếng việt
        * DataReal: Các file csv đã thu thập được: các đường link, chi tiết bài báo, dữ liệu github, code để lấy dữ liệu > tiếng anh
    + Data_Train: Dữ liệu để train cho demo để xây dựng mô hình
    + Data_Test: Dữ liệu để test cho demo sau khi xây dựng mô hình
    + Process_Data_Train: Chuẩn hóa dữ liệu trước khi train và tách dữ liệu lưu vào Data_Train và Data_Test
    + Demo: 
        * Xây dựng thuật toán
        * Code demo sau khi xây dựng và lưu model
    + Evaluate: Tính toán các độ đo PPV, TPR, ACC, F1, FPR, FNR
    + Model: Lưu trữ các model ban đầu
    + Predict: Lưu trữ dự đoán thực thế sau khi xây dựng
    + Vector: Lưu trữ vector hóa ngôn ngữ


- Code lấy tin tức từ trang trang web uy tín: 9 trang web độc hại + 1 link git
- Code lấy tin tức từ các trang mạng độc hại: 5 trang web độc hại + 1 link git
- Data Train:
    + Data Việt Nam: 12600 tin
        * True: 6600 tin
        * Fake: 6000 tin
    - Data English: 39000 tin 
        * True: 19500 tin
        * Fake: 19500 tin
- Data Test:
    + Data Việt Nam: 1367 tin
        * True: 1277 tin
        * Fake: 90 tin
    - Data English: 200 tin 
        * True: 100 tin
        * Fake: 100 tin

# 4, Xây dựng mô hình
- Tiền xử lý dữ liệu:
    + Xử lý tiếng Việt
    + Xử lý tiếng Anh

- Vector hóa:
    + CountVectorizer
    + TfidfVectorizer
    + Word2Vec
    + Doc2Vec
- Code thuật toán:
    + Decision Tree: đã code, đang tối ưu
    + Navie bayes: đã code, đang tối ưu
    + GaussianNBt: đã code, đang tối ưu
    + Random Forest: đã code, đang tối ưu
    + Support Vector Machines(SVM): đã code, đang tối ưu
- Tạo app demo nhiều dữ liệu cùng lúc 2 app riêng biệt xử lý tiếng việt + tiếng anh: đã code, đang tối ưu
- Tạo app để demo: Sửa lại lựa chọn ngôn ngữ -> lựa chọn mô hình -> nhập dữ liệu -> dự đoán -> đang xây dựng

