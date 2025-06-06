# Bài tập: Tìm ký tự xuất hiện nhiều nhất trong một chuỗi
def tim_ky_tu_xuat_hien_nhieu_nhat(chuoi):
    # Tạo từ điển để đếm số lần xuất hiện của mỗi ký tự
    dem = {}
    
    # Đếm số lần xuất hiện của từng ký tự
    for ky_tu in chuoi:
        if ky_tu in dem:
            dem[ky_tu] += 1
        else:
            dem[ky_tu] = 1
    
    # Tìm ký tự có số lần xuất hiện nhiều nhất
    ky_tu_nhieu_nhat = max(dem, key=dem.get)
    so_lan_xuat_hien = dem[ky_tu_nhieu_nhat]
    
    return ky_tu_nhieu_nhat, so_lan_xuat_hien

# Chương trình chính
chuoi_nhap = "Toi, la, nguoi, Viet, Nam,"
ky_tu, so_lan = tim_ky_tu_xuat_hien_nhieu_nhat(chuoi_nhap)

print(f"Chuỗi ban đầu: {chuoi_nhap}")
print(f"Ký tự '{ky_tu}' xuất hiện nhiều nhất với {so_lan} lần")