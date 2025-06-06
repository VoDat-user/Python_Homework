# Mục tiêu: Đảm bảo dữ liệu đầu vào hợp lệ
# Cách làm:
# - Kiểm tra có phải số nguyên không
# - Kiểm tra a < b
# - Xử lý ngoại lệ khi nhập sai

# B2: Tư duy: Số chính phương = n² (với n là số nguyên)
# Cách kiểm tra:
# - Tính căn bậc 2 của số đó
# - Kiểm tra xem căn bậc 2 có phải số nguyên không
# - Nếu sqrt(x) * sqrt(x) = x → là số chính phương

# B3: Tư duy: Sử dụng phép chia dư
# Cách kiểm tra:
# - Nếu số % 3 == 0 → chia hết cho 3

#B4: Duyệt từ a đến b:
#   Với mỗi số i:
#     Nếu i chia hết cho 3:
#       Nếu i không phải số chính phương:
#         Thêm i vào danh sách kết quả

# B5: Mục tiêu: In các số cách nhau bằng dấu phẩy
# Cách làm:
# - Nối các số thành chuỗi
# - Sử dụng dấu phẩy làm ký tự phân cách
def is_perfect_square(x):
    if x < 0:
        return False
    root = int(x**0.5)
    return root * root == x

def is_valid_input(a, b):
    if not isinstance(a, int) or not isinstance(b, int):
        raise ValueError("Input must be integers.")
    if a >= b:
        raise ValueError("a must be less than b.")
    return True

def find_non_perfect_square_multiples_of_3(a, b):
    """
    Tìm và trả về chuỗi các số chia hết cho 3 và không phải số chính phương
    trong khoảng [a,b], các số cách nhau bởi dấu phẩy
    """
    if not is_valid_input(a, b):
        return ""

    result = []
    for i in range(a, b + 1):
        if i % 3 == 0 and not is_perfect_square(i):
            result.append(str(i))
    
    return ", ".join(result)  # Nối các số bằng dấu phẩy

# Chương trình chính để test
if __name__ == "__main__":
    try:
        # Nhập dữ liệu
        a = int(input("Nhập số a: "))
        b = int(input("Nhập số b: "))
        
        # Lấy và in kết quả
        ket_qua = find_non_perfect_square_multiples_of_3(a, b)
        if ket_qua:
            print(f"Kết quả: {ket_qua}")
        else:
            print("Không có số thỏa mãn!")
            
    except ValueError as e:
        print(f"Lỗi: {str(e)}")