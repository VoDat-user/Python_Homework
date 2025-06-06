def viet_hoa_chu_dau_moi_tu(chuoi):
    """
    Chuyển đổi ký tự đầu tiên của mỗi từ trong chuỗi thành chữ in hoa.

    Args:
        chuoi: Chuỗi đầu vào.

    Returns:
        Chuỗi với ký tự đầu của mỗi từ được viết hoa.
    """
    # Tách chuỗi thành các từ
    cac_tu = chuoi.split()
    
    # Xử lý từng từ
    for i in range(len(cac_tu)):
        if cac_tu[i]:  # Kiểm tra từ không rỗng
            cac_tu[i] = cac_tu[i][0].upper() + cac_tu[i][1:]
    
    # Nối các từ lại thành chuỗi
    return ' '.join(cac_tu)

# Chương trình chính
if __name__ == "__main__":
    # Test với input từ người dùng
    chuoi_nhap = input("Nhập chuỗi của bạn: ")
    ket_qua = viet_hoa_chu_dau_moi_tu(chuoi_nhap)
    print(f"Kết quả: {ket_qua}")
    
    # Test các trường hợp
    test_cases = [
        "hello world!", 
        "python programming language",
        "viet nam dat nuoc toi",
        "mot hai ba bon"
    ]
    
    print("\nCác trường hợp test:")
    for test in test_cases:
        print(f"Input:  '{test}'")
        print(f"Output: '{viet_hoa_chu_dau_moi_tu(test)}'")
        print("-" * 40)