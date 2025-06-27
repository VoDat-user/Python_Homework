class NhanVien:
    def __init__(self, ma_nv, ho_ten, tuoi, phong_ban, luong):
        self.ma_nv = ma_nv
        self.ho_ten = ho_ten
        self.tuoi = tuoi
        self.phong_ban = phong_ban
        self.luong = luong

    def tinh_thuc_nhan(self):
        # Lương thực nhận sau thuế 10%
        return self.luong * 0.9

    def thong_tin(self):
        return f"Mã NV: {self.ma_nv}, Họ tên: {self.ho_ten}, Tuổi: {self.tuoi}, Phòng: {self.phong_ban}, Lương thực nhận: {self.tinh_thuc_nhan()}"

# Tạo đối tượng nhân viên
nv1 = NhanVien(101, "Nguyễn Văn An", 28, "IT", 800)
nv2 = NhanVien(102, "Trần Thị Bình", 25, "HR", 700)

# In thông tin nhân viên
print(nv1.thong_tin())
print(nv2.thong_tin())