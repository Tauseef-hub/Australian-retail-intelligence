import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extract.abs_api import ABSRetailDataExtractor
from transform.clean_retail_data import RetailDataTransformer
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def simple_etl():
    """Simplified ETL - extract, transform, load in smaller chunks"""
    
    print("="*70)
    print("SIMPLIFIED ETL PIPELINE")
    print("="*70)
    
    start_time = datetime.now()
    
    # Step 1: Extract
    print("\nStep 1: Extracting data...")
    extractor = ABSRetailDataExtractor()
    df_raw = extractor.extract_retail_sales(start_date='2023-01', end_date='2024-12')
    
    if df_raw is None or len(df_raw) == 0:
        print("No data extracted")
        return
    
    print(f"Extracted: {len(df_raw):,} records")
    
    # Step 2: Transform
    print("\nStep 2: Transforming...")
    transformer = RetailDataTransformer()
    df_clean = transformer.transform(df_raw)
    
    # Remove duplicates
    before = len(df_clean)
    df_clean = df_clean.drop_duplicates(subset=['sale_date', 'category', 'state'], keep='first')
    after = len(df_clean)
    print(f"Removed {before - after:,} duplicates")
    print(f"Final records: {len(df_clean):,}")
    
    # Step 3: Load
    print("\nStep 3: Loading to database...")
    
    # Create engine
    connection_string = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    engine = create_engine(connection_string, pool_pre_ping=True)
    
    # Load in small batches
    batch_size = 1000
    total_loaded = 0
    
    for i in range(0, len(df_clean), batch_size):
        batch = df_clean.iloc[i:i+batch_size]
        batch.to_sql('retail_sales', engine, if_exists='append', index=False, method='multi')
        total_loaded += len(batch)
        print(f"  Loaded {total_loaded:,}/{len(df_clean):,} records...")
    
    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds()
    
    print("\n" + "="*70)
    print("✅ ETL COMPLETE!")
    print("="*70)
    print(f"Total records loaded: {total_loaded:,}")
    print(f"Execution time: {execution_time:.2f} seconds")

if __name__ == "__main__":
    simple_etl()