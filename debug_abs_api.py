import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.extract.abs_api import ABSRetailDataExtractor
import pandas as pd

print("="*70)
print("DEBUGGING ABS API RAW DATA")
print("="*70)

extractor = ABSRetailDataExtractor()

# Extract just 2024 data for category 20
df_raw = extractor.extract_retail_sales(start_date='2024-01', end_date='2024-12')

if df_raw is not None:
    print(f"\nTotal raw records: {len(df_raw):,}")
    print(f"\nColumns: {list(df_raw.columns)}")
    
    # Filter for what should be category 20, state AUS
    print("\n" + "="*70)
    print("SAMPLE RAW DATA FOR 2024:")
    print("="*70)
    print(df_raw.head(50))
    
    # Check unique values
    print("\n" + "="*70)
    print("UNIQUE VALUES:")
    print("="*70)
    if 'INDUSTRY' in df_raw.columns:
        print(f"\nUnique INDUSTRY values: {sorted(df_raw['INDUSTRY'].unique())}")
    if 'REGION' in df_raw.columns:
        print(f"\nUnique REGION values: {sorted(df_raw['REGION'].unique())}")
    if 'TIME_PERIOD' in df_raw.columns:
        print(f"\nUnique TIME_PERIOD values: {sorted(df_raw['TIME_PERIOD'].unique())[:12]}")
    
    # Check OBS_VALUE for the quarterly spike pattern
    if 'INDUSTRY' in df_raw.columns and 'REGION' in df_raw.columns:
        # Filter to category 20 equivalent and AUS
        print("\n" + "="*70)
        print("CATEGORY 20 (Total Retail), STATE AUS - RAW VALUES:")
        print("="*70)
        
        # Try to find the right codes
        sample = df_raw[
            (df_raw['TIME_PERIOD'].str.startswith('2024')) 
        ].sort_values('TIME_PERIOD')
        
        print(sample[['TIME_PERIOD', 'INDUSTRY', 'REGION', 'OBS_VALUE']].head(30))
    
    # Save for inspection
    df_raw.to_csv('debug_raw_2024.csv', index=False)
    print("\n📁 Saved to: debug_raw_2024.csv")
    
else:
    print("❌ Failed to extract data")