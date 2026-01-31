# 🤖 Web Scraping Project - Kabupaten Cirebon

Project web scraping menggunakan Selenium Python untuk riset bisnis dan data collection.

## 📁 Struktur Folder

```
scrapping_project/
├── scrapers/               # Semua script scraper
│   ├── scraper_google_maps.py      # ⭐ Google Maps scraper
│   ├── scraper_tokopedia.py        # Tokopedia scraper
│   ├── scraper_google.py           # Google Search scraper
│   └── scraper_universal.py        # Universal template
│
├── output/                 # Hasil scraping
│   ├── google_maps/        # Hasil Google Maps (JSON & CSV)
│   ├── tokopedia/          # Hasil Tokopedia
│   ├── google_search/      # Hasil Google Search
│   └── universal/          # Hasil scraper universal
│
├── debug/                  # File debugging
│   ├── html_sources/       # HTML source untuk debugging
│   └── screenshots/        # Screenshot untuk debugging
│
├── docs/                   # Dokumentasi
│   ├── README.md           # Dokumentasi lengkap
│   ├── GOOGLE_MAPS_GUIDE.md # Panduan Google Maps
│   └── QUICKSTART.py       # Quick start guide
│
├── main.py                 # Library imports reference
└── .gitignore             # Git ignore rules
```

## 🚀 Quick Start

### 1. Scraping Google Maps (RECOMMENDED)
```bash
python3 scrapers/scraper_google_maps.py
```

### 2. Scraping Website Lain
```bash
# Tokopedia
python3 scrapers/scraper_tokopedia.py

# Google Search
python3 scrapers/scraper_google.py

# Universal Template
python3 scrapers/scraper_universal.py
```

### 3. Lihat Dokumentasi
```bash
# Quick start
python3 docs/QUICKSTART.py

# Baca dokumentasi lengkap
cat docs/README.md

# Panduan Google Maps
cat docs/GOOGLE_MAPS_GUIDE.md
```

## 📊 Hasil Scraping Terbaru

Hasil scraping otomatis tersimpan di folder `output/` dengan struktur:
- `output/google_maps/` - Data bisnis dari Google Maps
- `output/tokopedia/` - Data produk dari Tokopedia
- `output/google_search/` - Hasil pencarian Google
- `output/universal/` - Hasil scraper custom

## 🔧 Requirements

- Python 3.9+
- Selenium 4.36.0
- webdriver-manager 4.0.2
- Google Chrome browser

## 📝 Instalasi

```bash
pip3 install selenium webdriver-manager
```

## 💡 Tips

1. **Pertama kali**: Gunakan scraper Google Maps dengan jumlah kecil (10-20)
2. **Debugging**: Cek folder `debug/screenshots/` jika ada error
3. **Hasil**: Semua hasil tersimpan otomatis di folder `output/`
4. **Dokumentasi**: Baca `docs/GOOGLE_MAPS_GUIDE.md` untuk panduan lengkap

## 🎯 Scraper Terbaik

**Google Maps Scraper** (`scrapers/scraper_google_maps.py`)
- ✅ Paling reliable
- ✅ Data lengkap (nama, alamat, telepon, website, dll)
- ✅ Support CSV & JSON
- ✅ Cocok untuk riset bisnis lokal

## 📞 Support

Jika ada masalah:
1. Cek `debug/screenshots/` untuk melihat apa yang terjadi
2. Baca dokumentasi di folder `docs/`
3. Jalankan dengan mode non-headless untuk debugging

---

**Happy Scraping! 🚀**

*Project untuk riset bisnis di Kabupaten Cirebon, Jawa Barat*
