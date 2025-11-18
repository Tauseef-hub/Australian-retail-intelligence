import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from src.transform.clean_retail_data import RetailDataTransformer

print("="*70)
print("TESTING TRANSFORMATION ON 2024 DATA")
print("="*70)

# Load the raw data we just saved
df_raw = pd.read_csv('debug_raw_2024.csv')

print(f"\nRaw data: {len(df_raw):,} records")

# Transform it
transformer = RetailDataTransformer()
df_clean = transformer.transform(df_raw)

print(f"\nCleaned data: {len(df_clean):,} records")

# Check category 20, state AUS
print("\n" + "="*70)
print("CATEGORY 20, STATE AUS - AFTER TRANSFORMATION:")
print("="*70)

cat20 = df_clean[(df_clean['category'] == '20') & (df_clean['state'] == 'AUS')].sort_values('sale_date')

if len(cat20) > 0:
    print(cat20[['sale_date', 'turnover_millions']].to_string(index=False))
    
    print(f"\n\nSTATISTICS:")
    print(f"Records: {len(cat20)}")
    print(f"Mean: {cat20['turnover_millions'].mean():,.2f}")
    print(f"Std Dev: {cat20['turnover_millions'].std():,.2f}")
    print(f"Min: {cat20['turnover_millions'].min():,.2f}")
    print(f"Max: {cat20['turnover_millions'].max():,.2f}")
else:
    print("❌ No category 20, state AUS found after transformation!")
    
    # Show what categories DO exist
    print("\n Categories found:")
    print(df_clean.groupby('category')['turnover_millions'].count())
    
    print("\n States found:")
    print(df_clean.groupby('state')['turnover_millions'].count())

# Save for inspection
df_clean.to_csv('debug_transformed_2024.csv', index=False)
print("\n📁 Saved to: debug_transformed_2024.csv")