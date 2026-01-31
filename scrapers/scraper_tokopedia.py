"""
Web Scraper untuk Tokopedia
Scraping produk berdasarkan keyword pencarian
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
from datetime import datetime

class TokopediaScraper:
    def __init__(self, headless=False):
        """Initialize scraper dengan Chrome driver"""
        chrome_options = ChromeOptions()
        
        if headless:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        
    def search_products(self, keyword, max_products=10):
        """Scraping produk dari Tokopedia berdasarkan keyword"""
        print(f"🔍 Mencari produk: {keyword}")
        
        try:
            # Buka Tokopedia
            self.driver.get("https://www.tokopedia.com/")
            time.sleep(5)
            
            # Screenshot untuk debugging
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self.driver.save_screenshot(f"debug_1_homepage_{timestamp}.png")
            print("📸 Screenshot homepage saved")
            
            # Cari search box dengan multiple selectors
            search_box = None
            selectors = [
                "input[data-unify='Search']",
                "input[type='search']",
                "input[placeholder*='Cari']",
                "input.css-3017qm"
            ]
            
            for selector in selectors:
                try:
                    search_box = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    print(f"✅ Search box ditemukan dengan selector: {selector}")
                    break
                except:
                    continue
            
            if not search_box:
                print("❌ Search box tidak ditemukan!")
                self.driver.save_screenshot(f"debug_error_no_searchbox_{timestamp}.png")
                return []
            
            search_box.clear()
            search_box.send_keys(keyword)
            time.sleep(1)
            search_box.send_keys(Keys.RETURN)
            
            print("⏳ Menunggu hasil pencarian...")
            time.sleep(8)  # Wait lebih lama
            
            # Screenshot hasil pencarian
            self.driver.save_screenshot(f"debug_2_search_results_{timestamp}.png")
            print("📸 Screenshot search results saved")
            
            # Scroll untuk load lebih banyak produk
            self._scroll_page()
            
            # Coba berbagai selector untuk product cards
            product_cards = []
            card_selectors = [
                "div[data-testid='master-product-card']",
                "div[data-testid='divProductWrapper']",
                "div.css-1sn1xa2",
                "div.pcv3__container"
            ]
            
            for selector in card_selectors:
                product_cards = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if product_cards:
                    print(f"✅ Product cards ditemukan dengan selector: {selector}")
                    break
            
            print(f"📦 Menemukan {len(product_cards)} produk")
            
            if len(product_cards) == 0:
                print("⚠️  Tidak ada produk ditemukan. Cek screenshot untuk debugging.")
                print(f"📸 Lihat file: debug_2_search_results_{timestamp}.png")
                
                # Print page source untuk debugging
                with open(f"debug_page_source_{timestamp}.html", "w", encoding="utf-8") as f:
                    f.write(self.driver.page_source)
                print(f"📄 Page source saved: debug_page_source_{timestamp}.html")
                
                return []
            
            # Ambil data produk
            products = []
            for idx, card in enumerate(product_cards[:max_products], 1):
                try:
                    product_data = self._extract_product_data(card, idx)
                    if product_data:
                        products.append(product_data)
                        print(f"✅ [{idx}] {product_data['name'][:50]}... - {product_data['price']}")
                except Exception as e:
                    print(f"⚠️  Error pada produk {idx}: {str(e)}")
                    continue
            
            return products
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self.driver.save_screenshot(f"debug_error_{timestamp}.png")
            print(f"📸 Error screenshot saved: debug_error_{timestamp}.png")
            return []
    
    def _extract_product_data(self, card, index):
        """Extract data dari product card"""
        try:
            # Nama produk - coba berbagai selector
            name = None
            name_selectors = [
                "span[class*='prd_link-product-name']",
                "div.prd_link-product-name",
                "span.css-20kt3o",
                "div[data-testid='spnSRPProdName']"
            ]
            for selector in name_selectors:
                try:
                    name = card.find_element(By.CSS_SELECTOR, selector).text
                    if name:
                        break
                except:
                    continue
            
            if not name:
                return None
            
            # Harga - coba berbagai selector
            price = None
            price_selectors = [
                "span[class*='prd_link-product-price']",
                "div.prd_link-product-price",
                "span.css-o5uqvq",
                "div[data-testid='spnSRPProdPrice']"
            ]
            for selector in price_selectors:
                try:
                    price = card.find_element(By.CSS_SELECTOR, selector).text
                    if price:
                        break
                except:
                    continue
            
            if not price:
                price = "N/A"
            
            # Rating (optional)
            rating = "N/A"
            rating_selectors = [
                "span[class*='rating']",
                "span.css-t70v7i",
                "div[data-testid='spnSRPProdRating']"
            ]
            for selector in rating_selectors:
                try:
                    rating = card.find_element(By.CSS_SELECTOR, selector).text
                    if rating:
                        break
                except:
                    continue
            
            # Toko
            shop = "N/A"
            shop_selectors = [
                "span[class*='prd_link-shop-name']",
                "span.css-1kr22w3",
                "div[data-testid='spnSRPProdShop']"
            ]
            for selector in shop_selectors:
                try:
                    shop = card.find_element(By.CSS_SELECTOR, selector).text
                    if shop:
                        break
                except:
                    continue
            
            # Link produk
            link = "N/A"
            try:
                link = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            except:
                pass
            
            # Lokasi
            location = "N/A"
            location_selectors = [
                "span[class*='prd_link-shop-loc']",
                "span.css-1kdc32b",
                "div[data-testid='spnSRPProdLoc']"
            ]
            for selector in location_selectors:
                try:
                    location = card.find_element(By.CSS_SELECTOR, selector).text
                    if location:
                        break
                except:
                    continue
            
            return {
                "index": index,
                "name": name,
                "price": price,
                "rating": rating,
                "shop": shop,
                "location": location,
                "link": link,
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            print(f"   Debug: Error extracting data - {str(e)}")
            return None
    
    def _scroll_page(self):
        """Scroll halaman untuk load lebih banyak produk"""
        for _ in range(3):
            self.driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(1)
    
    def save_to_json(self, data, filename):
        """Simpan data ke file JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 Data disimpan ke {filename}")
    
    def close(self):
        """Tutup browser"""
        self.driver.quit()
        print("🔒 Browser ditutup")

