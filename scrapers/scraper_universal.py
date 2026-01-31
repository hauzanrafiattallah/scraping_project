"""
Web Scraper Template - Universal
Template yang bisa disesuaikan untuk scraping website apapun
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import csv
from datetime import datetime

class UniversalScraper:
    def __init__(self, headless=False):
        """Initialize scraper dengan Chrome driver"""
        chrome_options = ChromeOptions()
        
        if headless:
            chrome_options.add_argument('--headless')
        
        # Anti-detection settings
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)
        
        print("✅ Browser initialized")
    
    def open_url(self, url):
        """Buka URL"""
        print(f"🌐 Membuka: {url}")
        self.driver.get(url)
        time.sleep(3)
    
    def find_element(self, by, value, timeout=10):
        """Cari single element"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located((by, value)))
            return element
        except TimeoutException:
            print(f"⚠️  Element tidak ditemukan: {value}")
            return None
    
    def find_elements(self, by, value):
        """Cari multiple elements"""
        try:
            elements = self.driver.find_elements(by, value)
            print(f"📦 Menemukan {len(elements)} elements")
            return elements
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return []
    
    def get_text(self, element):
        """Ambil text dari element"""
        try:
            return element.text
        except:
            return "N/A"
    
    def get_attribute(self, element, attr):
        """Ambil attribute dari element"""
        try:
            return element.get_attribute(attr)
        except:
            return "N/A"
    
    def click_element(self, element):
        """Klik element"""
        try:
            element.click()
            time.sleep(2)
            return True
        except Exception as e:
            print(f"⚠️  Tidak bisa klik: {str(e)}")
            return False
    
    def input_text(self, element, text):
        """Input text ke element"""
        try:
            element.clear()
            element.send_keys(text)
            return True
        except Exception as e:
            print(f"⚠️  Tidak bisa input text: {str(e)}")
            return False
    
    def scroll_to_bottom(self, pause_time=2):
        """Scroll ke bawah halaman"""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause_time)
            
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    def scroll_by_pixels(self, pixels=1000):
        """Scroll sejumlah pixels"""
        self.driver.execute_script(f"window.scrollBy(0, {pixels});")
        time.sleep(1)
    
    def take_screenshot(self, filename):
        """Ambil screenshot"""
        self.driver.save_screenshot(filename)
        print(f"📸 Screenshot disimpan: {filename}")
    
    def save_to_json(self, data, filename):
        """Simpan data ke JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 Data disimpan ke {filename}")
    
    def save_to_csv(self, data, filename):
        """Simpan data ke CSV"""
        if not data:
            print("⚠️  Tidak ada data untuk disimpan")
            return
        
        keys = data[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        print(f"💾 Data disimpan ke {filename}")
    
    def wait_for_seconds(self, seconds):
        """Tunggu beberapa detik"""
        print(f"⏳ Menunggu {seconds} detik...")
        time.sleep(seconds)
    
    def close(self):
        """Tutup browser"""
        self.driver.quit()
        print("🔒 Browser ditutup")

# ============================================================================
# CONTOH PENGGUNAAN
# ============================================================================

def example_scrape_quotes():
    """Contoh scraping quotes dari quotes.toscrape.com"""
    print("=" * 60)
    print("📚 CONTOH: SCRAPING QUOTES")
    print("=" * 60)
    
    scraper = UniversalScraper(headless=False)
    
    try:
        # 1. Buka website
        scraper.open_url("http://quotes.toscrape.com/")
        
        # 2. Cari semua quotes
        quote_elements = scraper.find_elements(By.CLASS_NAME, "quote")
        
        # 3. Extract data
        quotes_data = []
        for idx, quote_elem in enumerate(quote_elements, 1):
            try:
                # Ambil text quote
                text = quote_elem.find_element(By.CLASS_NAME, "text").text
                
                # Ambil author
                author = quote_elem.find_element(By.CLASS_NAME, "author").text
                
                # Ambil tags
                tag_elements = quote_elem.find_elements(By.CLASS_NAME, "tag")
                tags = [tag.text for tag in tag_elements]
                
                quote_data = {
                    "index": idx,
                    "quote": text,
                    "author": author,
                    "tags": tags,
                    "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                quotes_data.append(quote_data)
                print(f"✅ [{idx}] {author}: {text[:50]}...")
                
            except Exception as e:
                print(f"⚠️  Error pada quote {idx}: {str(e)}")
                continue
        
        # 4. Simpan data
        if quotes_data:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            scraper.save_to_json(quotes_data, f"quotes_{timestamp}.json")
            scraper.save_to_csv(quotes_data, f"quotes_{timestamp}.csv")
            print(f"\n✨ Berhasil scraping {len(quotes_data)} quotes!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    finally:
        scraper.close()
        print("\n✅ Selesai!")

def custom_scraper():
    """Template untuk scraping custom"""
    print("=" * 60)
    print("🔧 CUSTOM SCRAPER")
    print("=" * 60)
    
    url = input("\n🌐 Masukkan URL website: ").strip()
    if not url:
        print("⚠️  URL tidak boleh kosong!")
        return
    
    headless = input("👻 Jalankan headless mode? (y/n, default: n): ").strip().lower()
    headless = headless == 'y'
    
    scraper = UniversalScraper(headless=headless)
    
    try:
        # Buka URL
        scraper.open_url(url)
        
        # Tunggu user melihat halaman
        scraper.wait_for_seconds(5)
        
        # Ambil screenshot
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        scraper.take_screenshot(f"screenshot_{timestamp}.png")
        
        print("\n💡 Tips:")
        print("   - Inspect element di browser untuk cari CSS selector")
        print("   - Gunakan scraper.find_elements(By.CSS_SELECTOR, 'your-selector')")
        print("   - Modifikasi function ini sesuai kebutuhan Anda")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    finally:
        scraper.close()

def main():
    """Main menu"""
    print("\n" + "=" * 60)
    print("🤖 UNIVERSAL WEB SCRAPER")
    print("=" * 60)
    print("\nPilih mode:")
    print("1. Contoh scraping (quotes.toscrape.com)")
    print("2. Custom scraper (masukkan URL sendiri)")
    print("3. Exit")
    
    choice = input("\nPilihan (1/2/3): ").strip()
    
    if choice == "1":
        example_scrape_quotes()
    elif choice == "2":
        custom_scraper()
    elif choice == "3":
        print("👋 Bye!")
    else:
        print("⚠️  Pilihan tidak valid!")

if __name__ == "__main__":
    main()
