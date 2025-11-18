# check_total_forecasts.py
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
    # Total forecasts
    result = conn.execute(text("SELECT COUNT(*) FROM sales_forecasts"))
    total = result.fetchone()[0]
    print(f"Total forecast records: {total:,}")
    
    # By category and state
    result = conn.execute(text("""
        SELECT category, state, COUNT(*) as cnt
        FROM sales_forecasts
        WHERE category='20' AND state='AUS'
        GROUP BY category, state
    """))
    
    print("\nCategory 20, State AUS:")
    for row in result:
        print(f"  {row[0]}, {row[1]}: {row[2]} records")
    
    # Show if there are duplicates
    result = conn.execute(text("""
        SELECT forecast_date, COUNT(*) as cnt
        FROM sales_forecasts
        WHERE category='20' AND state='AUS'
        GROUP BY forecast_date
        HAVING COUNT(*) > 1
    """))
    
    print("\nDuplicate dates (if any):")
    duplicates = list(result)
    if duplicates:
        for row in duplicates:
            print(f"  {row[0]}: {row[1]} records")
    else:
        print("  No duplicates found")