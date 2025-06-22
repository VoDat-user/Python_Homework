def tach_so_tu_chuoi(chuoi):

    so_trong_chuoi = []
    for ky_tu in chuoi:
        if ky_tu.isdigit():
            so_trong_chuoi.append(int(ky_tu))
    return so_trong_chuoi

# Ví dụ sử dụng
chuoi_test = "abc123def456ghi7"
mang_so = tach_so_tu_chuoi(chuoi_test)

if mang_so:
    print(f"Các số trong chuỗi '{chuoi_test}' là: {mang_so}")
else:
    print(f"Không tìm thấy số trong chuỗi '{chuoi_test}'")

chuoi_test2 = "abcdef"
mang_so2 = tach_so_tu_chuoi(chuoi_test2)

if mang_so2:
    print(f"Các số trong chuỗi '{chuoi_test2}' là: {mang_so2}")
else:
    print(f"Không tìm thấy số trong chuỗi '{chuoi_test2}'")