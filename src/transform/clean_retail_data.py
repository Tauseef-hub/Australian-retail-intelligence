import pandas as pd
from datetime import datetime

class RetailDataTransformer:
    """
    Transform raw ABS retail data into clean, database-ready format
    """
    
    def __init__(self):
        self.required_columns = ['TIME_PERIOD', 'OBS_VALUE', 'MEASURE', 'INDUSTRY', 'REGION']
    
    def validate_raw_data(self, df):
        """Check if raw data has required columns"""
        print("Validating raw data...")
        
        missing_cols = [col for col in self.required_columns if col not in df.columns]
        
        if missing_cols:
            print(f"❌ Missing required columns: {missing_cols}")
            return False
        
        print(f"✅ All required columns present")
        print(f"   Rows: {len(df):,}")
        print(f"   Columns: {len(df.columns)}")
        return True
    
    def parse_time_period(self, df):
        """Convert TIME_PERIOD to proper date - handle multiple formats"""
        print("\nParsing time periods...")
        
        # Check the format of TIME_PERIOD
        sample_period = str(df['TIME_PERIOD'].iloc[0])
        print(f"   Sample TIME_PERIOD: {sample_period}")
        
        try:
            # Try format 1: YYYY-MM (e.g., "1982-04")
            df['sale_date'] = pd.to_datetime(df['TIME_PERIOD'] + '-01', format='%Y-%m-%d')
        except:
            try:
                # Try format 2: YYYY-QN (e.g., "2020-Q1")
                df['sale_date'] = pd.to_datetime(df['TIME_PERIOD'], format='mixed')
            except:
                # Try format 3: Let pandas infer
                df['sale_date'] = pd.to_datetime(df['TIME_PERIOD'], format='ISO8601', errors='coerce')
        
        # Remove any rows where date parsing failed
        before_count = len(df)
        df = df[df['sale_date'].notna()].copy()
        after_count = len(df)
        
        if before_count != after_count:
            print(f"   ⚠️ Removed {before_count - after_count} rows with unparseable dates")
        
        # Extract components
        df['year'] = df['sale_date'].dt.year
        df['month_name'] = df['sale_date'].dt.strftime('%B')
        df['month_number'] = df['sale_date'].dt.month
        
        print(f"✅ Parsed {len(df)} time periods")
        print(f"   Date range: {df['sale_date'].min()} to {df['sale_date'].max()}")
        
        return df
    
    def clean_values(self, df):
        """Clean and validate OBS_VALUE (sales values)"""
        print("\nCleaning sales values...")
        
        # Rename for clarity
        df['turnover_millions'] = df['OBS_VALUE']
        
        # Remove any null values
        before_count = len(df)
        df = df[df['turnover_millions'].notna()].copy()
        after_count = len(df)
        
        if before_count != after_count:
            print(f"⚠️ Removed {before_count - after_count} rows with null values")
        
        # Ensure positive values
        df = df[df['turnover_millions'] > 0].copy()
        
        print(f"✅ Cleaned {len(df):,} records")
        print(f"   Min: ${df['turnover_millions'].min():.2f}M")
        print(f"   Max: ${df['turnover_millions'].max():.2f}M")
        print(f"   Mean: ${df['turnover_millions'].mean():.2f}M")
        
        return df
    
    def map_categories(self, df):
        """Map industry and region codes to readable names"""
        print("\nMapping categories...")
        
        # For now, keep codes as-is
        # Later we can add proper mapping dictionaries
        df['category'] = df['INDUSTRY'].astype(str)
        df['state'] = df['REGION'].astype(str)
        
        print(f"✅ Mapped categories")
        print(f"   Unique industries: {df['category'].nunique()}")
        print(f"   Unique regions: {df['state'].nunique()}")
        
        return df
    
    def calculate_growth_rates(self, df):
        """Calculate year-over-year growth rates"""
        print("\nCalculating growth rates...")
        
        # Sort by category, state, and date
        df = df.sort_values(['category', 'state', 'sale_date']).copy()
        
        # Calculate YoY growth (12 months ago)
        df['growth_rate_yoy'] = df.groupby(['category', 'state'])['turnover_millions'].pct_change(12) * 100
        
        # Round to 2 decimal places
        df['growth_rate_yoy'] = df['growth_rate_yoy'].round(2)
        
        valid_growth = df['growth_rate_yoy'].notna().sum()
        print(f"✅ Calculated growth rates for {valid_growth:,} records")
        
        return df
    
    def prepare_for_database(self, df):
        """Select and rename columns for database insertion"""
        print("\nPreparing final dataset for database...")
        
        # Select columns matching our database schema
        final_df = df[[
            'sale_date',
            'category',
            'state',
            'turnover_millions',
            'month_name',
            'year',
            'growth_rate_yoy'
        ]].copy()
        
        # Add metadata
        final_df['data_source'] = 'ABS_RT'
        
        print(f"✅ Final dataset ready: {len(final_df):,} rows × {len(final_df.columns)} columns")
        
        return final_df
    
    def transform(self, raw_df):
        """
        Main transformation pipeline
        
        Input: Raw DataFrame from ABS API
        Output: Clean DataFrame ready for database
        """
        print("="*70)
        print("STARTING DATA TRANSFORMATION PIPELINE")
        print("="*70)
        
        # Step 1: Validate
        if not self.validate_raw_data(raw_df):
            raise ValueError("Raw data validation failed")
        
        # Step 2: Parse dates
        df = self.parse_time_period(raw_df)
        
        # Step 3: Clean values
        df = self.clean_values(df)
        
        # Step 4: Map categories
        df = self.map_categories(df)
        
        # Step 5: Calculate growth
        df = self.calculate_growth_rates(df)
        
        # Step 6: Prepare final format
        final_df = self.prepare_for_database(df)
        
        print("\n" + "="*70)
        print("✅ TRANSFORMATION COMPLETE!")
        print("="*70)
        
        return final_df


def main():
    """Test the transformation pipeline"""
    
    print("Testing transformation pipeline with sample data...\n")
    
    # Load sample data
    df_raw = pd.read_csv('data/abs_sample.csv')
    
    # Transform
    transformer = RetailDataTransformer()
    df_clean = transformer.transform(df_raw)
    
    # Show results
    print("\nTransformed Data Sample:")
    print(df_clean.head(10))
    
    print("\nData Types:")
    print(df_clean.dtypes)
    
    # Save transformed sample
    df_clean.to_csv('data/abs_transformed.csv', index=False)
    print(f"\n📁 Saved transformed data to: data/abs_transformed.csv")


if __name__ == "__main__":
    main()