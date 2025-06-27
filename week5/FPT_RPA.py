import os
import time
import pandas as pd
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import logging

# Cấu hình logging
logging.basicConfig(
    filename='fpt_rpa.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Đảm bảo lấy đúng thư mục chứa script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(SCRIPT_DIR, "Downloads")
INPUT_FILE = os.path.join(SCRIPT_DIR, "input.xlsx")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "output.xlsx")

# Tạo thư mục Downloads nếu chưa có
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Đọc và chuẩn hóa file input
def read_input():
    try:
        df = pd.read_excel(INPUT_FILE)
        df.columns = [col.strip() for col in df.columns]
        df = df.rename(columns={
            'Mã số thuế': 'MST',
            'Mã tra cứu': 'MaTraCuu',
            'URL': 'URL'
        })
        # Loại bỏ dòng không hợp lệ
        df = df.dropna(subset=['MST', 'MaTraCuu', 'URL'])
        df = df[~df['MaTraCuu'].astype(str).str.contains("không tìm thấy", case=False)]
        logging.info("Đọc và chuẩn hóa input thành công.")
        return df[['MST', 'MaTraCuu', 'URL']]
    except Exception as e:
        logging.error(f"Lỗi đọc file input: {e}")
        raise

# Khởi tạo trình duyệt
def setup_driver(download_path):
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": download_path,
            "download.prompt_for_download": False,
            "directory_upgrade": True
        })
        # chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=chrome_options)
        logging.info("Khởi tạo trình duyệt thành công.")
        return driver
    except Exception as e:
        logging.error(f"Lỗi khởi tạo trình duyệt: {e}")
        raise

# Tra cứu FPT
def tra_cuu_fpt(driver, mst, matra):
    try:
        driver.get("https://tracuuhoadon.fpt.com.vn/search.html")
        time.sleep(2)
        driver.find_element(By.XPATH, '//input[@placeholder="MST bên bán"]').send_keys(mst)
        driver.find_element(By.XPATH, '//input[@placeholder="Mã tra cứu hóa đơn"]').send_keys(matra)
        driver.find_element(By.XPATH, '//button[contains(text(), "Tra cứu")]').click()
        time.sleep(3)
        # Thử tìm nút tải XML
        try:
            download_button = driver.find_element(By.XPATH, "//a[contains(@href,'.xml')]")
            if download_button:
                download_button.click()
                logging.info(f"Đã click nút tải XML cho: {mst} | {matra}")
                return True
        except Exception as e:
            logging.warning(f"Không tìm thấy nút tải XML: {e}")
            return False
        logging.info(f"Tra cứu FPT thành công: {mst} | {matra}")
    except Exception as e:
        logging.warning(f"Lỗi tra cứu FPT với {mst} | {matra}: {e}")
        return False
    return False

# Lấy file XML mới nhất
def get_latest_xml_file(path):
    try:
        files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.xml')]
        if not files:
            return None
        return max(files, key=os.path.getctime)
    except Exception as e:
        logging.error(f"Lỗi lấy file XML mới nhất: {e}")
        return None

# Trích xuất dữ liệu từ XML
def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        ns = {'ns': root.tag.split('}')[0].strip('{')}
        data = {
            'SoHoaDon': root.findtext('.//ns:SoHoaDon', default='', namespaces=ns),
            'DonViBanHang': root.findtext('.//ns:TenDonVi', default='', namespaces=ns),
            'MST_Ban': root.findtext('.//ns:MSTDonVi', default='', namespaces=ns),
            'DiaChiBan': root.findtext('.//ns:DiaChiDonVi', default='', namespaces=ns),
            'STK_Ban': root.findtext('.//ns:SoTaiKhoan', default='', namespaces=ns),
            'NguoiMua': root.findtext('.//ns:TenNguoiMua', default='', namespaces=ns),
            'DiaChiMua': root.findtext('.//ns:DiaChiNguoiMua', default='', namespaces=ns),
            'MST_Mua': root.findtext('.//ns:MSTNguoiMua', default='', namespaces=ns)
        }
        logging.info(f"Đọc file XML thành công: {file_path}")
        return data
    except Exception as e:
        logging.error(f"Lỗi đọc XML {file_path}: {e}")
        return {}

# Chương trình chính
def main():
    try:
        input_data = read_input()
    except Exception:
        logging.critical("Dừng chương trình do lỗi đọc input.")
        return

    try:
        driver = setup_driver(DOWNLOAD_DIR)
    except Exception:
        logging.critical("Dừng chương trình do lỗi khởi tạo trình duyệt.")
        return

    output_data = []

    try:
        for idx, row in input_data.iterrows():
            mst = str(row['MST'])
            matra = str(row['MaTraCuu'])
            url = str(row['URL']).lower()

            logging.info(f"Đang tra cứu: {mst} | {matra} | {url}")

            if "tracuuhoadon.fpt.com.vn" in url:
                success = tra_cuu_fpt(driver, mst, matra)
            else:
                logging.warning(f"URL không hỗ trợ: {url}")
                success = False

            time.sleep(2)

            if success:
                time.sleep(10)  # tăng thời gian chờ tải file
                xml_path = get_latest_xml_file(DOWNLOAD_DIR)
                if xml_path:
                    parsed = parse_xml(xml_path)
                    parsed.update({'MST': mst, 'MaTraCuu': matra, 'Status': 'OK', 'URL': url})
                    output_data.append(parsed)
                    try:
                        os.remove(xml_path)
                    except Exception as e:
                        logging.warning(f"Không xóa được file XML {xml_path}: {e}")
                else:
                    logging.warning("Không tìm thấy file XML.")
                    output_data.append({'MST': mst, 'MaTraCuu': matra, 'Status': 'Fail', 'URL': url})
            else:
                output_data.append({'MST': mst, 'MaTraCuu': matra, 'Status': 'Fail', 'URL': url})
    finally:
        driver.quit()

    try:
        df_out = pd.DataFrame(output_data)
        df_out.to_excel(OUTPUT_FILE, index=False)
        logging.info("Xuất file output hoàn tất.")
    except Exception as e:
        logging.error(f"Lỗi ghi file output: {e}")

if __name__ == "__main__":
    main()
