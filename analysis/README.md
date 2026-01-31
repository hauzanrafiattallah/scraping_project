# 📊 Data Analysis - Google Maps Cafe Scraping

Folder ini berisi analisis data hasil scraping cafe/kedai kopi di Kabupaten Cirebon dari Google Maps.

## 📁 Struktur Folder

```
analysis/
├── notebooks/              # Jupyter notebooks untuk analisis
│   └── eda_google_maps_cafe.ipynb    # EDA lengkap
│
├── reports/                # Hasil analisis & laporan
│   ├── cleaned_cafe_data.csv         # Data yang sudah dibersihkan
│   ├── summary_statistics.csv        # Statistik ringkasan
│   └── eda_summary.txt               # Executive summary
│
└── visualizations/         # Grafik & visualisasi
    ├── missing_data.png
    ├── category_distribution.png
    ├── rating_distribution.png
    ├── rating_by_category.png
    ├── top_10_cafes.png
    ├── district_distribution.png
    ├── contact_availability.png
    └── cafe_map.html                 # Interactive map
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install pandas numpy matplotlib seaborn plotly jupyter
```

### 2. Run Jupyter Notebook

```bash
cd analysis/notebooks
jupyter notebook eda_google_maps_cafe.ipynb
```

### 3. View Results

- **Visualizations:** `analysis/visualizations/`
- **Reports:** `analysis/reports/`
- **Interactive Map:** Open `visualizations/cafe_map.html` in browser

## 📊 Analisis yang Dilakukan

### 1. **Data Cleaning**
- ✅ Handling missing values
- ✅ Data type conversion
- ✅ Duplicate removal
- ✅ Feature engineering

### 2. **Exploratory Data Analysis (EDA)**
- ✅ Category distribution analysis
- ✅ Rating analysis & statistics
- ✅ Geographic distribution
- ✅ Top performers identification
- ✅ Digital presence assessment

### 3. **Visualizations**
- ✅ Bar charts & pie charts
- ✅ Histograms & box plots
- ✅ Geographic heatmaps
- ✅ Interactive Plotly maps

### 4. **Business Insights**
- ✅ Market opportunity analysis
- ✅ Competitor benchmarking
- ✅ Digital marketing recommendations
- ✅ Quality standards

## 📈 Key Findings

Lihat file `reports/eda_summary.txt` untuk ringkasan lengkap hasil analisis.

### Highlights:
- **Total Cafes:** 74 (setelah cleaning)
- **Average Rating:** ~4.6 ⭐
- **Top Category:** Kedai Kopi
- **Digital Presence:** 
  - Phone: ~90%
  - Website: ~30%

## 🎯 Use Cases

1. **Business Research:** Riset pasar untuk membuka cafe baru
2. **Competitor Analysis:** Analisis kompetitor di area tertentu
3. **Marketing Strategy:** Identifikasi gap digital marketing
4. **Location Planning:** Pilih lokasi strategis berdasarkan data

## 📝 Notes

- Data source: `../output/google_maps/gmaps_cafe_20260131_134158.csv`
- Analysis date: 31 Januari 2026
- Total records: 75 (74 after deduplication)

## 🔄 Update Analysis

Untuk update analisis dengan data baru:

1. Jalankan scraper baru
2. Update `data_path` di notebook
3. Run all cells
4. Check new visualizations & reports

---

**Happy Analyzing! 📊**
