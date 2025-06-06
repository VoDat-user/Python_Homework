def doi_chu_xen_ke(chuoi):
    """
    Đổi chữ xen kẽ trong chuỗi: một chữ hoa, một chữ thường.
    
    Args:
        chuoi: Chuỗi đầu vào cần xử lý
        
    Returns:
        Chuỗi đã được xử lý với ký tự xen kẽ hoa thường
    """
    ket_qua = ""
    for i in range(len(chuoi)):
        if i % 2 == 0:
            ket_qua += chuoi[i].upper()
        else:
            ket_qua += chuoi[i].lower()
    return ket_qua

# Chương trình chính
if __name__ == "__main__":
    # Test với input từ người dùng
    chuoi_nhap = input("Nhập chuỗi của bạn: ")
    ket_qua = doi_chu_xen_ke(chuoi_nhap)
    print(f"Kết quả: {ket_qua}")
    
    # Test các trường hợp
    test_cases = [
        "hello world",
        "python",
        "TESTING",
        "xin chao cac ban"
    ]
    
    print("\nCác trường hợp test:")
    for test in test_cases:
        print(f"Input:  '{test}'")
        print(f"Output: '{doi_chu_xen_ke(test)}'")
        print("-" * 40)