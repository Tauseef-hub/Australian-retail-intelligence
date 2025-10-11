from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import os
from datetime import datetime

load_dotenv()

class DatabaseLoader:
    """
    Load transformed data into PostgreSQL database
    """
    
    def __init__(self):
        self.engine = self._create_engine()
    
    def _create_engine(self):
        """Create database connection engine"""
        connection_string = (
            f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )
        return create_engine(connection_string, pool_pre_ping=True)
    
    def test_connection(self):
        """Verify database connection"""
        print("Testing database connection...")
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print("✅ Database connection successful!")
                return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def get_table_count(self, table_name):
        """Count existing records in table"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                count = result.fetchone()[0]
                return count
        except Exception as e:
            print(f"Error counting records: {e}")
            return 0
    
    def load_retail_sales(self, df, batch_size=1000):
        """
        Load retail sales data into database
        
        Parameters:
        - df: Transformed DataFrame
        - batch_size: Number of records to insert at once
        """
        print("="*70)
        print("LOADING DATA TO DATABASE")
        print("="*70)
        
        print(f"\nPreparing to load {len(df):,} records...")
        
        # Check current record count
        current_count = self.get_table_count('retail_sales')
        print(f"Current records in database: {current_count:,}")
        
        try:
            # Insert data in batches
            total_inserted = 0
            
            for i in range(0, len(df), batch_size):
                batch = df.iloc[i:i+batch_size]
                
                # Load to database
                batch.to_sql(
                    'retail_sales',
                    self.engine,
                    if_exists='append',
                    index=False,
                    method='multi'
                )
                
                total_inserted += len(batch)
                print(f"  Loaded batch: {total_inserted:,}/{len(df):,} records")
            
            # Verify insertion
            new_count = self.get_table_count('retail_sales')
            print(f"\n✅ LOAD COMPLETE!")
            print(f"   Records before: {current_count:,}")
            print(f"   Records after: {new_count:,}")
            print(f"   Records inserted: {new_count - current_count:,}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Load failed: {e}")
            return False
    
    def log_etl_job(self, job_name, status, records_processed, records_inserted, 
                    execution_time, error_message=None):
        """Log ETL job execution to etl_logs table"""
        
        log_data = pd.DataFrame([{
            'job_name': job_name,
            'status': status,
            'records_processed': records_processed,
            'records_inserted': records_inserted,
            'records_updated': 0,
            'error_message': error_message,
            'execution_time_seconds': execution_time,
            'completed_at': datetime.now()
        }])
        
        try:
            log_data.to_sql('etl_logs', self.engine, if_exists='append', index=False)
            print(f"📝 ETL job logged: {job_name} - {status}")
        except Exception as e:
            print(f"⚠️ Could not log ETL job: {e}")
    
    def verify_data_quality(self, df):
        """Run basic data quality checks before loading"""
        print("\n🔍 Running data quality checks...")
        
        issues = []
        
        # Check for nulls in critical columns
        critical_cols = ['sale_date', 'turnover_millions']
        for col in critical_cols:
            null_count = df[col].isnull().sum()
            if null_count > 0:
                issues.append(f"{col} has {null_count} null values")
        
        # Check for negative values
        if (df['turnover_millions'] < 0).any():
            issues.append("Found negative turnover values")
        
        # Check for duplicate dates per category/state
        duplicates = df.duplicated(subset=['sale_date', 'category', 'state']).sum()
        if duplicates > 0:
            issues.append(f"Found {duplicates} duplicate records")
        
        if issues:
            print("⚠️ Data quality issues found:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        else:
            print("✅ All data quality checks passed")
            return True


def main():
    """Test database loading with transformed sample data"""
    
    print("Testing database loader...\n")
    
    # Initialize loader
    loader = DatabaseLoader()
    
    # Test connection
    if not loader.test_connection():
        print("Cannot proceed without database connection")
        return
    
    # Load transformed sample data
    print("\nLoading transformed sample data...")
    df = pd.read_csv('data/abs_transformed.csv')
    
    print(f"Loaded {len(df)} transformed records from CSV")
    
    # Quality checks
    if not loader.verify_data_quality(df):
        print("\n⚠️ Data quality issues detected. Fix before loading.")
        return
    
    # Load to database
    start_time = datetime.now()
    success = loader.load_retail_sales(df)
    end_time = datetime.now()
    
    execution_time = (end_time - start_time).total_seconds()
    
    # Log the job
    loader.log_etl_job(
        job_name='test_sample_load',
        status='SUCCESS' if success else 'FAILED',
        records_processed=len(df),
        records_inserted=len(df) if success else 0,
        execution_time=execution_time
    )
    
    if success:
        print("\n" + "="*70)
        print("✅ DATABASE LOAD TEST COMPLETE!")
        print("="*70)
        print(f"Execution time: {execution_time:.2f} seconds")


if __name__ == "__main__":
    main()