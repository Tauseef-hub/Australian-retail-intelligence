from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

connection_string = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
engine = create_engine(connection_string)

# Check historical data for category 20, state AUS
query = """
    SELECT sale_date, turnover_millions, growth_rate_yoy
    FROM retail_sales
    WHERE category='20' AND state='AUS'
    ORDER BY sale_date DESC
    LIMIT 24
"""

df = pd.read_sql(query, engine)

print("\nLAST 24 MONTHS OF HISTORICAL DATA (Category 20, AUS):")
print("="*60)
print(df.to_string(index=False))

print(f"\n\nSTATISTICS:")
print(f"Mean: {df['turnover_millions'].mean():,.2f}")
print(f"Std Dev: {df['turnover_millions'].std():,.2f}")
print(f"Min: {df['turnover_millions'].min():,.2f}")
print(f"Max: {df['turnover_millions'].max():,.2f}")

# Check for negatives or zeros
negatives = df[df['turnover_millions'] <= 0]
if len(negatives) > 0:
    print(f"\n⚠️ WARNING: Found {len(negatives)} records with zero or negative values!")
    print(negatives)
else:
    print("\n✅ No negative or zero values in historical data")

# Check for missing data
print(f"\nTotal historical records for category 20, state AUS:")
total_query = """
    SELECT COUNT(*) 
    FROM retail_sales 
    WHERE category='20' AND state='AUS'
"""
result = pd.read_sql(total_query, engine)
print(f"  {result.iloc[0, 0]:,} records")