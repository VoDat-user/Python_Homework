import os
import time
import pandas as pd
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import glob

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
        df = pd.read_excel(
            INPUT_FILE,
            dtype={'Mã số thuế': str, 'Mã tra cứu': str}
        )
        df.columns = [col.strip() for col in df.columns]
        df = df.rename(columns={
            'Mã số thuế': 'MST',
            'Mã tra cứu': 'MaTraCuu',
            'URL': 'URL'
        })
        # Đảm bảo các trường MST và MaTraCuu là chuỗi, loại bỏ .0 nếu có
        df['MST'] = df['MST'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
        df['MaTraCuu'] = df['MaTraCuu'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
        logging.info("Đọc toàn bộ input thành công.")
        return df
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
            "directory_upgrade": True,
            "safebrowsing.enabled": True,
            "safebrowsing.disable_download_protection": True
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
        time.sleep(5)  # tăng thời gian chờ

        try:
            # Sửa selector cho đúng nút "Tải XML"
            download_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Tải XML')]")
            if download_button:
                download_button.click()
                logging.info(f"Đã click nút tải XML cho: {mst} | {matra}")
                print(f"Đã click nút tải XML cho: {mst} | {matra}")
                return True
        except Exception as e:
            logging.warning(f"Không tìm thấy nút tải XML: {e}")
            print(f"Không tìm thấy nút tải XML cho: {mst} | {matra} | {driver.current_url}")
            return False
    except Exception as e:
        logging.warning(f"Lỗi tra cứu FPT với {mst} | {matra}: {e}")
        print(f"Lỗi tra cứu FPT với {mst} | {matra}: {e}")
        return False
    return False

# Tra cứu MeInvoice
def tra_cuu_meinvoice(driver, mst, matra):
    try:
        driver.get("https://www.meinvoice.vn/tra-cuu/")
        time.sleep(2)
        driver.find_element(By.NAME, "txtCode").clear()
        driver.find_element(By.NAME, "txtCode").send_keys(matra)
        driver.find_element(By.ID, "btnSearchInvoice").click()
        time.sleep(3)
        try:
            # Bước 1: Click nút "Tải hóa đơn" để hiện menu
            btn_download = driver.find_element(By.CSS_SELECTOR, "span.download-invoice")
            btn_download.click()
            time.sleep(1)  # Đợi menu xổ ra

            # Bước 2: Click nút "Tải hóa đơn dạng XML"
            download_button = driver.find_element(By.CSS_SELECTOR, "div.dm-item.xml.txt-download-xml")
            if download_button:
                download_button.click()
                logging.info(f"Đã click nút tải XML cho mã tra cứu: {matra}")
                print(f"Đã click nút tải XML cho mã tra cứu: {matra}")
                return True
        except Exception as e:
            logging.warning(f"Không tìm thấy nút tải XML trên meinvoice.vn: {e}")
            print(f"Không tìm thấy nút tải XML trên meinvoice.vn cho: {matra} | {driver.current_url}")
            return False
    except Exception as e:
        logging.warning(f"Lỗi tra cứu MeInvoice với {mst} | {matra}: {e}")
        print(f"Lỗi tra cứu MeInvoice với {mst} | {matra}: {e}")
        return False
    return False

# Tra cứu VNEHoadon
def tra_cuu_vanehoadon(driver, mst, matra):
    try:
        url = f"https://van.ehoadon.vn/TCHD?MTC={matra}"
        driver.get(url)
        time.sleep(3)
        try:
            btn_download = driver.find_element(By.ID, "btnDownload")
            btn_download.click()
            try:
                download_button = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.ID, "LinkDownXML"))
                )
                download_button.click()
                logging.info(f"Đã click nút tải XML cho mã tra cứu: {matra}")
                print(f"Đã click nút tải XML cho mã tra cứu: {matra}")
                return True
            except Exception:
                logging.warning("Không tìm thấy nút LinkDownXML sau khi mở menu.")
                print(f"Không tìm thấy nút tải XML trên van.ehoadon.vn cho: {matra} | {driver.current_url}")
                return False
        except Exception as e:
            logging.warning(f"Không tìm thấy nút tải XML trên van.ehoadon.vn: {e}")
            print(f"Không tìm thấy nút tải XML trên van.ehoadon.vn cho: {matra} | {driver.current_url}")
            return False
    except Exception as e:
        logging.warning(f"Lỗi tra cứu van.ehoadon.vn với mã tra cứu {matra}: {e}")
        print(f"Lỗi tra cứu van.ehoadon.vn với mã tra cứu {matra}: {e}")
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
        data = {}
        # Lấy thông tin hóa đơn
        dlhdon = root.find('.//DLHDon')
        if dlhdon is not None:
            ttchung = dlhdon.find('TTChung')
            if ttchung is not None:
                data['SoHoaDon'] = ttchung.findtext('SHDon', default='')
            ndhdon = dlhdon.find('NDHDon')
            if ndhdon is not None:
                nban = ndhdon.find('NBan')
                if nban is not None:
                    data['DonViBanHang'] = nban.findtext('Ten', default='')
                    data['MST_Ban'] = nban.findtext('MST', default='')
                    data['DiaChiBan'] = nban.findtext('DChi', default='')
                    data['STK_Ban'] = nban.findtext('STKNHang', default='')
                nmua = ndhdon.find('NMua')
                if nmua is not None:
                    data['NguoiMua'] = nmua.findtext('Ten', default='')
                    data['DiaChiMua'] = nmua.findtext('DChi', default='')
                    data['MST_Mua'] = nmua.findtext('MST', default='')
        return data
    except Exception as e:
        logging.error(f"Lỗi đọc XML {file_path}: {e}")
        return {}

def wait_for_xml_file(download_dir, timeout=30):
    """Chờ file XML xuất hiện và hoàn tất tải về."""
    waited = 0
    while waited < timeout:
        xml_files = glob.glob(os.path.join(download_dir, "*.xml"))
        downloading = glob.glob(os.path.join(download_dir, "*.crdownload"))
        if xml_files and not downloading:
            return xml_files[0]
        time.sleep(1)
        waited += 1
    return None

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
            success = False

            if not url or pd.isna(url):
                logging.warning(f"URL trống hoặc không hợp lệ cho MST: {mst}")
            elif "tracuuhoadon.fpt.com.vn" in url:
                try:
                    success = tra_cuu_fpt(driver, mst, matra)
                except Exception as e:
                    logging.error(f"Lỗi khi tra cứu FPT: {e}")
            elif "meinvoice.vn" in url:
                try:
                    success = tra_cuu_meinvoice(driver, mst, matra)
                except Exception as e:
                    logging.error(f"Lỗi khi tra cứu meinvoice.vn: {e}")
            elif "van.ehoadon.vn" in url:
                try:
                    success = tra_cuu_vanehoadon(driver, mst, matra)
                except Exception as e:
                    logging.error(f"Lỗi khi tra cứu van.ehoadon.vn: {e}")
            else:
                logging.warning(f"URL không được hỗ trợ: {url}")

            time.sleep(2)

            if success:
                xml_path = wait_for_xml_file(DOWNLOAD_DIR, timeout=30)
                if xml_path:
                    parsed = parse_xml(xml_path)
                    parsed.update({'MST': mst, 'MaTraCuu': matra, 'Status': 'OK', 'URL': url})
                    output_data.append(parsed)
                    # os.remove(xml_path)  # <-- Bỏ hoặc comment dòng này để giữ lại file XML
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
