# import pandas as pd

# # Tạo DataFrame với dữ liệu tiếng Việt
# data = {'title': ['Chào bạn', 'Python là ngôn ngữ tuyệt vời', 'Học data science rất thú vị']}
# data_df = pd.DataFrame(data)

# # Tính tổng số từ trong cột 'title'
# total_words = data_df['title'].str.split().map(len).sum()

# print("Tổng số từ trong cột 'title':", total_words)



import pandas as pd

# Tạo DataFrame với dữ liệu ví dụ
data = {'text': ['Chào bạn', 'Python là ngôn ngữ tuyệt vời', 'Học data science rất thú vị']}
data_df = pd.DataFrame(data)

# Tính trung bình số từ trong cột 'text'
avg_text = data_df['text'].str.split().map(len).mean()

print("Trung bình số từ trong cột 'text':", avg_text)
