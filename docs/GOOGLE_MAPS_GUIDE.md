# 🗺️ Google Maps Scraper - Panduan Lengkap

## 📋 Deskripsi

Scraper ini dirancang khusus untuk mengambil data bisnis/pengusaha dari Google Maps berdasarkan kategori dan lokasi tertentu. Sangat cocok untuk:

- 📊 Riset pasar lokal
- 📞 Mengumpulkan database kontak bisnis
- 🏪 Analisis kompetitor
- 📍 Pemetaan bisnis di suatu wilayah
- 📈 Market research

## 🎯 Data yang Di-scrape

Setiap bisnis akan menghasilkan data berikut:

| Field | Deskripsi | Contoh |
|-------|-----------|--------|
| **name** | Nama bisnis | "Warung Makan Bu Tini" |
| **category** | Kategori/jenis usaha | "Restoran" |
| **rating** | Rating (1-5) | "4.5" |
| **total_reviews** | Jumlah review | "120" |
| **address** | Alamat lengkap | "Jl. Raya Cirebon No. 123" |
| **phone** | Nomor telepon | "0231-123456" |
| **website** | Website (jika ada) | "https://example.com" |
| **hours** | Jam operasional | "Buka 24 jam" |
| **coordinates** | Koordinat GPS | "-6.7063,108.5571" |
| **scraped_at** | Waktu scraping | "2026-01-31 13:30:00" |

## 🚀 Cara Menggunakan

### 1. Jalankan Scraper

```bash
python3 scraper_google_maps.py
```

### 2. Input yang Diminta

#### a. Kategori Bisnis
Masukkan jenis bisnis yang ingin di-scrape:

**Contoh kategori populer:**
- `restoran` - Semua jenis restoran
- `warung makan` - Warung makan tradisional
- `cafe` - Kafe dan coffee shop
- `hotel` - Hotel dan penginapan
- `toko` - Toko retail
- `bengkel` - Bengkel kendaraan
- `salon` - Salon kecantikan
- `apotek` - Apotek dan toko obat
- `toko bangunan` - Toko material bangunan
- `laundry` - Jasa laundry
- `fotocopy` - Jasa fotocopy
- `barbershop` - Pangkas rambut pria
- `gym` - Fitness center
- `spa` - Spa dan massage
- `minimarket` - Minimarket

**Tips:**
- Gunakan bahasa Indonesia untuk hasil lebih akurat
- Semakin spesifik kategori, semakin relevan hasilnya
- Bisa gunakan kombinasi: "restoran seafood", "hotel murah", dll

#### b. Lokasi
Masukkan lokasi target (default: Kabupaten Cirebon, Jawa Barat)

**Format yang bisa digunakan:**
- `Kabupaten Cirebon, Jawa Barat`
- `Kota Cirebon`
- `Cirebon`
- `Sumber, Cirebon`
- `Palimanan, Cirebon`

**Lokasi lain di Indonesia:**
- `Jakarta Selatan, DKI Jakarta`
- `Bandung, Jawa Barat`
- `Surabaya, Jawa Timur`
- `Yogyakarta`
- dll.

#### c. Jumlah Bisnis
Masukkan berapa banyak bisnis yang ingin di-scrape (default: 20)

**Rekomendasi:**
- **10-20** untuk testing/coba-coba
- **50-100** untuk riset kecil
- **100-200** untuk riset menengah
- **200+** untuk riset besar (butuh waktu lama)

**Estimasi waktu:**
- 10 bisnis: ~2-3 menit
- 50 bisnis: ~8-10 menit
- 100 bisnis: ~15-20 menit
- 200 bisnis: ~30-40 menit

#### d. Headless Mode
- **n (No)** - Browser akan terlihat (recommended untuk pertama kali)
- **y (Yes)** - Browser berjalan di background (lebih cepat)

## 📊 Contoh Penggunaan

### Contoh 1: Scraping Restoran di Cirebon
```bash
$ python3 scraper_google_maps.py

🔍 Masukkan kategori bisnis: restoran
📍 Lokasi: Kabupaten Cirebon, Jawa Barat
📊 Berapa bisnis: 50
👻 Headless mode: n
```

**Output:**
- `gmaps_restoran_20260131_133000.json`
- `gmaps_restoran_20260131_133000.csv`

### Contoh 2: Scraping Hotel di Kota Cirebon
```bash
$ python3 scraper_google_maps.py

🔍 Masukkan kategori bisnis: hotel
📍 Lokasi: Kota Cirebon
📊 Berapa bisnis: 30
👻 Headless mode: n
```

### Contoh 3: Scraping Toko Bangunan
```bash
$ python3 scraper_google_maps.py

🔍 Masukkan kategori bisnis: toko bangunan
📍 Lokasi: Kabupaten Cirebon, Jawa Barat
📊 Berapa bisnis: 20
👻 Headless mode: n
```

