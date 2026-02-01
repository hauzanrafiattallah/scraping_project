"""
Data Cleaner untuk Data Cafe Cirebon
Script untuk membersihkan dan memproses data hasil scraping Google Maps
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path


def load_data(file_path):
    """Memuat data dari file CSV"""
    try:
        df = pd.read_csv(file_path)
        print(f"[INFO] Data berhasil dimuat: {len(df)} baris, {len(df.columns)} kolom")
        return df
    except FileNotFoundError:
        print(f"[ERROR] File tidak ditemukan: {file_path}")
        return None
    except Exception as e:
        print(f"[ERROR] Gagal memuat data: {e}")
        return None


def clean_rating(df):
    """
    Membersihkan kolom rating dari format Indonesia ke float
    Contoh: "4,5" -> 4.5
    """
    def parse_rating(value):
        if pd.isna(value) or value == "N/A":
            return np.nan
        try:
            # Ganti koma dengan titik untuk format Indonesia
            clean_value = str(value).replace(",", ".").strip()
            return float(clean_value)
        except (ValueError, TypeError):
            return np.nan
    
    df["rating_clean"] = df["rating"].apply(parse_rating)
    
    valid_count = df["rating_clean"].notna().sum()
    print(f"[INFO] Rating berhasil dibersihkan: {valid_count}/{len(df)} valid")
    
    return df


def parse_coordinates(df):
    """
    Memisahkan coordinates menjadi latitude dan longitude
    Format input: "-6.7295044,108.4773185"
    """
    def extract_lat_lng(coord):
        if pd.isna(coord) or coord == "N/A":
            return np.nan, np.nan
        try:
            parts = str(coord).split(",")
            if len(parts) == 2:
                return float(parts[0].strip()), float(parts[1].strip())
        except (ValueError, TypeError):
            pass
        return np.nan, np.nan
    
    # Ekstrak latitude dan longitude
    coords = df["coordinates"].apply(extract_lat_lng)
    df["latitude"] = coords.apply(lambda x: x[0])
    df["longitude"] = coords.apply(lambda x: x[1])
    
    valid_count = df["latitude"].notna().sum()
    print(f"[INFO] Koordinat berhasil diparse: {valid_count}/{len(df)} valid")
    
    return df


def extract_kecamatan(df):
    """
    Mengekstrak nama kecamatan dari alamat
    Pattern: "Kec. NamaKecamatan,"
    """
    def get_kecamatan(address):
        if pd.isna(address) or address == "N/A":
            return "Tidak Diketahui"
        
        # Cari pattern "Kec. [NamaKecamatan]"
        match = re.search(r"Kec\.\s*([^,]+)", str(address))
        if match:
            return match.group(1).strip()
        return "Tidak Diketahui"
    
    df["kecamatan"] = df["address"].apply(get_kecamatan)
    
    # Hitung kecamatan unik
    unique_kec = df["kecamatan"].nunique()
    print(f"[INFO] Kecamatan berhasil diekstrak: {unique_kec} kecamatan unik")
    
    return df


def identify_wilayah(df):
    """
    Mengidentifikasi wilayah: Kota Cirebon atau Kabupaten Cirebon
    Berdasarkan string dalam alamat
    """
    def get_wilayah(address):
        if pd.isna(address) or address == "N/A":
            return "Tidak Diketahui"
        
        addr_lower = str(address).lower()
        
        # Cek Kota Cirebon terlebih dahulu (lebih spesifik)
        if "kota cirebon" in addr_lower:
            return "Kota Cirebon"
        # Cek Kabupaten Cirebon
        elif "kabupaten cirebon" in addr_lower:
            return "Kabupaten Cirebon"
        # Fallback jika hanya ada "Cirebon" tanpa kota/kabupaten
        elif "cirebon" in addr_lower:
            # Cek berdasarkan kecamatan yang dikenal
            kecamatan_kota = ["kesambi", "harjamukti", "kejaksan", "lemahwungkuk", "pekalipan"]
            for kec in kecamatan_kota:
                if kec in addr_lower:
                    return "Kota Cirebon"
            return "Kabupaten Cirebon"  # Default ke Kabupaten jika tidak jelas
        
        return "Tidak Diketahui"
    
    df["wilayah"] = df["address"].apply(get_wilayah)
    
    # Tampilkan distribusi wilayah
    wilayah_counts = df["wilayah"].value_counts()
    print(f"[INFO] Distribusi wilayah:")
    for wil, count in wilayah_counts.items():
        print(f"       - {wil}: {count}")
    
    return df


def clean_category(df):
    """
    Membersihkan kategori yang N/A atau kosong
    """
    df["category_clean"] = df["category"].apply(
        lambda x: "Cafe/Kedai Kopi" if pd.isna(x) or x == "N/A" else x
    )
    
    unique_cat = df["category_clean"].nunique()
    print(f"[INFO] Kategori berhasil dibersihkan: {unique_cat} kategori unik")
    
    return df


def clean_contact_info(df):
    """
    Membersihkan informasi kontak (phone, website)
    Mengganti N/A dengan NaN untuk konsistensi
    """
    # Phone
    df["has_phone"] = df["phone"].apply(
        lambda x: False if pd.isna(x) or x == "N/A" else True
    )
    df["phone_clean"] = df["phone"].apply(
        lambda x: np.nan if pd.isna(x) or x == "N/A" else x
    )
    
    # Website
    df["has_website"] = df["website"].apply(
        lambda x: False if pd.isna(x) or x == "N/A" else True
    )
    df["website_clean"] = df["website"].apply(
        lambda x: np.nan if pd.isna(x) or x == "N/A" else x
    )
    
    phone_count = df["has_phone"].sum()
    website_count = df["has_website"].sum()
    
    print(f"[INFO] Digital presence:")
    print(f"       - Dengan nomor telepon: {phone_count}/{len(df)} ({phone_count/len(df)*100:.1f}%)")
    print(f"       - Dengan website: {website_count}/{len(df)} ({website_count/len(df)*100:.1f}%)")
    
    return df


def remove_duplicates(df):
    """
    Menghapus data duplikat berdasarkan nama dan alamat
    """
    initial_count = len(df)
    
    # Hapus duplikat berdasarkan nama + alamat
    df_clean = df.drop_duplicates(subset=["name", "address"], keep="first")
    
    removed_count = initial_count - len(df_clean)
    print(f"[INFO] Duplikat dihapus: {removed_count} baris")
    
    return df_clean


def clean_name(df):
    """
    Membersihkan nama cafe yang N/A
    """
    df["name_clean"] = df["name"].apply(
        lambda x: "Cafe Tanpa Nama" if pd.isna(x) or x == "N/A" else x
    )
    
    na_count = (df["name"] == "N/A").sum() + df["name"].isna().sum()
    if na_count > 0:
        print(f"[INFO] Ditemukan {na_count} cafe tanpa nama")
    
    return df


def main():
    """Fungsi utama untuk menjalankan data cleaning"""
    print("=" * 60)
    print("DATA CLEANER - CAFE CIREBON")
    print("=" * 60)
    print()
    
    # Path ke file data
    project_root = Path(__file__).parent.parent
    input_path = project_root / "output" / "google_maps" / "gmaps_cafe_20260131_134158.csv"
    output_path = project_root / "analysis" / "reports" / "cleaned_cafe_cirebon.csv"
    
    # Muat data
    print("[STEP 1] Memuat data...")
    df = load_data(input_path)
    if df is None:
        return
    
    print()
    print("[STEP 2] Membersihkan data...")
    
    # Jalankan semua fungsi cleaning
    df = clean_name(df)
    df = clean_rating(df)
    df = parse_coordinates(df)
    df = extract_kecamatan(df)
    df = identify_wilayah(df)
    df = clean_category(df)
    df = clean_contact_info(df)
    df = remove_duplicates(df)
    
    print()
    print("[STEP 3] Menyimpan data bersih...")
    
    # Pilih kolom yang akan disimpan
    output_columns = [
        "index", "name", "name_clean", "category", "category_clean",
        "rating", "rating_clean", "total_reviews", "address",
        "kecamatan", "wilayah",
        "phone", "phone_clean", "has_phone",
        "website", "website_clean", "has_website",
        "hours", "coordinates", "latitude", "longitude",
        "scraped_at"
    ]
    
    # Filter kolom yang ada
    available_columns = [col for col in output_columns if col in df.columns]
    df_output = df[available_columns]
    
    # Simpan ke CSV
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_output.to_csv(output_path, index=False)
    
    print(f"[SUCCESS] Data bersih disimpan ke: {output_path}")
    print()
    
    # Tampilkan ringkasan akhir
    print("=" * 60)
    print("RINGKASAN DATA BERSIH")
    print("=" * 60)
    print(f"Total cafe       : {len(df_output)}")
    print(f"Kolom            : {len(df_output.columns)}")
    print(f"Rating rata-rata : {df_output['rating_clean'].mean():.2f}")
    print(f"Kecamatan unik   : {df_output['kecamatan'].nunique()}")
    print(f"Wilayah          : {df_output['wilayah'].value_counts().to_dict()}")
    print("=" * 60)
    
    return df_output


if __name__ == "__main__":
    main()
