import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def cat_ho_ten(hoten):
    
    slist = hoten.split()
    n = len(slist)
    
    if n == 0:
        return "", ""
    elif n == 1:
        return "", slist[0]  # Chỉ có tên
    else:
        ho = slist[0]  # Từ đầu tiên là họ
        ten = slist[n-1]  # Từ cuối cùng là tên
        
        if n > 2:
            dem = " ".join(slist[1:n-1])  # Các từ giữa là tên đệm
            ho_lot = ho + " " + dem
        else:
            ho_lot = ho  # Chỉ có họ và tên
            
        return ho_lot, ten

# Test hàm
def test_cat_ho_ten():
    test_cases = [
        "Nguyễn Thùy Trang",
        "Lê Văn Nam", 
        "Trần Thị Hồng Nhung",
        "Vũ Minh",
        "Hoàng"
    ]
    
    for hoten in test_cases:
        ho_lot, ten = cat_ho_ten(hoten)
        print(f"Họ tên: {hoten}")
        print(f"Họ lót: {ho_lot}")
        print(f"Tên: {ten}")
        print("-" * 30)

# Chạy test
if __name__ == "__main__":
    # Nhập từ người dùng như trong ảnh
    hoten = input("Nhập họ tên đầy đủ của bạn: ")
    ho_lot, ten = cat_ho_ten(hoten)
    
    print(f"Tên của bạn là: {ten}")
    print(f"Họ của bạn là: {ho_lot}")
    
    print("\nTest với các trường hợp khác:")
    test_cat_ho_ten()