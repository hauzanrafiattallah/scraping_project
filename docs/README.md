# 🤖 Web Scraping Project

Project web scraping menggunakan Selenium Python dengan berbagai template siap pakai.

## 📋 Requirements

- Python 3.9+
- Selenium 4.36.0
- webdriver-manager 4.0.2
- Google Chrome browser

## 🚀 Instalasi

Semua dependencies sudah terinstall. Jika belum, jalankan:

```bash
pip3 install selenium webdriver-manager
```

## 📁 File-file yang Tersedia

### 1. `scraper_tokopedia.py` - Tokopedia Product Scraper
Scraping produk dari Tokopedia berdasarkan keyword.

**Fitur:**
- ✅ Search produk berdasarkan keyword
- ✅ Extract nama, harga, rating, toko, lokasi, link
- ✅ Save ke JSON
- ✅ Headless mode support

**Cara Pakai:**
```bash
python3 scraper_tokopedia.py
```

**Input yang diminta:**
- Keyword pencarian (contoh: laptop, sepatu, hp)
- Jumlah produk yang ingin di-scrape
- Headless mode (y/n)

**Output:**
- File JSON: `tokopedia_[keyword]_[timestamp].json`

---

### 2. `scraper_google.py` - Google Search Scraper
Scraping hasil pencarian Google.

**Fitur:**
- ✅ Search di Google
- ✅ Extract title, link, description
- ✅ Save ke JSON
- ✅ Headless mode support

**Cara Pakai:**
```bash
python3 scraper_google.py
```

**Input yang diminta:**
- Query pencarian
- Jumlah hasil yang ingin di-scrape
- Headless mode (y/n)

**Output:**
- File JSON: `google_[query]_[timestamp].json`

---

### 3. `scraper_universal.py` - Universal Scraper Template
Template yang bisa disesuaikan untuk scraping website apapun.

**Fitur:**
- ✅ Helper functions lengkap
- ✅ Contoh scraping quotes.toscrape.com
- ✅ Custom scraper mode
- ✅ Save ke JSON & CSV
- ✅ Screenshot support
- ✅ Anti-detection settings

**Cara Pakai:**
```bash
python3 scraper_universal.py
```

**Menu:**
1. Contoh scraping (quotes.toscrape.com)
2. Custom scraper (masukkan URL sendiri)
3. Exit

**Output:**
- File JSON: `quotes_[timestamp].json`
- File CSV: `quotes_[timestamp].csv`
- Screenshot: `screenshot_[timestamp].png`

---

### 4. `scraper_google_maps.py` - Google Maps Business Scraper ⭐ NEW!
Scraping data bisnis/pengusaha dari Google Maps berdasarkan lokasi.

**Fitur:**
- ✅ Search bisnis berdasarkan kategori dan lokasi
- ✅ Extract nama, kategori, rating, total review
- ✅ Extract alamat, nomor telepon, website
- ✅ Extract jam operasional dan koordinat
- ✅ Save ke JSON & CSV
- ✅ Auto scroll untuk load lebih banyak hasil
- ✅ Random delay untuk menghindari deteksi bot

**Cara Pakai:**
```bash
python3 scraper_google_maps.py
```

**Input yang diminta:**
- Kategori bisnis (contoh: restoran, toko, bengkel, salon, hotel)
- Lokasi (default: Kabupaten Cirebon, Jawa Barat)
- Jumlah bisnis yang ingin di-scrape
- Headless mode (y/n)

**Output:**
- File JSON: `gmaps_[kategori]_[timestamp].json`
- File CSV: `gmaps_[kategori]_[timestamp].csv`

**Contoh Penggunaan:**
```bash
python3 scraper_google_maps.py
# Input kategori: restoran
# Input lokasi: Kabupaten Cirebon, Jawa Barat
# Input jumlah: 50
# Headless: n
```

---

## 🎯 Quick Start

### Scraping Tokopedia
```bash
python3 scraper_tokopedia.py
# Input: laptop
# Input: 10
# Input: n
```

### Scraping Google
```bash
python3 scraper_google.py
# Input: python tutorial
# Input: 10
# Input: n
```

### Scraping Custom Website
```bash
python3 scraper_universal.py
# Pilih: 2
# Input: https://example.com
# Input: n
```

## 📚 Helper Functions (Universal Scraper)

```python
scraper = UniversalScraper(headless=False)

# Navigasi
scraper.open_url("https://example.com")

# Cari element
element = scraper.find_element(By.ID, "element-id")
elements = scraper.find_elements(By.CLASS_NAME, "class-name")

# Extract data
text = scraper.get_text(element)
link = scraper.get_attribute(element, "href")

# Interaksi
scraper.click_element(element)
scraper.input_text(element, "text")

# Scroll
scraper.scroll_to_bottom()
scraper.scroll_by_pixels(1000)

# Save data
scraper.save_to_json(data, "output.json")
scraper.save_to_csv(data, "output.csv")
scraper.take_screenshot("screenshot.png")

# Tutup
scraper.close()
```

## 🔍 CSS Selectors Cheat Sheet

```python
# By ID
By.ID, "element-id"

# By Class
By.CLASS_NAME, "class-name"

# By Tag
By.TAG_NAME, "div"

# By CSS Selector
By.CSS_SELECTOR, "div.class-name"
By.CSS_SELECTOR, "#element-id"
By.CSS_SELECTOR, "div[data-testid='value']"

# By XPath
By.XPATH, "//div[@class='class-name']"
By.XPATH, "//a[contains(@href, 'example')]"
```

## ⚙️ Chrome Options

```python
chrome_options = ChromeOptions()

# Headless mode (tanpa GUI)
chrome_options.add_argument('--headless')

# Anti-detection
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

# User agent
chrome_options.add_argument('user-agent=Mozilla/5.0...')

# Window size
chrome_options.add_argument('--window-size=1920,1080')

# Disable images (faster)
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
```

## 🛡️ Best Practices

1. **Respect robots.txt** - Cek `website.com/robots.txt`
2. **Add delays** - Gunakan `time.sleep()` untuk tidak overload server
3. **Handle errors** - Gunakan try-except
4. **User agent** - Set user agent yang realistis
5. **Rate limiting** - Jangan scrape terlalu cepat
6. **Legal** - Pastikan scraping diperbolehkan

## ⚠️ Troubleshooting

### ChromeDriver Error
```bash
# Update webdriver-manager
pip3 install --upgrade webdriver-manager
```

### Element Not Found
- Tambah wait time: `WebDriverWait(driver, 20)`
- Cek CSS selector di browser DevTools
- Tunggu page load: `time.sleep(5)`

### Headless Mode Error
- Jalankan tanpa headless dulu untuk debug
- Tambah window size: `--window-size=1920,1080`

## 📝 Notes

- Semua scraper sudah include anti-detection settings
- Data disimpan dengan timestamp otomatis
- Support headless mode untuk running di server
- Error handling sudah included

## 🎓 Cara Modifikasi untuk Website Lain

1. Buka website target di browser
2. Inspect element (F12)
3. Cari CSS selector element yang ingin di-scrape
4. Copy template dari `scraper_universal.py`
5. Ganti CSS selector sesuai website target
6. Test dan adjust

## 📞 Support

Jika ada error atau pertanyaan, cek:
- CSS selector sudah benar?
- Website tidak block scraping?
- Chrome version compatible?
- Internet connection stable?

---

**Happy Scraping! 🚀**
