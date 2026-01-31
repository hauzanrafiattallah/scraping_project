"""
Google Maps Scraper - Kabupaten Cirebon
Scraping data pengusaha/bisnis di Kabupaten Cirebon, Jawa Barat
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
import random

class GoogleMapsScraper:
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
        chrome_options.add_argument('--lang=id-ID')
        
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)
        
        print("✅ Browser initialized")
    
    def search_businesses(self, query, location="Kabupaten Cirebon, Jawa Barat", max_results=50):
        """Scraping bisnis dari Google Maps"""
        print(f"🔍 Mencari: {query}")
        print(f"📍 Lokasi: {location}")
        
        try:
            # Buka Google Maps
            search_query = f"{query} {location}"
            url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
            
            self.driver.get(url)
            print("⏳ Menunggu hasil pencarian...")
            time.sleep(8)
            
            # Screenshot untuk debugging
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self.driver.save_screenshot(f"gmaps_search_{timestamp}.png")
            print("📸 Screenshot saved")
            
            # Scroll untuk load lebih banyak hasil
            print("📜 Scrolling untuk load lebih banyak hasil...")
            self._scroll_results_panel(max_results)
            
            # Ambil semua business cards
            businesses = []
            business_elements = self._get_business_elements()
            
            print(f"📦 Menemukan {len(business_elements)} bisnis")
            
            if len(business_elements) == 0:
                print("⚠️  Tidak ada bisnis ditemukan. Cek screenshot untuk debugging.")
                return []
            
            # Extract data dari setiap bisnis
            for idx, element in enumerate(business_elements[:max_results], 1):
                try:
                    print(f"⏳ Scraping bisnis {idx}/{min(len(business_elements), max_results)}...")
                    business_data = self._extract_business_data(element, idx)
                    
                    if business_data:
                        businesses.append(business_data)
                        print(f"✅ [{idx}] {business_data['name']}")
                        
                        # Random delay untuk menghindari deteksi bot
                        time.sleep(random.uniform(0.5, 1.5))
                    
                except Exception as e:
                    print(f"⚠️  Error pada bisnis {idx}: {str(e)}")
                    continue
            
            return businesses
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self.driver.save_screenshot(f"gmaps_error_{timestamp}.png")
            return []
    
    def _scroll_results_panel(self, target_results=50):
        """Scroll panel hasil untuk load lebih banyak bisnis"""
        # Cari panel hasil
        try:
            # Berbagai selector untuk panel hasil
            panel_selectors = [
                "div[role='feed']",
                "div.m6QErb",
                "div[aria-label*='Results']"
            ]
            
            scrollable_div = None
            for selector in panel_selectors:
                try:
                    scrollable_div = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if scrollable_div:
                        break
                except:
                    continue
            
            if not scrollable_div:
                print("⚠️  Panel hasil tidak ditemukan, skip scrolling")
                return
            
            # Scroll beberapa kali
            scroll_count = max(5, target_results // 10)
            for i in range(scroll_count):
                # Scroll ke bawah
                self.driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight", 
                    scrollable_div
                )
                time.sleep(2)
                
                # Cek apakah sudah sampai bawah
                current_height = self.driver.execute_script(
                    "return arguments[0].scrollTop", scrollable_div
                )
                max_height = self.driver.execute_script(
                    "return arguments[0].scrollHeight", scrollable_div
                )
                
                print(f"   Scroll {i+1}/{scroll_count}...")
                
                if current_height >= max_height - 100:
                    print("   Sudah sampai bawah")
                    break
                    
        except Exception as e:
            print(f"⚠️  Error saat scrolling: {str(e)}")
    
    def _get_business_elements(self):
        """Ambil semua element bisnis"""
        business_elements = []
        
        # Berbagai selector untuk business cards
        selectors = [
            "div.Nv2PK",
            "a.hfpxzc",
            "div[role='article']",
            "div.lI9IFe"
        ]
        
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✅ Business elements ditemukan dengan selector: {selector}")
                    business_elements = elements
                    break
            except:
                continue
        
        return business_elements
    
    def _extract_business_data(self, element, index):
        """Extract data dari business element"""
        try:
            # Klik element untuk buka detail
            try:
                element.click()
                time.sleep(3)
            except:
                # Jika tidak bisa klik, coba scroll ke element
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(1)
                element.click()
                time.sleep(3)
            
            # Ambil data dari panel detail
            data = {
                "index": index,
                "name": self._get_text_safe("h1.DUwDvf", "N/A"),
                "category": self._get_text_safe("button.DkEaL", "N/A"),
                "rating": self._get_rating(),
                "total_reviews": self._get_total_reviews(),
                "address": self._get_address(),
                "phone": self._get_phone(),
                "website": self._get_website(),
                "hours": self._get_hours(),
                "coordinates": self._get_coordinates(),
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return data
            
        except Exception as e:
            print(f"   Error extracting: {str(e)}")
            return None
    
    def _get_text_safe(self, selector, default="N/A"):
        """Safely get text from element"""
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            return element.text if element.text else default
        except:
            return default
    
    def _get_rating(self):
        """Get rating"""
        try:
            rating_selectors = [
                "div.F7nice span[aria-hidden='true']",
                "span.ceNzKf",
                "div.fontDisplayLarge"
            ]
            for selector in rating_selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    text = element.text
                    if text and any(char.isdigit() for char in text):
                        return text.split()[0] if text else "N/A"
                except:
                    continue
            return "N/A"
        except:
            return "N/A"
    
    def _get_total_reviews(self):
        """Get total reviews"""
        try:
            review_selectors = [
                "div.F7nice span[aria-label*='reviews']",
                "button.HHrUdb span",
                "span.RDApEe"
            ]
            for selector in review_selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    text = element.text
                    if '(' in text and ')' in text:
                        return text.split('(')[1].split(')')[0]
                except:
                    continue
            return "N/A"
        except:
            return "N/A"
    
    def _get_address(self):
        """Get address"""
        try:
            address_selectors = [
                "button[data-item-id='address'] div.fontBodyMedium",
                "div.Io6YTe",
                "button[data-tooltip='Copy address']"
            ]
            for selector in address_selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element.text:
                        return element.text
                except:
                    continue
            return "N/A"
        except:
            return "N/A"
    
    def _get_phone(self):
        """Get phone number"""
        try:
            phone_selectors = [
                "button[data-item-id*='phone'] div.fontBodyMedium",
                "button[aria-label*='Phone']",
                "a[href^='tel:']"
            ]
            for selector in phone_selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element.text:
                        return element.text
                    elif 'href' in element.get_attribute('outerHTML'):
                        return element.get_attribute('href').replace('tel:', '')
                except:
                    continue
            return "N/A"
        except:
            return "N/A"
    
    def _get_website(self):
        """Get website"""
        try:
            website_selectors = [
                "a[data-item-id='authority']",
                "button[data-item-id='authority'] div.fontBodyMedium",
                "a[aria-label*='Website']"
            ]
            for selector in website_selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    href = element.get_attribute('href')
                    if href and 'http' in href:
                        return href
                    elif element.text:
                        return element.text
                except:
                    continue
            return "N/A"
        except:
            return "N/A"
    
    def _get_hours(self):
        """Get business hours"""
        try:
            hours_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label*='Hours']")
            return hours_button.get_attribute('aria-label')
        except:
            return "N/A"
    
    def _get_coordinates(self):
        """Get coordinates from URL"""
        try:
            current_url = self.driver.current_url
            if '@' in current_url:
                coords = current_url.split('@')[1].split(',')[:2]
                return f"{coords[0]},{coords[1]}"
            return "N/A"
        except:
            return "N/A"
    
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
    
    def close(self):
        """Tutup browser"""
        self.driver.quit()
        print("🔒 Browser ditutup")

def main():
    """Main function"""
    print("=" * 70)
    print("🗺️  GOOGLE MAPS SCRAPER - KABUPATEN CIREBON")
    print("=" * 70)
    
    # Input dari user
    print("\n📝 Contoh kategori bisnis:")
    print("   - restoran")
    print("   - toko")
    print("   - bengkel")
    print("   - salon")
    print("   - hotel")
    print("   - cafe")
    print("   - warung makan")
    print("   - toko bangunan")
    
    query = input("\n🔍 Masukkan kategori bisnis yang ingin di-scrape: ").strip()
    if not query:
        query = "restoran"
        print(f"   Menggunakan kategori default: {query}")
    
    location = input("📍 Lokasi (default: Kabupaten Cirebon, Jawa Barat): ").strip()
    if not location:
        location = "Kabupaten Cirebon, Jawa Barat"
    
    max_results = input("📊 Berapa bisnis yang ingin di-scrape? (default: 20): ").strip()
    max_results = int(max_results) if max_results.isdigit() else 20
    
    headless = input("👻 Jalankan headless mode? (y/n, default: n): ").strip().lower()
    headless = headless == 'y'
    
    print("\n🚀 Memulai scraping...")
    print("⏰ Estimasi waktu: ~{} menit".format(max_results // 10 + 1))
    
    # Inisialisasi scraper
    scraper = GoogleMapsScraper(headless=headless)
    
    try:
        # Scraping bisnis
        businesses = scraper.search_businesses(query, location, max_results)
        
        if businesses:
            # Simpan ke file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            json_filename = f"gmaps_{query.replace(' ', '_')}_{timestamp}.json"
            csv_filename = f"gmaps_{query.replace(' ', '_')}_{timestamp}.csv"
            
            scraper.save_to_json(businesses, json_filename)
            scraper.save_to_csv(businesses, csv_filename)
            
            print(f"\n✨ Berhasil scraping {len(businesses)} bisnis!")
            print(f"📁 File JSON: {json_filename}")
            print(f"📁 File CSV: {csv_filename}")
            
            # Tampilkan summary
            print("\n📊 SUMMARY:")
            print(f"   Total bisnis: {len(businesses)}")
            with_phone = sum(1 for b in businesses if b['phone'] != 'N/A')
            with_website = sum(1 for b in businesses if b['website'] != 'N/A')
            print(f"   Dengan nomor telepon: {with_phone}")
            print(f"   Dengan website: {with_website}")
        else:
            print("\n⚠️  Tidak ada bisnis yang berhasil di-scrape")
    
    except KeyboardInterrupt:
        print("\n\n⏸️  Scraping dibatalkan oleh user")
    
    finally:
        scraper.close()
        print("\n✅ Selesai!")

if __name__ == "__main__":
    main()
