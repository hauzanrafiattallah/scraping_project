"""
EDA (Exploratory Data Analysis) - Data Cafe Cirebon
Script untuk analisis dan visualisasi data cafe di Kota/Kabupaten Cirebon
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings

# Konfigurasi matplotlib
warnings.filterwarnings("ignore")
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["font.size"] = 11
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.labelsize"] = 12

# Warna tema konsisten
COLORS = {
    "primary": "#2563EB",
    "secondary": "#7C3AED",
    "accent": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "gray": "#6B7280",
    "kota": "#3B82F6",
    "kabupaten": "#8B5CF6"
}

# Palette untuk chart
PALETTE_MAIN = ["#2563EB", "#7C3AED", "#10B981", "#F59E0B", "#EF4444", "#6366F1", "#EC4899"]


def load_cleaned_data(file_path):
    """Memuat data yang sudah dibersihkan"""
    try:
        df = pd.read_csv(file_path)
        print(f"[INFO] Data dimuat: {len(df)} cafe")
        return df
    except Exception as e:
        print(f"[ERROR] Gagal memuat data: {e}")
        return None


def print_overview(df):
    """Menampilkan overview statistik dasar"""
    print("\n" + "=" * 70)
    print("OVERVIEW DATA CAFE CIREBON")
    print("=" * 70)
    
    print(f"\n{'Metrik':<35} {'Nilai':>15}")
    print("-" * 50)
    print(f"{'Total Cafe':<35} {len(df):>15}")
    print(f"{'Kota Cirebon':<35} {len(df[df['wilayah'] == 'Kota Cirebon']):>15}")
    print(f"{'Kabupaten Cirebon':<35} {len(df[df['wilayah'] == 'Kabupaten Cirebon']):>15}")
    print(f"{'Kategori Unik':<35} {df['category_clean'].nunique():>15}")
    print(f"{'Kecamatan Unik':<35} {df['kecamatan'].nunique():>15}")
    
    print(f"\n{'Statistik Rating':<35}")
    print("-" * 50)
    print(f"{'Rata-rata Rating':<35} {df['rating_clean'].mean():>15.2f}")
    print(f"{'Median Rating':<35} {df['rating_clean'].median():>15.2f}")
    print(f"{'Rating Tertinggi':<35} {df['rating_clean'].max():>15.2f}")
    print(f"{'Rating Terendah':<35} {df['rating_clean'].min():>15.2f}")
    print(f"{'Std. Deviasi':<35} {df['rating_clean'].std():>15.2f}")
    
    print(f"\n{'Digital Presence':<35}")
    print("-" * 50)
    phone_pct = df['has_phone'].sum() / len(df) * 100
    website_pct = df['has_website'].sum() / len(df) * 100
    print(f"{'Cafe dengan Telepon':<35} {df['has_phone'].sum():>10} ({phone_pct:.1f}%)")
    print(f"{'Cafe dengan Website':<35} {df['has_website'].sum():>10} ({website_pct:.1f}%)")
    
    return None


def plot_rating_distribution(df, output_dir):
    """
    Visualisasi distribusi rating cafe
    Output: histogram rating dengan statistik
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Subplot 1: Histogram distribusi rating
    ax1 = axes[0]
    ratings = df["rating_clean"].dropna()
    
    ax1.hist(ratings, bins=10, color=COLORS["primary"], edgecolor="white", alpha=0.8)
    ax1.axvline(ratings.mean(), color=COLORS["danger"], linestyle="--", linewidth=2, 
                label=f"Rata-rata: {ratings.mean():.2f}")
    ax1.axvline(ratings.median(), color=COLORS["accent"], linestyle="-.", linewidth=2,
                label=f"Median: {ratings.median():.2f}")
    
    ax1.set_xlabel("Rating")
    ax1.set_ylabel("Jumlah Cafe")
    ax1.set_title("Distribusi Rating Cafe di Cirebon")
    ax1.legend(loc="upper left")
    
    # Subplot 2: Rating per wilayah (boxplot)
    ax2 = axes[1]
    wilayah_order = ["Kota Cirebon", "Kabupaten Cirebon"]
    colors_wilayah = [COLORS["kota"], COLORS["kabupaten"]]
    
    bp = ax2.boxplot(
        [df[df["wilayah"] == w]["rating_clean"].dropna() for w in wilayah_order],
        labels=wilayah_order,
        patch_artist=True
    )
    
    for patch, color in zip(bp["boxes"], colors_wilayah):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax2.set_ylabel("Rating")
    ax2.set_title("Perbandingan Rating: Kota vs Kabupaten Cirebon")
    
    # Tambahkan mean points
    for i, w in enumerate(wilayah_order):
        mean_val = df[df["wilayah"] == w]["rating_clean"].mean()
        ax2.scatter(i + 1, mean_val, marker="D", color=COLORS["danger"], s=80, 
                   zorder=10, label="Rata-rata" if i == 0 else "")
    ax2.legend()
    
    plt.tight_layout()
    
    # Simpan plot
    output_path = output_dir / "01_rating_distribution.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    
    print(f"[PLOT] Rating distribution disimpan: {output_path.name}")
    
    return None


