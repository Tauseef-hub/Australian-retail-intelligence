from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

def fix_retail_sales_schema():
    """Fix the retail_sales table to handle larger numbers"""
    
    print("Fixing database schema...")
    
    connection_string = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    engine = create_engine(connection_string, pool_pre_ping=True)
    
    with engine.connect() as conn:
        # Modify the column to handle bigger numbers
        conn.execute(text("""
            ALTER TABLE retail_sales 
            ALTER COLUMN turnover_millions TYPE NUMERIC(20, 2);
        """))
        conn.commit()
        
        print("✅ Schema fixed! turnover_millions now supports larger values")
        
        # Check current data
        result = conn.execute(text("SELECT COUNT(*) FROM retail_sales"))
        count = result.fetchone()[0]
        print(f"Current records in database: {count:,}")

if __name__ == "__main__":
    fix_retail_sales_schema()