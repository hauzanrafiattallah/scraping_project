"""
Quick Analysis Script untuk Data Cafe Google Maps
Author: Data Analysis Team
Date: 2026-01-31

Script ini memberikan quick insights dari data scraping tanpa perlu Jupyter Notebook.
"""

import pandas as pd
import sys
from pathlib import Path


def load_data(file_path):
    """Load data dari CSV file"""
    try:
        df = pd.read_csv(file_path)
        print(f"✅ Data loaded successfully: {df.shape[0]} rows × {df.shape[1]} columns\n")
        return df
    except FileNotFoundError:
        print(f"❌ Error: File not found at {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        sys.exit(1)


def clean_data(df):
    """Basic data cleaning"""
    # Clean rating
    df['rating_clean'] = df['rating'].str.replace(',', '.').astype(float)
    
    # Split coordinates
    df[['latitude', 'longitude']] = df['coordinates'].str.split(',', expand=True)
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].astype(float)
    
    # Extract district
    df['district'] = df['address'].str.extract(r'Kec\. ([^,]+)')
    
    # Remove duplicates
    df_clean = df.drop_duplicates(subset=['name', 'address'], keep='first')
    
    print(f"🧹 Data cleaned: {len(df) - len(df_clean)} duplicates removed\n")
    return df_clean


def print_summary(df):
    """Print quick summary statistics"""
    print("=" * 80)
    print("📊 QUICK ANALYSIS SUMMARY - CAFE DATA KABUPATEN CIREBON")
    print("=" * 80)
    print()
    
    # Basic stats
    print(f"📈 BASIC STATISTICS:")
    print(f"   Total Cafes: {len(df)}")
    print(f"   Unique Categories: {df['category'].nunique()}")
    print(f"   Unique Districts: {df['district'].nunique()}")
    print()
    
    # Rating stats
    print(f"⭐ RATING STATISTICS:")
    print(f"   Average Rating: {df['rating_clean'].mean():.2f}")
    print(f"   Median Rating: {df['rating_clean'].median():.2f}")
    print(f"   Min Rating: {df['rating_clean'].min():.2f}")
    print(f"   Max Rating: {df['rating_clean'].max():.2f}")
    print(f"   Cafes with rating ≥ 4.5: {len(df[df['rating_clean'] >= 4.5])} ({len(df[df['rating_clean'] >= 4.5])/len(df)*100:.1f}%)")
    print()
    
    # Category distribution
    print(f"📊 TOP 5 CATEGORIES:")
    for idx, (category, count) in enumerate(df['category'].value_counts().head(5).items(), 1):
        print(f"   {idx}. {category}: {count} cafes ({count/len(df)*100:.1f}%)")
    print()
    
    # District distribution
    print(f"📍 TOP 5 DISTRICTS:")
    for idx, (district, count) in enumerate(df['district'].value_counts().head(5).items(), 1):
        print(f"   {idx}. {district}: {count} cafes")
    print()
    
    # Top rated cafes
    print(f"🏆 TOP 5 HIGHEST RATED CAFES:")
    top_5 = df.nlargest(5, 'rating_clean')[['name', 'rating_clean', 'category', 'district']]
    for idx, row in enumerate(top_5.itertuples(), 1):
        print(f"   {idx}. {row.name} - {row.rating_clean:.1f}⭐ ({row.category}, {row.district})")
    print()
    
    # Contact info
    phone_available = df['phone'].notna().sum()
    website_available = df['website'].notna().sum()
    print(f"📞 DIGITAL PRESENCE:")
    print(f"   Cafes with Phone: {phone_available} ({phone_available/len(df)*100:.1f}%)")
    print(f"   Cafes with Website: {website_available} ({website_available/len(df)*100:.1f}%)")
    print()
    
    print("=" * 80)
    print()
    print("💡 TIP: Run the Jupyter notebook for detailed analysis and visualizations!")
    print("   Command: jupyter notebook analysis/notebooks/eda_google_maps_cafe.ipynb")
    print()


def main():
    """Main function"""
    # Path to data
    data_path = Path(__file__).parent.parent / "output" / "google_maps" / "gmaps_cafe_20260131_134158.csv"
    
    print("\n🚀 Starting Quick Analysis...\n")
    
    # Load and clean data
    df = load_data(data_path)
    df_clean = clean_data(df)
    
    # Print summary
    print_summary(df_clean)
    
    # Save cleaned data
    output_path = Path(__file__).parent / "reports" / "cleaned_cafe_data.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(output_path, index=False)
    print(f"✅ Cleaned data saved to: {output_path}")
    print()


if __name__ == "__main__":
    main()
