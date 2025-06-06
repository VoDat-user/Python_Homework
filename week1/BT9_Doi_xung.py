def kiem_tra_doi_xung(chuoi):
    """
    Kiểm tra xem chuỗi có đối xứng không.
    
    Args:
        chuoi: Chuỗi cần kiểm tra
        
    Returns:
        bool: True nếu chuỗi đối xứng, False nếu không
    """
    # Loại bỏ khoảng trắng và chuyển về chữ thường
    chuoi = chuoi.lower().replace(" ", "")
    
    # So sánh chuỗi với chuỗi đảo ngược
    return chuoi == chuoi[::-1]

# Chương trình chính
if __name__ == "__main__":
    # Test với input từ người dùng
    chuoi_nhap = input("Nhập chuỗi cần kiểm tra: ")
    if kiem_tra_doi_xung(chuoi_nhap):
        print("Chuỗi này là chuỗi đối xứng!")
    else:
        print("Chuỗi này không đối xứng!")
    
    # Test các trường hợp
    test_cases = [
        "radar",
        "hello",
        "A man a plan a canal Panama",
        "race a car",
        "noon",
        "12321"
    ]
    
    print("\nCác trường hợp test:")
    for test in test_cases:
        result = "đối xứng" if kiem_tra_doi_xung(test) else "không đối xứng"
        print(f"'{test}' -> {result}")
        print("-" * 40)