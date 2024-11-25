import pandas as pd
import os

# Đọc file CSV
file_viet = os.path.abspath("AppDetection/App/Check_Vietnamese.csv")
file_anh = os.path.abspath("AppDetection/App/Check_English.csv")

def Predict_real(path,real,pre):
    df = pd.read_csv(path)
    count_label = df[df['label'] == real].shape[0]
    filtered_data = df[((df['label'] == real) & (df['Prediction'] == pre))]
    print("Số dự đoán sai là: "+ str(len(filtered_data)) +"/"+str(count_label))
    print("Phần trăm: "+ str(1-len(filtered_data)/count_label))
    # print(filtered_data)

print("Dự đoán tiếng việt trong thực tế tin thật thành giả là: ")
Predict_real(file_viet,0,1)
print("Dự đoán tiếng việt trong thực tế tin giả thành thật là: ")
Predict_real(file_viet,1,0)

print('----------------')

print("Dự đoán tiếng anh trong thực tế tin thật thành giả là: ")
Predict_real(file_anh,0,1)
print("Dự đoán tiếng anh trong thực tế tin giả thành thật là: ")
Predict_real(file_anh,1,0)