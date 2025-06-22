from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options

git add .def doc_ma_hoa_don_tu_file_txt(duong_dan_file):
    with open(duong_dan_file, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def mo_trinh_duyet():
    # Cấu hình selenium để tải file về thư mục ngoài dự án
    tuy_chon = Options()
    tuy_chon_download = {
        "plugins.always_open_pdf_externally": True,
        # Đổi đường dẫn tải về ra ngoài thư mục code
        "download.default_directory": r"D:\HOADON_DOWNLOAD",
        "download.prompt_for_download": False
    }
    tuy_chon.add_experimental_option("prefs", tuy_chon_download)
    tuy_chon.add_argument("--disable-notifications")
    duong_dan_chromedriver = "chromedriver.exe"
    dich_vu = ChromeService(executable_path=duong_dan_chromedriver, options=tuy_chon)
    trinh_duyet = webdriver.Chrome(service=dich_vu, options=tuy_chon)
    return trinh_duyet

def nhap_ma_tra_cuu(trinh_duyet, ma_hoa_don):
    trinh_duyet.get("https://www.meinvoice.vn/tra-cuu")
    trinh_duyet.implicitly_wait(10)
    o_ma = trinh_duyet.find_element(By.NAME, "txtCode")
    o_ma.clear()
    o_ma.send_keys(ma_hoa_don)

def thuc_hien_tim_kiem(trinh_duyet):
    time.sleep(0.1)
    trinh_duyet.implicitly_wait(10)
    nut_tim_kiem = trinh_duyet.find_element(By.ID, "btnSearchInvoice")
    nut_tim_kiem.click()

def xu_ly_ket_qua(trinh_duyet):
    if "Thông tin hóa đơn" in trinh_duyet.page_source:
        print("Hóa đơn tồn tại")
        return True
    else:
        print("Không tìm thấy hóa đơn hoặc mã không hợp lệ")
        return False

def tai_hoa_don_pdf(trinh_duyet):
    trinh_duyet.implicitly_wait(10)
    iframe = trinh_duyet.find_element(By.ID, "frmResult")
    duong_dan_pdf = iframe.get_attribute("src")
    print("Link PDF:", duong_dan_pdf)
    trinh_duyet.get(duong_dan_pdf)
    time.sleep(5)

def main():
    danh_sach_ma = doc_ma_hoa_don_tu_file_txt("ma_hoa_don.txt")
    for ma_hoa_don in danh_sach_ma:
        trinh_duyet = mo_trinh_duyet()
        try:
            nhap_ma_tra_cuu(trinh_duyet, ma_hoa_don)
            thuc_hien_tim_kiem(trinh_duyet)
            if xu_ly_ket_qua(trinh_duyet):
                tai_hoa_don_pdf(trinh_duyet)
                print(f"Tải hóa đơn {ma_hoa_don} thành công.")
            else:
                print(f"Không thể tải hóa đơn {ma_hoa_don}.")
        finally:
            trinh_duyet.quit()

if __name__ == "__main__":
    main()