def main():
    """Main function"""
    print("=" * 60)
    print("🛒 TOKOPEDIA PRODUCT SCRAPER")
    print("=" * 60)
    
    # Input dari user
    keyword = input("\n📝 Masukkan keyword pencarian (contoh: laptop): ").strip()
    if not keyword:
        keyword = "laptop"
        print(f"   Menggunakan keyword default: {keyword}")
    
    max_products = input("📊 Berapa produk yang ingin di-scrape? (default: 10): ").strip()
    max_products = int(max_products) if max_products.isdigit() else 10
    
    headless = input("👻 Jalankan headless mode? (y/n, default: n): ").strip().lower()
    headless = headless == 'y'
    
    print("\n🚀 Memulai scraping...")
    
    # Inisialisasi scraper
    scraper = TokopediaScraper(headless=headless)
    
    try:
        # Scraping produk
        products = scraper.search_products(keyword, max_products)
        
        if products:
            # Simpan ke JSON
            filename = f"tokopedia_{keyword.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            scraper.save_to_json(products, filename)
            
            print(f"\n✨ Berhasil scraping {len(products)} produk!")
            print(f"📁 File tersimpan: {filename}")
        else:
            print("\n⚠️  Tidak ada produk yang berhasil di-scrape")
    
    except KeyboardInterrupt:
        print("\n\n⏸️  Scraping dibatalkan oleh user")
    
    finally:
        scraper.close()
        print("\n✅ Selesai!")

if __name__ == "__main__":
    main()