def plot_cafe_by_kecamatan(df, output_dir):
    """
    Visualisasi jumlah cafe per kecamatan
    Output: horizontal bar chart
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Hitung cafe per kecamatan
    kec_counts = df["kecamatan"].value_counts()
    
    # Buat warna berdasarkan wilayah
    kec_wilayah = df.groupby("kecamatan")["wilayah"].first()
    colors = [COLORS["kota"] if kec_wilayah.get(k) == "Kota Cirebon" else COLORS["kabupaten"] 
              for k in kec_counts.index]
    
    # Plot horizontal bar
    bars = ax.barh(range(len(kec_counts)), kec_counts.values, color=colors, alpha=0.8)
    
    # Labels
    ax.set_yticks(range(len(kec_counts)))
    ax.set_yticklabels(kec_counts.index)
    ax.set_xlabel("Jumlah Cafe")
    ax.set_title("Distribusi Cafe per Kecamatan di Cirebon")
    
    # Tambahkan nilai di ujung bar
    for i, (bar, val) in enumerate(zip(bars, kec_counts.values)):
        ax.text(val + 0.2, i, str(val), va="center", fontsize=10, fontweight="bold")
    
    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=COLORS["kota"], alpha=0.8, label="Kota Cirebon"),
        Patch(facecolor=COLORS["kabupaten"], alpha=0.8, label="Kabupaten Cirebon")
    ]
    ax.legend(handles=legend_elements, loc="lower right")
    
    ax.invert_yaxis()  # Kecamatan dengan cafe terbanyak di atas
    plt.tight_layout()
    
    # Simpan plot
    output_path = output_dir / "02_cafe_by_kecamatan.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    
    print(f"[PLOT] Cafe by kecamatan disimpan: {output_path.name}")
    
    return None


def plot_category_distribution(df, output_dir):
    """
    Visualisasi distribusi kategori bisnis cafe
    Output: pie chart dan bar chart
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Data kategori
    cat_counts = df["category_clean"].value_counts()
    
    # Subplot 1: Pie chart
    ax1 = axes[0]
    colors = PALETTE_MAIN[:len(cat_counts)]
    
    wedges, texts, autotexts = ax1.pie(
        cat_counts.values, 
        labels=None,
        autopct=lambda pct: f"{pct:.1f}%" if pct > 5 else "",
        colors=colors,
        startangle=90,
        pctdistance=0.75
    )
    
    # Legend di samping
    ax1.legend(
        wedges, 
        [f"{cat} ({count})" for cat, count in cat_counts.items()],
        title="Kategori",
        loc="center left",
        bbox_to_anchor=(0.95, 0.5)
    )
    ax1.set_title("Proporsi Kategori Cafe")
    
    # Subplot 2: Bar chart dengan rating rata-rata
    ax2 = axes[1]
    
    # Hitung rata-rata rating per kategori
    cat_rating = df.groupby("category_clean")["rating_clean"].agg(["mean", "count"])
    cat_rating = cat_rating.sort_values("mean", ascending=True)
    
    bars = ax2.barh(range(len(cat_rating)), cat_rating["mean"], color=COLORS["primary"], alpha=0.8)
    
    ax2.set_yticks(range(len(cat_rating)))
    ax2.set_yticklabels(cat_rating.index)
    ax2.set_xlabel("Rata-rata Rating")
    ax2.set_title("Rating Rata-rata per Kategori")
    ax2.set_xlim(3.5, 5.0)
    
    # Tambahkan nilai
    for i, (bar, val, count) in enumerate(zip(bars, cat_rating["mean"], cat_rating["count"])):
        ax2.text(val + 0.02, i, f"{val:.2f} (n={count})", va="center", fontsize=9)
    
    plt.tight_layout()
    
    # Simpan plot
    output_path = output_dir / "03_category_distribution.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    
    print(f"[PLOT] Category distribution disimpan: {output_path.name}")
    
    return None


