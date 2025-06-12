import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class CompanyDataCollector:
    """Class để thu thập dữ liệu từ website thuvienphapluat.vn"""
    
    def __init__(self):
        """Khởi tạo trình duyệt và các thiết lập cần thiết"""
        self.options = Options()
        self.options.add_argument("--disable-popup-blocking")
        self.service = Service()
        self.browser = webdriver.Chrome(service=self.service, options=self.options)
        self.wait = WebDriverWait(self.browser, 10)
        
    def collect_table_data(self):
        """Thu thập dữ liệu từ bảng trong trang hiện tại"""
        # Đợi bảng xuất hiện
        table = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table")))
        
        # Thu thập dữ liệu từ các hàng
        data = []
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Bỏ qua hàng tiêu đề
        
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 4:
                data.append({
                    "Tên doanh nghiệp": cols[1].text,
                    "Mã số thuế": cols[2].text,
                    "Ngày cấp": cols[3].text
                })
        
        return pd.DataFrame(data)
    
    def navigate_pages(self, max_pages=5):
        """Thu thập dữ liệu từ nhiều trang"""
        all_data = {}
        current_page = 1
        
        try:
            # Truy cập URL
            self.browser.get("https://thuvienphapluat.vn/ma-so-thue/tra-cuu-ma-so-thue-doanh-nghiep")
            time.sleep(2)
            
            while current_page <= max_pages:
                print(f"Đang thu thập dữ liệu trang {current_page}")
                
                # Thu thập dữ liệu trang hiện tại
                df = self.collect_table_data()
                all_data[f"Trang_{current_page}"] = df
                
                # Tìm nút next và kiểm tra có thể click không
                next_button = self.browser.find_element(By.CSS_SELECTOR, "a.next")
                if "disabled" in next_button.get_attribute("class"):
                    break
                    
                next_button.click()
                time.sleep(2)
                current_page += 1
                
        except Exception as e:
            print(f"Lỗi khi thu thập dữ liệu: {e}")
            
        finally:
            self.browser.quit()
            
        return all_data
    
    def save_to_excel(self, data, filename="company_data.xlsx"):
        """Lưu dữ liệu vào file Excel"""
        try:
            with pd.ExcelWriter(filename) as writer:
                for sheet_name, df in data.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"Đã lưu dữ liệu thành công vào file {filename}")
        except Exception as e:
            print(f"Lỗi khi lưu file Excel: {e}")

def main():
    # Khởi tạo collector
    collector = CompanyDataCollector()
    
    # Thu thập dữ liệu
    data = collector.navigate_pages(max_pages=5)
    
    # Lưu vào Excel
    collector.save_to_excel(data)

if __name__ == "__main__":
    main()