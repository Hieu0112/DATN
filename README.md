# 1, Thông tin
- Đồ án tốt nghiệp: Nghiên cứu phát hiện tin giả độc hại
- Người thực hiện: Trịnh Viết Hiếu
- Mã sinh Viên: B20DCAT063
- Lớp: D20CQAT03-B

# 2, Lý thuyết
- Tìm hiểu tin giả(đã xong)
- Tìm hiểu học máy, học sâu(đã xong)
- Báo cáo đã xong mục lý thuyết, khái quát
# 3, Giới thiệu cấu trúc thư mục trong DATN
**Data_Collect: Thu thập dữ liệu trên github và code lấy dữ liệu từ các trang web**
    - DataEnglish
        + Details_English: Dữ liệu nguyên thủy lấy về
        + Train_English: Dữ liệu đã xử lý ở Subtract_Data_English.py
    - DataFake: Các file csv đã thu thập được: các đường link, chi tiết bài báo, dữ liệu github, code để lấy dữ liệu > tiếng việt
        + Code
            * collect_urls.py -> Lấy các link bài báo
            * DetailsLink.py -> Từ link lấy thông tin chi tiết
            * read_excel.py -> Đọc file excel và lưu vào file csv(thông tin thu thập github)
        + Urls_Fake: Url link bài viết
        + Details_Fake: 
            * Chi tiết các url đã lấy được các thông tin
            * Data csv lấy được từ github
    - DataReal: Các file csv đã thu thập được: các đường link, chi tiết bài báo, dữ liệu github, code để lấy dữ liệu > tiếng anh
        + Code
            * collect_urls.py -> Lấy các link bài báo
            * details_link.py -> Từ link lấy thông tin chi tiết
            * updateUrls_begin_zero.py -> Đánh dấu link đã xử lý( cập nhật trạng thái xem đã lấy dữ liệu ở link chưa)
        + Urls_Real: Url link bài viết
        + Details_Real: 
            * Chi tiết các url đã lấy được các thông tin
            * Data csv lấy được từ github

**Data_Train: Dữ liệu để train cho demo để xây dựng mô hình**
**Data_Test: Dữ liệu để test cho demo sau khi xây dựng mô hình**
**Process_Data_Train: Chuẩn hóa dữ liệu trước khi train và tách dữ liệu lưu vào Data_Train và Data_Test**
    - Merge_Data: Hợp nhất data để xây dựng mô hình
    - Subtract_Data_English: Lựa chọn 19600 của tin thật và giả tiếng anh > lựa chọn 3 trường để lưu lại vào dataEnglish/Train_English
        + Random_Data.py: Tách data để thực hiện train và test
**Demo:**
        + Xây dựng nhiều mô hình thuật toán khác nhau
        + Code demo sau khi xây dựng và lưu model
**Evaluate: Tính toán các độ đo PPV, TPR, ACC, F1, FPR, FNR**
** Model: Lưu trữ các model ban đầu **
**Predict: Lưu trữ dự đoán thực thế sau khi xây dựng**
**AppDetection:**
    - Phát hiện tin giả: bằng tiếng anh và tiếng việt 
    - Những thuật toán cuối cùng lựa chọn
**Vector: Lưu trữ vector hóa ngôn ngữ**

# 4, Thu thập dữ liệu
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

# 5, Xây dựng mô hình
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

