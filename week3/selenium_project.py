import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Thiết lập tùy chọn Chrome
browser_options = Options()
browser_options.add_argument("--disable-popup-blocking")

# Danh sách tài khoản test
test_accounts = [
    {"username": "standard_user", "password": "secret_sauce"},
    {"username": "locked_out_user", "password": "secret_sauce"},
    {"username": "problem_user", "password": "secret_sauce"},
    {"username": "performance_glitch_user", "password": "secret_sauce"}
]

# Khởi tạo danh sách lưu thông tin sản phẩm
product_list = []

# Khởi tạo trình duyệt
chrome_service = Service()
browser = webdriver.Chrome(service=chrome_service)

try:
    for account in test_accounts:
        # Truy cập trang đăng nhập
        browser.get("https://www.saucedemo.com")
        
        # Tìm các phần tử đăng nhập
        username_field = browser.find_element(By.ID, "user-name")
        password_field = browser.find_element(By.ID, "password")
        login_button = browser.find_element(By.ID, "login-button")
        
        # Điền thông tin đăng nhập
        username_field.send_keys(account["username"])
        password_field.send_keys(account["password"])
        login_button.click()
        
        time.sleep(2)  # Đợi trang tải
        
        # Kiểm tra đăng nhập thành công
        if "inventory.html" in browser.current_url:
            print(f"Đăng nhập thành công với tài khoản {account['username']}")
            
            # Lấy thông tin sản phẩm
            product_elements = browser.find_elements(By.CLASS_NAME, "inventory_item")
            for product in product_elements:
                product_name = product.find_element(By.CLASS_NAME, "inventory_item_name").text
                product_price = product.find_element(By.CLASS_NAME, "inventory_item_price").text
                product_list.append({
                    "Tài khoản": account["username"],
                    "Tên sản phẩm": product_name,
                    "Giá": product_price.replace("$", "")
                })
        else:
            print(f"Đăng nhập thất bại với tài khoản {account['username']}")

    # Lưu dữ liệu vào file Excel
    if product_list:
        product_df = pd.DataFrame(product_list)
        product_df.to_excel("saucedemo_products.xlsx", index=False)
        print("Đã lưu dữ liệu vào file saucedemo_products.xlsx")

except Exception as error:
    print(f"Có lỗi xảy ra: {error}")

finally:
    # Đóng trình duyệt
    browser.quit()


