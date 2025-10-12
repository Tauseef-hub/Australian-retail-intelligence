import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extract.abs_api import ABSRetailDataExtractor
from transform.clean_retail_data import RetailDataTransformer
from load.db_loader import DatabaseLoader
from datetime import datetime
import pandas as pd

def run_full_etl_pipeline():
    """
    Complete ETL pipeline: Extract ALL ABS data → Transform → Load to database
    """
    
    print("="*80)
    print("FULL ETL PIPELINE: AUSTRALIAN RETAIL INTELLIGENCE")
    print("="*80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    start_time = datetime.now()
    
    # Initialize components
    extractor = ABSRetailDataExtractor()
    transformer = RetailDataTransformer()
    loader = DatabaseLoader()
    
    # Step 1: EXTRACT
    print("\n" + "="*80)
    print("STEP 1: EXTRACT DATA FROM ABS API")
    print("="*80)
    
    # Extract from 2020 to present (to keep it manageable)
    # You can change dates to get more historical data
    df_raw = extractor.extract_retail_sales(
    start_date='1982-01',  # Changed from 2020 to 2010
    end_date='2024-12'
)
    
    if df_raw is None or len(df_raw) == 0:
        print("❌ Extraction failed or returned no data")
        return False
    
    print(f"\n✅ Extracted {len(df_raw):,} records")
    
    # Save raw data
    df_raw.to_csv('data/abs_raw_full.csv', index=False)
    print(f"📁 Saved raw data to: data/abs_raw_full.csv")
    
    # Step 2: TRANSFORM
    print("\n" + "="*80)
    print("STEP 2: TRANSFORM DATA")
    print("="*80)
    
    try:
        df_clean = transformer.transform(df_raw)
        print(f"\n✅ Transformed {len(df_clean):,} records")
        
        # Save transformed data
        df_clean.to_csv('data/abs_transformed_full.csv', index=False)
        print(f"📁 Saved transformed data to: data/abs_transformed_full.csv")
        
    except Exception as e:
        print(f"❌ Transformation failed: {e}")
        return False
    
    # Step 3: LOAD
    print("\n" + "="*80)
    print("STEP 3: LOAD DATA TO DATABASE")
    print("="*80)
    
    # Quality checks
    if not loader.verify_data_quality(df_clean):
        print("❌ Data quality checks failed")
        return False
    
    # Load to database
    success = loader.load_retail_sales(df_clean, batch_size=5000)
    
    if not success:
        print("❌ Load failed")
        return False
    
    # Calculate execution time
    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds()
    
    # Log the job
    loader.log_etl_job(
        job_name='full_etl_pipeline',
        status='SUCCESS',
        records_processed=len(df_raw),
        records_inserted=len(df_clean),
        execution_time=execution_time
    )
    
    # Summary
    print("\n" + "="*80)
    print("🎉 FULL ETL PIPELINE COMPLETE!")
    print("="*80)
    print(f"Extracted: {len(df_raw):,} raw records")
    print(f"Transformed: {len(df_clean):,} clean records")
    print(f"Loaded: {len(df_clean):,} records to database")
    print(f"Execution time: {execution_time:.2f} seconds ({execution_time/60:.2f} minutes)")
    print(f"Completed at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    return True

if __name__ == "__main__":
    success = run_full_etl_pipeline()
    
    if success:
        print("\n✅ Pipeline completed successfully!")
    else:
        print("\n❌ Pipeline failed!")