## 📁 Format Output

### JSON Format
```json
[
  {
    "index": 1,
    "name": "Warung Makan Bu Tini",
    "category": "Restoran",
    "rating": "4.5",
    "total_reviews": "120",
    "address": "Jl. Raya Cirebon No. 123, Cirebon",
    "phone": "0231-123456",
    "website": "https://example.com",
    "hours": "Buka 24 jam",
    "coordinates": "-6.7063,108.5571",
    "scraped_at": "2026-01-31 13:30:00"
  },
  ...
]
```

### CSV Format
File CSV bisa langsung dibuka di Excel/Google Sheets dengan kolom:
- index
- name
- category
- rating
- total_reviews
- address
- phone
- website
- hours
- coordinates
- scraped_at

## 💡 Tips & Tricks

### 1. Mendapatkan Hasil Maksimal
- ✅ Gunakan kategori yang spesifik
- ✅ Coba berbagai variasi keyword
- ✅ Scrape di waktu yang berbeda untuk hasil yang berbeda
- ✅ Gunakan lokasi yang spesifik (kecamatan, kelurahan)

### 2. Menghindari Deteksi Bot
- ✅ Jangan scrape terlalu banyak sekaligus (max 200)
- ✅ Gunakan delay yang cukup (sudah otomatis di scraper)
- ✅ Jangan jalankan scraper terlalu sering
- ✅ Gunakan headless mode dengan bijak

### 3. Mengolah Data Hasil Scraping
- ✅ Buka CSV di Excel untuk analisis
- ✅ Filter berdasarkan rating untuk cari bisnis terbaik
- ✅ Gunakan koordinat untuk mapping di Google Maps
- ✅ Export nomor telepon untuk database marketing

## ⚠️ Troubleshooting

### Tidak Ada Hasil
**Penyebab:**
- Kategori terlalu spesifik
- Lokasi tidak ada bisnis dengan kategori tersebut
- Typo di kategori atau lokasi

**Solusi:**
- Coba kategori yang lebih umum
- Cek spelling kategori dan lokasi
- Coba lokasi yang lebih luas (kabupaten vs kecamatan)

### Scraper Berhenti di Tengah
**Penyebab:**
- Internet terputus
- Google Maps mendeteksi bot
- Element tidak ditemukan

**Solusi:**
- Cek koneksi internet
- Restart scraper dengan jumlah lebih kecil
- Jalankan tanpa headless mode untuk debug

### Data Tidak Lengkap (Banyak N/A)
**Penyebab:**
- Bisnis tidak melengkapi profil Google Maps
- Selector berubah (Google Maps update)

**Solusi:**
- Ini normal, tidak semua bisnis punya data lengkap
- Cek screenshot untuk debugging
- Filter data yang punya nomor telepon/website

## 📈 Use Cases

### 1. Riset Pasar Restoran
```bash
# Scrape semua restoran di Cirebon
Kategori: restoran
Lokasi: Kabupaten Cirebon, Jawa Barat
Jumlah: 100

# Analisis:
- Lihat rating tertinggi
- Cek lokasi paling ramai (banyak review)
- Bandingkan harga (dari nama/kategori)
```

### 2. Database Marketing
```bash
# Scrape toko untuk marketing
Kategori: toko
Lokasi: Kabupaten Cirebon, Jawa Barat
Jumlah: 200

# Gunakan:
- Nomor telepon untuk WhatsApp marketing
- Alamat untuk direct mail
- Website untuk email marketing
```

### 3. Analisis Kompetitor
```bash
# Scrape kompetitor sejenis
Kategori: bengkel mobil
Lokasi: Kota Cirebon
Jumlah: 50

# Analisis:
- Rating kompetitor
- Lokasi strategis
- Jam operasional
- Review pelanggan
```

## 🔒 Legal & Ethics

**Perhatian:**
- ✅ Data Google Maps bersifat publik
- ✅ Gunakan untuk riset dan analisis pribadi
- ⚠️ Jangan gunakan untuk spam
- ⚠️ Hormati privasi bisnis
- ⚠️ Jangan overload server Google

**Best Practice:**
- Scrape dengan bijak (jangan berlebihan)
- Gunakan data secara etis
- Respect robots.txt dan terms of service

## 📞 Support

Jika ada masalah:
1. Cek screenshot yang di-generate
2. Baca error message dengan teliti
3. Coba dengan jumlah lebih kecil dulu
4. Jalankan tanpa headless mode untuk debug

---

**Happy Scraping! 🗺️**

*Dibuat khusus untuk riset bisnis di Kabupaten Cirebon, Jawa Barat*
