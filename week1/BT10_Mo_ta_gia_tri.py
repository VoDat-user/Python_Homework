def doc_so_mot_chu_so(n):
    """Đọc số có một chữ số"""
    chu_so = ['không', 'một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín']
    return chu_so[n]

def doc_so_ba_chu_so(n):
    """
    Chuyển số có 3 chữ số thành chữ
    
    Args:
        n: số nguyên có 3 chữ số (100-999)
    Returns:
        str: Chuỗi mô tả số đó bằng chữ
    """
    if not (100 <= n <= 999):
        return "Số không hợp lệ. Vui lòng nhập số có 3 chữ số!"
    
    # Tách các chữ số
    tram = n // 100
    chuc = (n % 100) // 10
    donvi = n % 10
    
    ket_qua = doc_so_mot_chu_so(tram) + " trăm"
    
    if chuc == 0:
        if donvi != 0:
            ket_qua += " lẻ " + doc_so_mot_chu_so(donvi)
    else:
        if chuc == 1:
            ket_qua += " mười"
        else:
            ket_qua += " " + doc_so_mot_chu_so(chuc) + " mươi"
            
        if donvi == 1:
            ket_qua += " mốt"
        elif donvi == 5:
            ket_qua += " lăm"
        elif donvi != 0:
            ket_qua += " " + doc_so_mot_chu_so(donvi)
    
    return ket_qua

# Chương trình chính
if __name__ == "__main__":
    while True:
        try:
            so = int(input("Nhập số có 3 chữ số (100-999): "))
            ket_qua = doc_so_ba_chu_so(so)
            print(f"Kết quả: {ket_qua}")
            break
        except ValueError:
            print("Vui lòng nhập một số nguyên!")

    # Test một số trường hợp
    test_cases = [123, 205, 350, 401, 515, 600, 999]
    print("\nCác trường hợp test:")
    for test in test_cases:
        print(f"{test}: {doc_so_ba_chu_so(test)}")