def plot_kota_vs_kabupaten(df, output_dir):
    """
    Visualisasi perbandingan Kota Cirebon vs Kabupaten Cirebon
    Output: multiple metrics comparison
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Data per wilayah
    kota = df[df["wilayah"] == "Kota Cirebon"]
    kabupaten = df[df["wilayah"] == "Kabupaten Cirebon"]
    wilayah_labels = ["Kota Cirebon", "Kabupaten Cirebon"]
    wilayah_colors = [COLORS["kota"], COLORS["kabupaten"]]
    
    # Subplot 1: Jumlah cafe
    ax1 = axes[0, 0]
    counts = [len(kota), len(kabupaten)]
    bars = ax1.bar(wilayah_labels, counts, color=wilayah_colors, alpha=0.8)
    ax1.set_ylabel("Jumlah Cafe")
    ax1.set_title("Jumlah Cafe per Wilayah")
    for bar, val in zip(bars, counts):
        ax1.text(bar.get_x() + bar.get_width()/2, val + 0.5, str(val), 
                ha="center", fontweight="bold", fontsize=12)
    
    # Subplot 2: Rating rata-rata
    ax2 = axes[0, 1]
    ratings = [kota["rating_clean"].mean(), kabupaten["rating_clean"].mean()]
    bars = ax2.bar(wilayah_labels, ratings, color=wilayah_colors, alpha=0.8)
    ax2.set_ylabel("Rata-rata Rating")
    ax2.set_title("Rata-rata Rating per Wilayah")
    ax2.set_ylim(4.0, 5.0)
    for bar, val in zip(bars, ratings):
        ax2.text(bar.get_x() + bar.get_width()/2, val + 0.02, f"{val:.2f}", 
                ha="center", fontweight="bold", fontsize=12)
    
    # Subplot 3: Digital presence (stacked bar)
    ax3 = axes[1, 0]
    
    kota_phone = kota["has_phone"].mean() * 100
    kota_website = kota["has_website"].mean() * 100
    kab_phone = kabupaten["has_phone"].mean() * 100
    kab_website = kabupaten["has_website"].mean() * 100
    
    x = np.arange(2)
    width = 0.35
    
    bars1 = ax3.bar(x - width/2, [kota_phone, kab_phone], width, label="Telepon", 
                    color=COLORS["primary"], alpha=0.8)
    bars2 = ax3.bar(x + width/2, [kota_website, kab_website], width, label="Website",
                    color=COLORS["accent"], alpha=0.8)
    
    ax3.set_ylabel("Persentase (%)")
    ax3.set_title("Digital Presence per Wilayah")
    ax3.set_xticks(x)
    ax3.set_xticklabels(wilayah_labels)
    ax3.legend()
    ax3.set_ylim(0, 100)
    
    # Subplot 4: Top categories per wilayah
    ax4 = axes[1, 1]
    
    kota_cats = kota["category_clean"].value_counts().head(3)
    kab_cats = kabupaten["category_clean"].value_counts().head(3)
    
    # Buat text summary
    text_kota = "KOTA CIREBON\n" + "-" * 20 + "\n"
    for cat, count in kota_cats.items():
        text_kota += f"{cat}: {count}\n"
    
    text_kab = "\nKABUPATEN CIREBON\n" + "-" * 20 + "\n"
    for cat, count in kab_cats.items():
        text_kab += f"{cat}: {count}\n"
    
    ax4.text(0.1, 0.9, text_kota, transform=ax4.transAxes, fontsize=11,
             verticalalignment="top", fontfamily="monospace",
             bbox=dict(boxstyle="round", facecolor=COLORS["kota"], alpha=0.2))
    ax4.text(0.55, 0.9, text_kab, transform=ax4.transAxes, fontsize=11,
             verticalalignment="top", fontfamily="monospace",
             bbox=dict(boxstyle="round", facecolor=COLORS["kabupaten"], alpha=0.2))
    
    ax4.set_title("Top 3 Kategori per Wilayah")
    ax4.axis("off")
    
    plt.tight_layout()
    
    # Simpan plot
    output_path = output_dir / "04_kota_vs_kabupaten.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    
    print(f"[PLOT] Kota vs Kabupaten disimpan: {output_path.name}")
    
    return None


def plot_digital_presence(df, output_dir):
    """
    Visualisasi analisis digital presence cafe
    Output: pie charts dan bar chart
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Subplot 1: Pie chart - Telepon
    ax1 = axes[0]
    phone_data = [df["has_phone"].sum(), (~df["has_phone"]).sum()]
    colors_phone = [COLORS["accent"], COLORS["gray"]]
    
    wedges, _, autotexts = ax1.pie(
        phone_data,
        labels=["Ada Telepon", "Tidak Ada"],
        autopct="%1.1f%%",
        colors=colors_phone,
        startangle=90
    )
    ax1.set_title("Ketersediaan Nomor Telepon")
    
    # Subplot 2: Pie chart - Website
    ax2 = axes[1]
    website_data = [df["has_website"].sum(), (~df["has_website"]).sum()]
    colors_website = [COLORS["primary"], COLORS["gray"]]
    
    wedges, _, autotexts = ax2.pie(
        website_data,
        labels=["Ada Website", "Tidak Ada"],
        autopct="%1.1f%%",
        colors=colors_website,
        startangle=90
    )
    ax2.set_title("Ketersediaan Website")
    
    # Subplot 3: Digital maturity score
    ax3 = axes[2]
    
    # Hitung skor digital maturity
    df_temp = df.copy()
    df_temp["digital_score"] = df_temp["has_phone"].astype(int) + df_temp["has_website"].astype(int)
    
    score_counts = df_temp["digital_score"].value_counts().sort_index()
    score_labels = {0: "Tidak Ada\nKeduanya", 1: "Salah Satu", 2: "Keduanya\nLengkap"}
    
    bars = ax3.bar(
        [score_labels.get(i, str(i)) for i in score_counts.index],
        score_counts.values,
        color=[COLORS["danger"], COLORS["warning"], COLORS["accent"]],
        alpha=0.8
    )
    
    ax3.set_ylabel("Jumlah Cafe")
    ax3.set_title("Tingkat Kelengkapan Digital")
    
    for bar, val in zip(bars, score_counts.values):
        pct = val / len(df) * 100
        ax3.text(bar.get_x() + bar.get_width()/2, val + 0.5, f"{val}\n({pct:.1f}%)", 
                ha="center", fontsize=10)
    
    plt.tight_layout()
    
    # Simpan plot
    output_path = output_dir / "05_digital_presence.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    
    print(f"[PLOT] Digital presence disimpan: {output_path.name}")
    
    return None


