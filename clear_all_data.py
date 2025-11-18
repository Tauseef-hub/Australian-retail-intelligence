from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

def clear_all_data():
    """Delete ALL data from retail_sales and sales_forecasts tables"""
    
    print("="*70)
    print("⚠️  WARNING: DELETING ALL DATA!")
    print("="*70)
    print("\nThis will delete:")
    print("  - All historical retail sales data")
    print("  - All forecasts")
    print("\nYou will need to re-run the full ETL pipeline after this.")
    
    confirm = input("\nType 'DELETE' to confirm: ")
    
    if confirm != 'DELETE':
        print("❌ Cancelled")
        return False
    
    connection_string = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    engine = create_engine(connection_string, pool_pre_ping=True)
    
    with engine.connect() as conn:
        # Count records before deletion
        result = conn.execute(text("SELECT COUNT(*) FROM retail_sales"))
        sales_count = result.fetchone()[0]
        
        result = conn.execute(text("SELECT COUNT(*) FROM sales_forecasts"))
        forecast_count = result.fetchone()[0]
        
        print(f"\n📊 Current data:")
        print(f"   Historical sales: {sales_count:,} records")
        print(f"   Forecasts: {forecast_count:,} records")
        
        # Delete everything
        print(f"\n🗑️ Deleting all data...")
        conn.execute(text("DELETE FROM sales_forecasts"))
        conn.execute(text("DELETE FROM retail_sales"))
        conn.commit()
        
        print("✅ All data deleted successfully!")
        return True

if __name__ == "__main__":
    if clear_all_data():
        print("\n" + "="*70)
        print("NEXT STEPS:")
        print("="*70)
        print("1. Run: python src/pipeline/full_etl_pipeline.py")
        print("2. Run: python src/forecast/forecast_all_categories.py")
        print("3. Refresh Power BI")