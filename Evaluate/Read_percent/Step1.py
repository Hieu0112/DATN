import os
import pandas as pd

# Đường dẫn đến thư mục chứa các file CSV
# directory_path = "Evaluate/Vietnamese"  # Thay bằng đường dẫn thực tế
directory_path = "Evaluate/English"
# Lấy danh sách tất cả các file CSV trong thư mục
csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv') and 'step2' not in f]

# Định nghĩa thứ tự sắp xếp
order = ['Accuracy (ACC)', 'Precision (PPV)', 'Recall (TPR)', 'F1-Score', 
         'False Positive Rate (FPR)', 'False Negative Rate (FNR)']

# Xử lý và in nội dung từng file
for file in csv_files:
    file_path = os.path.join(directory_path, file)
    print(f"Contents of {file}:")
    
    # Đọc file CSV
    df = pd.read_csv(file_path)
    
    name='evaluation_metrics'
    name='evaluation metrics'
    # Sắp xếp lại cột evaluation_metrics theo thứ tự
    df[name] = pd.Categorical(df[name], categories=order, ordered=True)
    df_sorted = df.sort_values(name)
    
    # Nhân giá trị cột Value với 100 và làm tròn 2 chữ số
    df_sorted['Value'] = (df_sorted['Value'] * 100).round(2)
    
    # In kết quả
    for _, row in df_sorted.iterrows():
        print(f"{row[name]}: {row['Value']}")
    print("\n" + "-" * 50 + "\n")  # Ngăn cách giữa các file
