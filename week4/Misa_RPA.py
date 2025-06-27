from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def doc_ma_hoa_don_tu_file_txt(duong_dan_file):
    with open(duong_dan_file, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def mo_trinh_duyet():
    # Đảm bảo thư mục tải về tồn tại
    download_dir = r"D:\Download_AnyAny\HOADON_DOWNLOAD"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    tuy_chon = Options()
    tuy_chon_download = {
        "plugins.always_open_pdf_externally": True,
        "download.default_directory": download_dir,
        "download.prompt_for_download": False
    }
    tuy_chon.add_experimental_option("prefs", tuy_chon_download)
    tuy_chon.add_argument("--disable-notifications")
    # Khởi tạo ChromeDriver
    dich_vu = ChromeService(ChromeDriverManager().install())
    trinh_duyet = webdriver.Chrome(service=dich_vu, options=tuy_chon)
    return trinh_duyet

def nhap_ma_tra_cuu(trinh_duyet, ma_hoa_don):
    trinh_duyet.get("https://www.meinvoice.vn/tra-cuu")
    trinh_duyet.implicitly_wait(10)
    o_ma = trinh_duyet.find_element(By.NAME, "txtCode")
    o_ma.clear()
    o_ma.send_keys(ma_hoa_don)

def thuc_hien_tim_kiem(trinh_duyet):
    trinh_duyet.implicitly_wait(10)
    nut_tim_kiem = trinh_duyet.find_element(By.ID, "btnSearchInvoice")
    nut_tim_kiem.click()

def xu_ly_ket_qua(trinh_duyet):
    time.sleep(2)
    if "Thông tin hóa đơn" in trinh_duyet.page_source:
        print("Hóa đơn tồn tại")
        return True
    else:
        print("Không tìm thấy hóa đơn hoặc mã không hợp lệ")
        return False

def tai_hoa_don_pdf(trinh_duyet):
    trinh_duyet.implicitly_wait(10)
    try:
        iframe = trinh_duyet.find_element(By.ID, "frmResult")
        duong_dan_pdf = iframe.get_attribute("src")
        print("Link PDF:", duong_dan_pdf)
        trinh_duyet.get(duong_dan_pdf)
        time.sleep(5)
    except Exception as e:
        print("Lỗi khi tải hóa đơn PDF:", e)

def main():
    try:
        danh_sach_ma = doc_ma_hoa_don_tu_file_txt("D:/SVTT/week4-5/ma_hoa_don.txt")
    except Exception as e:
        print("Không đọc được file mã hóa đơn:", e)
        return

    trinh_duyet = mo_trinh_duyet()
    for ma_hoa_don in danh_sach_ma:
        print(f"Đang xử lý mã hóa đơn: {ma_hoa_don}")
        try:
            nhap_ma_tra_cuu(trinh_duyet, ma_hoa_don)
            thuc_hien_tim_kiem(trinh_duyet)
            if xu_ly_ket_qua(trinh_duyet):
                tai_hoa_don_pdf(trinh_duyet)
                print(f"Tải hóa đơn {ma_hoa_don} thành công.")
            else:
                print(f"Không thể tải hóa đơn {ma_hoa_don}.")
        except Exception as e:
            print(f"Lỗi khi xử lý mã {ma_hoa_don}:", e)
        time.sleep(2)
    trinh_duyet.quit()

if __name__ == "__main__":
    main()