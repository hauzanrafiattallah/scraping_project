"""
Web Scraper untuk Google Search Results
Scraping hasil pencarian Google
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from datetime import datetime

class GoogleScraper:
    def __init__(self, headless=False):
        """Initialize scraper dengan Chrome driver"""
        chrome_options = ChromeOptions()
        
        if headless:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
        
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
    
    def search(self, query, max_results=10):
        """Scraping hasil pencarian Google"""
        print(f"🔍 Mencari: {query}")
        
        try:
            # Buka Google
            self.driver.get("https://www.google.com")
            time.sleep(2)
            
            # Cari search box
            search_box = self.wait.until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            print("⏳ Menunggu hasil...")
            time.sleep(3)
            
            # Ambil hasil pencarian
            results = []
            search_results = self.driver.find_elements(By.CSS_SELECTOR, "div.g")
            
            print(f"📄 Menemukan {len(search_results)} hasil")
            
            for idx, result in enumerate(search_results[:max_results], 1):
                try:
                    data = self._extract_result_data(result, idx)
                    if data:
                        results.append(data)
                        print(f"✅ [{idx}] {data['title'][:60]}...")
                except Exception as e:
                    continue
            
            return results
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return []
    
    def _extract_result_data(self, result, index):
        """Extract data dari search result"""
        try:
            # Title
            title_elem = result.find_element(By.CSS_SELECTOR, "h3")
            title = title_elem.text
            
            # Link
            link_elem = result.find_element(By.CSS_SELECTOR, "a")
            link = link_elem.get_attribute("href")
            
            # Description
            try:
                desc = result.find_element(By.CSS_SELECTOR, "div[data-sncf='1']").text
            except:
                desc = "N/A"
            
            return {
                "index": index,
                "title": title,
                "link": link,
                "description": desc,
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except:
            return None
    
    def save_to_json(self, data, filename):
        """Simpan data ke JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 Data disimpan ke {filename}")
    
    def close(self):
        """Tutup browser"""
        self.driver.quit()
        print("🔒 Browser ditutup")

def main():
    print("=" * 60)
    print("🔎 GOOGLE SEARCH SCRAPER")
    print("=" * 60)
    
    query = input("\n📝 Masukkan query pencarian: ").strip()
    if not query:
        query = "python web scraping"
        print(f"   Menggunakan query default: {query}")
    
    max_results = input("📊 Berapa hasil yang ingin di-scrape? (default: 10): ").strip()
    max_results = int(max_results) if max_results.isdigit() else 10
    
    headless = input("👻 Jalankan headless mode? (y/n, default: n): ").strip().lower()
    headless = headless == 'y'
    
    print("\n🚀 Memulai scraping...")
    
    scraper = GoogleScraper(headless=headless)
    
    try:
        results = scraper.search(query, max_results)
        
        if results:
            filename = f"google_{query.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            scraper.save_to_json(results, filename)
            print(f"\n✨ Berhasil scraping {len(results)} hasil!")
            print(f"📁 File tersimpan: {filename}")
        else:
            print("\n⚠️  Tidak ada hasil yang berhasil di-scrape")
    
    except KeyboardInterrupt:
        print("\n\n⏸️  Scraping dibatalkan")
    
    finally:
        scraper.close()
        print("\n✅ Selesai!")

if __name__ == "__main__":
    main()
