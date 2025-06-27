import pandas as pd

# DataFrame tên là df_students chứa thông tin của 10 sinh viên
data = {
    "Name": ["Vo Thanh Dat", "Kieu Phuoc Vinh", "Tran Nguyen Tien Dung", 
             "Nguyen Van A", "Nguyen Van A", "Nguyen Van B", "Nguyen Van C", 
             "Nguyen Van D", "Nguyen Van E", "Nguyen Van F"],

    "Age": [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],

    "Gender": ["Male", "Male", "Male", "Female", "Male", 
               "Female", "Male", "Female", "Male", "Female"],

    "Score": [9.0, 8.5, 7.5, 6.0, 4.5, 8.0, 7.0, 6.5, 9.2, 3.8]  
}

# Tạo DataFrame từ dictionary
df_students = pd.DataFrame(data)

# Hiển thị toàn bộ dữ liệu
print("DataFrame of students:")
print(df_students)

# Hiển thị 3 dòng đầu tiên
print("First 3 rows of the DataFrame:")
print(df_students.head(3))

# Theo index=2 và cột Name:
print("\nName at index 2:")
print(df_students.at[2, 'Name'])

#Theo index=10 và cột Age:
print("\nAge at 10th student:")
print(df_students.loc[9, 'Age'])  # Chú ý rằng index bắt đầu từ 0, nên index=10 là 9

#Các cột Name và Score
print("\nName and Score columns:")
print(df_students[['Name', 'Score']])

#Thêm một cột tên Pass với giá trị True nếu giá trị cột Score >= 5, ngược lại là False.

print("\nDataFrame with Pass column:")
df_students['Pass'] = df_students['Score'] >= 5
print(df_students) 

#Sắp xếp danh sách sinh viên theo điểm Score giảm dần.
print("\nDataFrame sorted by Score in descending order:")
df_sorted = df_students.sort_values(by='Score', ascending=False)
print(df_sorted)