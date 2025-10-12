from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

def rebuild_retail_sales_table():
    """Drop and recreate retail_sales table with proper schema"""
    
    print("⚠️  WARNING: This will delete all data in retail_sales table!")
    confirm = input("Type 'yes' to continue: ")
    
    if confirm.lower() != 'yes':
        print("Cancelled")
        return
    
    connection_string = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    engine = create_engine(connection_string, pool_pre_ping=True)
    
    with engine.connect() as conn:
        # Drop existing table
        print("\nDropping old table...")
        conn.execute(text("DROP TABLE IF EXISTS retail_sales CASCADE"))
        conn.commit()
        
        # Create new table with correct schema
        print("Creating new table with proper schema...")
        conn.execute(text("""
            CREATE TABLE retail_sales (
                sale_id SERIAL PRIMARY KEY,
                sale_date DATE NOT NULL,
                category VARCHAR(200),
                state VARCHAR(50),
                turnover_millions NUMERIC(20, 4),
                month_name VARCHAR(20),
                year INTEGER,
                growth_rate_yoy NUMERIC(10, 2),
                data_source VARCHAR(100) DEFAULT 'ABS_RT',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        conn.commit()
        
        # Create indexes
        print("Creating indexes...")
        conn.execute(text("CREATE INDEX idx_sale_date ON retail_sales(sale_date)"))
        conn.execute(text("CREATE INDEX idx_category ON retail_sales(category)"))
        conn.execute(text("CREATE INDEX idx_state ON retail_sales(state)"))
        conn.commit()
        
        print("\n✅ Table rebuilt successfully!")
        print("   - turnover_millions: NUMERIC(20, 4) - supports values up to 9,999,999,999,999,999.9999")

if __name__ == "__main__":
    rebuild_retail_sales_table()