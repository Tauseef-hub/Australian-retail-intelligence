import pandas as pd

# Load the transformed data
df = pd.read_csv('data/abs_transformed_full.csv')

print("Checking turnover_millions column...")
print(f"Max value: {df['turnover_millions'].max()}")
print(f"Min value: {df['turnover_millions'].min()}")
print(f"Data type: {df['turnover_millions'].dtype}")

# Find problematic values
large_values = df[df['turnover_millions'] > 99999]
print(f"\nRecords with turnover > 99,999: {len(large_values)}")

if len(large_values) > 0:
    print("\nSample large values:")
    print(large_values[['sale_date', 'category', 'state', 'turnover_millions']].head(10))