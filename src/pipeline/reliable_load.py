import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extract.abs_api import ABSRetailDataExtractor
from transform.clean_retail_data import RetailDataTransformer
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def load_with_smaller_batches():
    """ETL with very small batch sizes to avoid parameter limits"""
    
    print("="*70)
    print("RELIABLE ETL PIPELINE (Small Batches)")
    print("="*70)
    
    start_time = datetime.now()
    
    # Step 1: Extract (just 2024 data to start)
    print("\nStep 1: Extracting 2024 data...")
    extractor = ABSRetailDataExtractor()
    df_raw = extractor.extract_retail_sales(start_date='2024-01', end_date='2024-12')
    
    if df_raw is None or len(df_raw) == 0:
        print("No data extracted")
        return
    
    print(f"✅ Extracted: {len(df_raw):,} records")
    
    # Step 2: Transform
    print("\nStep 2: Transforming...")
    transformer = RetailDataTransformer()
    df_clean = transformer.transform(df_raw)
    
    # Remove duplicates
    before = len(df_clean)
    df_clean = df_clean.drop_duplicates(subset=['sale_date', 'category', 'state'], keep='first')
    after = len(df_clean)
    
    if before != after:
        print(f"⚠️ Removed {before - after:,} duplicates")
    
    print(f"✅ Final clean records: {len(df_clean):,}")
    
    # Step 3: Load with VERY small batches
    print("\nStep 3: Loading to database (batch size=100)...")
    
    connection_string = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    engine = create_engine(connection_string, pool_pre_ping=True)
    
    # Use VERY small batches (100 records at a time)
    batch_size = 100
    total_loaded = 0
    failed_batches = 0
    
    for i in range(0, len(df_clean), batch_size):
        batch = df_clean.iloc[i:i+batch_size]
        
        try:
            batch.to_sql('retail_sales', engine, if_exists='append', index=False, method='multi', chunksize=10)
            total_loaded += len(batch)
            
            if total_loaded % 500 == 0:
                print(f"  ✓ Loaded {total_loaded:,}/{len(df_clean):,} records...")
                
        except Exception as e:
            failed_batches += 1
            print(f"  ✗ Failed batch at row {i}: {str(e)[:100]}")
            if failed_batches > 5:
                print("Too many failures, stopping")
                break
    
    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds()
    
    # Check final count
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM retail_sales"))
        final_count = result.fetchone()[0]
    
    print("\n" + "="*70)
    print("✅ ETL COMPLETE!")
    print("="*70)
    print(f"Records loaded this run: {total_loaded:,}")
    print(f"Total records in database: {final_count:,}")
    print(f"Execution time: {execution_time:.2f} seconds")
    print(f"Failed batches: {failed_batches}")

if __name__ == "__main__":
    load_with_smaller_batches()