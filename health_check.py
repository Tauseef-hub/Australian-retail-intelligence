from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

print("="*70)
print("HEALTH CHECK - AUSTRALIAN RETAIL INTELLIGENCE")
print("="*70)

# Database connection
try:
    connection_string = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    engine = create_engine(connection_string, pool_pre_ping=True)
    
    with engine.connect() as conn:
        # Test connection
        conn.execute(text("SELECT 1"))
        print("\n✅ DATABASE CONNECTION: SUCCESS")
        
        # Check tables
        print("\n📊 TABLE STATUS:")
        tables = ['retail_sales', 'sales_forecasts', 'state_mapping', 'category_mapping']
        for table in tables:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = result.fetchone()[0]
            print(f"   ✅ {table}: {count:,} records")
        
        # Check mappings
        print("\n🗺️  STATE MAPPINGS:")
        result = conn.execute(text("SELECT state_code, state_name FROM state_mapping ORDER BY state_code"))
        for row in result:
            print(f"   {row[0]} → {row[1]}")
        
        print("\n📦 CATEGORY MAPPINGS (first 5):")
        result = conn.execute(text("SELECT category_code, category_name FROM category_mapping ORDER BY category_code LIMIT 5"))
        for row in result:
            print(f"   {row[0]} → {row[1]}")
        
except Exception as e:
    print(f"\n❌ DATABASE ERROR: {str(e)}")

print("\n" + "="*70)