def plot_geo_scatter(df, output_dir):
    """
    Visualisasi peta scatter plot lokasi cafe
    Output: scatter plot koordinat dengan warna per wilayah
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Filter data dengan koordinat valid
    df_geo = df[df["latitude"].notna() & df["longitude"].notna()].copy()
    
    # Plot per wilayah
    for wilayah, color in [("Kota Cirebon", COLORS["kota"]), ("Kabupaten Cirebon", COLORS["kabupaten"])]:
        data = df_geo[df_geo["wilayah"] == wilayah]
        ax.scatter(
            data["longitude"], 
            data["latitude"],
            c=color,
            s=data["rating_clean"] * 30,  # Ukuran berdasarkan rating
            alpha=0.6,
            label=f"{wilayah} (n={len(data)})",
            edgecolors="white",
            linewidth=0.5
        )
    
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("Peta Sebaran Lokasi Cafe di Cirebon\n(Ukuran titik = Rating)")
    ax.legend(loc="upper right")
    
    # Grid
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Simpan plot
    output_path = output_dir / "06_geo_scatter.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    
    print(f"[PLOT] Geo scatter disimpan: {output_path.name}")
    
    return None


def plot_top_rated_cafes(df, output_dir):
    """
    Visualisasi top cafe dengan rating tertinggi
    Output: horizontal bar chart top 15 cafe
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Ambil top 15 cafe berdasarkan rating
    top_cafes = df.nlargest(15, "rating_clean")[["name_clean", "rating_clean", "wilayah", "kecamatan"]]
    top_cafes = top_cafes.iloc[::-1]  # Reverse untuk display
    
    # Warna berdasarkan wilayah
    colors = [COLORS["kota"] if w == "Kota Cirebon" else COLORS["kabupaten"] 
              for w in top_cafes["wilayah"]]
    
    # Plot horizontal bar
    bars = ax.barh(range(len(top_cafes)), top_cafes["rating_clean"], color=colors, alpha=0.8)
    
    # Labels - nama cafe dengan kecamatan
    labels = [f"{name[:30]}..." if len(name) > 30 else name 
              for name in top_cafes["name_clean"]]
    ax.set_yticks(range(len(top_cafes)))
    ax.set_yticklabels(labels)
    ax.set_xlabel("Rating")
    ax.set_title("Top 15 Cafe dengan Rating Tertinggi di Cirebon")
    ax.set_xlim(4.0, 5.2)
    
    # Tambahkan rating dan kecamatan di ujung bar
    for i, (bar, rating, kec) in enumerate(zip(bars, top_cafes["rating_clean"], top_cafes["kecamatan"])):
        ax.text(rating + 0.02, i, f"{rating:.1f} | {kec}", va="center", fontsize=9)
    
    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=COLORS["kota"], alpha=0.8, label="Kota Cirebon"),
        Patch(facecolor=COLORS["kabupaten"], alpha=0.8, label="Kabupaten Cirebon")
    ]
    ax.legend(handles=legend_elements, loc="lower right")
    
    plt.tight_layout()
    
    # Simpan plot
    output_path = output_dir / "07_top_rated_cafes.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    
    print(f"[PLOT] Top rated cafes disimpan: {output_path.name}")
    
    return None


