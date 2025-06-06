#Student Database Management
#Tạo một DataFrame tên là df_students chứa thông tin của 10 sinh viên.
import pandas as pd

#df_students 
df_students = pd.DataFrame({
    # Tên sinh viên 
    'Name_Student': ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 
             'Frank', 'Grace', 'Hannah', 'Ian', 'Jack'],
    # Tuổi sinh viên
    'Age_Student': [20, 21, 22, 23, 20, 21, 22, 23, 20, 21],
    #Giới tính 
    'Gender_Student': ['F', 'M', 'M', 'M', 'F', 
               'M', 'F', 'F', 'M', 'M'],
    #`Điểm tổng kết `
    'Score_Student': [3.5, 3.8, 3.2, 3.9, 3.6, 
                      3.7, 3.4, 3.1, 3.0, 3.3]
})

"""
Yêu cầu: Hiển thị:
1.Toàn bộ dữ liệu của bảng
2.3 dòng đầu tiên
3.Theo index=2 và cột Name
4.Theo index=10 và cột Age
5.Các cột Name và Score
6.Thêm một cột tên Pass với giá trị True nếu giá trị cột Score >= 5, ngược lại là False.
7.Sắp xếp danh sách sinh viên theo điểm Score giảm dần.
"""

# 1. Hiển thị toàn bộ dữ liệu của bảng
print("Toàn bộ dữ liệu của bảng df_students:")
print(df_students)
print("__" * 50)

# 2. Hiển thị 3 dòng đầu tiên
print("\n 3 dòng đầu tiên của df_students:")
print(df_students.head(3)) 
print("__" * 50)

# 3. Hiển thị theo index=2 và cột Name
print("\n Theo index=2 và cột Name:")
print(df_students.loc[2, 'Name_Student'])
print("__" * 50)

# 4. Hiển thị theo index=10 và cột Age
print("\n Theo index=10 và cột Age:")
print(df_students.loc[9, 'Age_Student'])  # Chú ý: index bắt đầu từ 0, nên index=10 là dòng thứ 11
print("__" * 50)

# 5. Hiển thị các cột Name và Score
print("\n Các cột Name và Score:")
print(df_students[['Name_Student', 'Score_Student']])
print("__" * 50)

# 6. Thêm một cột tên Pass với giá trị True nếu giá trị cột Score >= 5, ngược lại là False
df_students['Pass'] = df_students['Score_Student'] >= 5
print("\n Thêm cột Pass:")
print(df_students)
print("__" * 50)

# 7. Sắp xếp danh sách sinh viên theo điểm Score giảm dần
df_students.sort_values(by=['Score_Student'], ascending=False, inplace=True)
print("\n Danh sách sinh viên theo điểm Score giảm dần:")
print(df_students)
print("__" * 50)