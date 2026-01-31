# Import library Selenium untuk web scraping
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

# Import untuk Chrome options
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService

# Import untuk Firefox options (opsional)
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

# Import exceptions untuk error handling
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    WebDriverException
)

# Import library tambahan yang sering digunakan
import time
import random
from datetime import datetime

# Import webdriver manager untuk otomatis download driver
from webdriver_manager.chrome import ChromeDriverManager

# Contoh setup driver (uncomment untuk menggunakan)
# chrome_options = ChromeOptions()
# chrome_options.add_argument('--headless')  # Jalankan tanpa membuka browser
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--disable-blink-features=AutomationControlled')
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# chrome_options.add_experimental_option('useAutomationExtension', False)

# Setup driver dengan webdriver-manager (otomatis download driver)
# service = ChromeService(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service, options=chrome_options)

if __name__ == "__main__":
    print("Selenium libraries imported successfully!")
    print("Ready untuk web scraping project!")
    
    # Contoh penggunaan sederhana
    # Uncomment kode di bawah untuk test
    """
    chrome_options = ChromeOptions()
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get("https://www.google.com")
        print(f"Title: {driver.title}")
        time.sleep(2)
    finally:
        driver.quit()
    """


print("Test")
