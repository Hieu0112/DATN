import csv
input_csv_file = 'dataReal/Urls1.csv'

def reset_processed_field(csv_file):
    # Đọc dữ liệu từ tệp CSV
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)  # Đọc tất cả các hàng vào danh sách

    # Cập nhật giá trị của trường 'Processed' từ 1 về 0
    for row in rows:
        if row['Processed'] == '1':
            row['Processed'] = '0'

    # Ghi lại dữ liệu đã cập nhật vào tệp CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Đã cập nhật trường 'Processed' từ 1 về 0 trong tệp {csv_file}.")

if __name__ == '__main__':
    reset_processed_field(input_csv_file)
