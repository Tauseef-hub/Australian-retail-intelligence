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

# Get Total Retail Trade forecasts for Australia
query = """
    SELECT forecast_date, predicted_turnover, lower_bound, upper_bound
    FROM sales_forecasts
    WHERE state='AUS' AND category='20'
    ORDER BY forecast_date
"""

df = pd.read_sql(query, engine)

print("\nTOTAL RETAIL TRADE FORECASTS (Australia):")
print("="*60)
print(df.to_string(index=False))
print(f"\nMean: {df['predicted_turnover'].mean():,.2f}")
print(f"Std Dev: {df['predicted_turnover'].std():,.2f}")
print(f"Min: {df['predicted_turnover'].min():,.2f}")
print(f"Max: {df['predicted_turnover'].max():,.2f}")