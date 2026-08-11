# check_m1_duplicates.py
import pandas as pd

df = pd.read_csv('data/abs_raw_full.csv')

print("="*70)
print("ANALYZING M1 DATA FOR DUPLICATES")
print("="*70)

print(f"\nTotal M1 records: {len(df):,}")
print(f"\nColumns: {list(df.columns)}")

# Check for duplicates by date/industry/region
print("\n" + "="*70)
print("CHECKING DUPLICATES FOR 2024-01, INDUSTRY 20, REGION AUS:")
print("="*70)

sample = df[
    (df['TIME_PERIOD'] == '2024-01') & 
    (df['INDUSTRY'] == 20) & 
    (df['REGION'] == 'AUS')
]

if len(sample) > 0:
    print(f"\nFound {len(sample)} records for this combination!")
    print("\nShowing all columns for these records:")
    print(sample.to_string())
else:
    print("No records found")