def generate_insights(df):
    """Menghasilkan key insights dari data"""
    print("\n" + "=" * 70)
    print("KEY INSIGHTS - CAFE CIREBON")
    print("=" * 70)
    
    # Insight 1: Distribusi wilayah
    kota_count = len(df[df["wilayah"] == "Kota Cirebon"])
    kab_count = len(df[df["wilayah"] == "Kabupaten Cirebon"])
    
    print(f"\n[1] DISTRIBUSI WILAYAH")
    print(f"    Kota Cirebon memiliki {kota_count} cafe ({kota_count/len(df)*100:.1f}%)")
    print(f"    Kabupaten Cirebon memiliki {kab_count} cafe ({kab_count/len(df)*100:.1f}%)")
    if kota_count > kab_count:
        print(f"    -> Cafe lebih terkonsentrasi di wilayah kota")
    
    # Insight 2: Rating
    high_rating = len(df[df["rating_clean"] >= 4.5])
    print(f"\n[2] KUALITAS CAFE")
    print(f"    {high_rating} cafe ({high_rating/len(df)*100:.1f}%) memiliki rating >= 4.5")
    print(f"    Rating rata-rata: {df['rating_clean'].mean():.2f}")
    
    # Insight 3: Kecamatan terpopuler
    top_kec = df["kecamatan"].value_counts().head(3)
    print(f"\n[3] KECAMATAN DENGAN CAFE TERBANYAK")
    for i, (kec, count) in enumerate(top_kec.items(), 1):
        print(f"    {i}. {kec}: {count} cafe")
    
    # Insight 4: Kategori dominan
    top_cat = df["category_clean"].value_counts().head(1)
    print(f"\n[4] KATEGORI DOMINAN")
    print(f"    '{top_cat.index[0]}' adalah kategori terbanyak dengan {top_cat.values[0]} cafe")
    
    # Insight 5: Digital presence
    phone_pct = df["has_phone"].sum() / len(df) * 100
    website_pct = df["has_website"].sum() / len(df) * 100
    print(f"\n[5] DIGITAL PRESENCE")
    print(f"    {phone_pct:.1f}% cafe memiliki nomor telepon yang tersedia")
    print(f"    {website_pct:.1f}% cafe memiliki website/link")
    if phone_pct > website_pct:
        print(f"    -> Cafe lebih banyak mencantumkan telepon daripada website")
    
    # Insight 6: Top rated cafe
    top_cafe = df.nlargest(1, "rating_clean").iloc[0]
    print(f"\n[6] CAFE TERBAIK")
    print(f"    '{top_cafe['name_clean']}' dengan rating {top_cafe['rating_clean']:.1f}")
    print(f"    Lokasi: {top_cafe['kecamatan']}, {top_cafe['wilayah']}")
    
    # Insight 7: Perbandingan rating Kota vs Kabupaten
    kota_rating = df[df["wilayah"] == "Kota Cirebon"]["rating_clean"].mean()
    kab_rating = df[df["wilayah"] == "Kabupaten Cirebon"]["rating_clean"].mean()
    print(f"\n[7] PERBANDINGAN RATING WILAYAH")
    print(f"    Rating rata-rata Kota Cirebon: {kota_rating:.2f}")
    print(f"    Rating rata-rata Kabupaten Cirebon: {kab_rating:.2f}")
    if kota_rating > kab_rating:
        print(f"    -> Cafe di Kota Cirebon cenderung memiliki rating lebih tinggi")
    else:
        print(f"    -> Cafe di Kabupaten Cirebon cenderung memiliki rating lebih tinggi")
    
    print("\n" + "=" * 70)
    
    return None


