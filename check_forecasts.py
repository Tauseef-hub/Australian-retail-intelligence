from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

connection_string = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
engine = create_engine(connection_string)

with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT forecast_date, state, category, predicted_turnover 
        FROM sales_forecasts 
        WHERE state='AUS' 
        ORDER BY forecast_date 
        LIMIT 10
    """))
    
    print("\nAUSTRALIA NATIONAL FORECASTS:")
    print("="*60)
    print(f"{'Date':<12} {'Category':<10} {'Predicted ($M)':<15}")
    print("-"*60)
    
    for row in result:
        print(f"{str(row[0]):<12} {row[2]:<10} ${row[3]:>10,.2f}")