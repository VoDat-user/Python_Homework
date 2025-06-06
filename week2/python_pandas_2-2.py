import pandas as pd
import numpy as np

# Khởi tạo dữ liệu nhân viên
nhan_vien_data = pd.DataFrame({
    'ma_nv': [101, 102, 103, 104, 105, 106],
    'ho_ten': ['An', 'Bình', 'Cường', 'Dương', np.nan, 'Hạnh'],
    'tuoi': [25, np.nan, 30, 22, 28, 35],
    'phong_ban': ['HR', 'IT', 'IT', 'Finance', 'HR', np.nan],
    'luong': [700, 800, 750, np.nan, 710, 770]
})

print("Danh sách nhân viên:")
print(nhan_vien_data)

# Thông tin quản lý phòng ban
quan_ly_data = pd.DataFrame({
    'phong_ban': ['HR', 'IT', 'Finance', 'Marketing'],
    'truong_phong': ['Trang', 'Khoa', 'Minh', 'Lan']
})

print("Danh sách trưởng phòng:")
print(quan_ly_data)

# Kiểm tra dữ liệu thiếu
print("Kiểm tra nhân viên có dữ liệu thiếu:")
print(nhan_vien_data[nhan_vien_data.isnull().any(axis=1)])

# Xử lý dữ liệu thiếu
# Bỏ hàng có >2 giá trị null
xoa_null_df = nhan_vien_data.dropna(thresh=len(nhan_vien_data.columns) - 2)

# Điền thông tin còn thiếu
nhan_vien_data['ho_ten'] = nhan_vien_data['ho_ten'].fillna("Chưa xác định")
nhan_vien_data['tuoi'] = nhan_vien_data['tuoi'].fillna(nhan_vien_data['tuoi'].mean()).astype(int)
nhan_vien_data['luong'] = nhan_vien_data['luong'].ffill()
nhan_vien_data['phong_ban'] = nhan_vien_data['phong_ban'].fillna("Chưa phân công")

# Tính lương thực nhận (sau thuế 10%)
nhan_vien_data['thuc_nhan'] = nhan_vien_data['luong'] * 0.9

# Lọc nhân viên IT trên 25 tuổi
nv_it_df = nhan_vien_data[(nhan_vien_data['phong_ban'] == 'IT') & (nhan_vien_data['tuoi'] > 25)]
print("Nhân viên IT trên 25 tuổi:")
print(nv_it_df)

# Sắp xếp theo lương thực nhận
nhan_vien_data = nhan_vien_data.sort_values(by='thuc_nhan', ascending=False)

# Tính lương TB theo phòng ban
luong_tb_df = nhan_vien_data.groupby('phong_ban')['luong'].mean().round(2)
print("Lương trung bình từng phòng:")
print(luong_tb_df)

# Thêm thông tin trưởng phòng
nhan_vien_data = pd.merge(nhan_vien_data, quan_ly_data, on='phong_ban', how='left')

# Thêm nhân viên mới
nv_moi_data = pd.DataFrame({
    'ma_nv': [107, 108],
    'ho_ten': ['Kiên', 'Lan'],
    'tuoi': [29, 26],
    'phong_ban': ['IT', 'Marketing'],
    'luong': [800, 900]
})

nhan_vien_data = pd.concat([nhan_vien_data, nv_moi_data], ignore_index=True)
nhan_vien_data['thuc_nhan'] = nhan_vien_data['luong'] * 0.9

print("Danh sách nhân viên cập nhật:")
print(nhan_vien_data)