def main():
    """Fungsi utama menjalankan EDA"""
    print("=" * 70)
    print("EDA - DATA CAFE CIREBON")
    print("Exploratory Data Analysis")
    print("=" * 70)
    
    # Path setup
    project_root = Path(__file__).parent.parent
    data_path = project_root / "analysis" / "reports" / "cleaned_cafe_cirebon.csv"
    output_dir = project_root / "analysis" / "visualizations" / "cafe_eda"
    
    # Buat folder output jika belum ada
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Muat data
    print("\n[STEP 1] Memuat data...")
    df = load_cleaned_data(data_path)
    if df is None:
        print("[ERROR] Gagal memuat data. Jalankan data_cleaner.py terlebih dahulu.")
        return
    
    # Tampilkan overview
    print("\n[STEP 2] Menampilkan overview...")
    print_overview(df)
    
    # Generate visualisasi
    print("\n[STEP 3] Membuat visualisasi...")
    plot_rating_distribution(df, output_dir)
    plot_cafe_by_kecamatan(df, output_dir)
    plot_category_distribution(df, output_dir)
    plot_kota_vs_kabupaten(df, output_dir)
    plot_digital_presence(df, output_dir)
    plot_geo_scatter(df, output_dir)
    plot_top_rated_cafes(df, output_dir)
    
    # Generate insights
    print("\n[STEP 4] Menghasilkan insights...")
    generate_insights(df)
    
    print(f"\n[SUCCESS] EDA selesai!")
    print(f"[INFO] Visualisasi tersimpan di: {output_dir}")
    print(f"[INFO] Total {len(list(output_dir.glob('*.png')))} file PNG dibuat")
    
    return df


if __name__ == "__main__":
    main()
