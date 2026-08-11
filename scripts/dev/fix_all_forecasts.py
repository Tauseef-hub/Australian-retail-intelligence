import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def clear_all_forecasts():
    """Delete ALL forecasts from database"""
    
    connection_string = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    engine = create_engine(connection_string)
    
    print("⚠️  WARNING: This will delete ALL forecasts!")
    confirm = input("Type 'yes' to continue: ")
    
    if confirm.lower() != 'yes':
        print("Cancelled")
        return
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM sales_forecasts"))
        count = result.fetchone()[0]
        print(f"\nDeleting {count:,} forecast records...")
        
        conn.execute(text("DELETE FROM sales_forecasts"))
        conn.commit()
        
        print("✅ All forecasts deleted!")

if __name__ == "__main__":
    clear_all_forecasts()