import requests
import pandas as pd
from datetime import datetime
import time

class ABSRetailDataExtractor:
    """
    Extract retail sales data from Australian Bureau of Statistics API
    Using the Monthly Household Spending Indicator (MHSI)
    """
    
    def __init__(self):
        self.base_url = "https://api.data.abs.gov.au/data"
        self.dataset_id = "RT"  # Retail Trade dataset
        self.version = "1.0.0"
        
    def test_connection(self):
        """Test if we can connect to ABS API"""
        print("Testing ABS API connection...")
        
        try:
            # Simple test endpoint
            test_url = f"{self.base_url}/ABS,{self.dataset_id},{self.version}/all"
            
            response = requests.get(test_url, timeout=10, params={'format': 'csv'})
            
            if response.status_code == 200:
                print("✅ ABS API connection successful!")
                print(f"Response size: {len(response.content)} bytes")
                return True
            else:
                print(f"⚠️ API returned status code: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Connection failed: {str(e)}")
            return False
    
    def explore_available_data(self):
        """Explore what data is available from ABS"""
        print("\nExploring ABS Retail Trade data...")
        
        try:
            # Get all retail trade data
            url = f"{self.base_url}/ABS,{self.dataset_id},{self.version}/all"
            
            print(f"Fetching from: {url}")
            
            response = requests.get(url, params={'format': 'csv'}, timeout=30)
            
            if response.status_code == 200:
                # Parse CSV response
                from io import StringIO
                df = pd.read_csv(StringIO(response.text))
                
                print(f"\n✅ Data retrieved successfully!")
                print(f"Rows: {len(df)}")
                print(f"Columns: {list(df.columns)}")
                
                print("\nFirst few rows:")
                print(df.head())
                
                print("\nData types:")
                print(df.dtypes)
                
                # Save sample for inspection
                df.head(100).to_csv('data/abs_sample.csv', index=False)
                print("\n📁 Saved sample to: data/abs_sample.csv")
                
                return df
            else:
                print(f"❌ Failed to retrieve data: {response.status_code}")
                print(f"Response: {response.text[:500]}")
                return None
                
        except Exception as e:
            print(f"❌ Error exploring data: {str(e)}")
            return None
    
    def extract_retail_sales(self, start_date=None, end_date=None):
        """
        Extract retail sales data for specified date range
        
        Parameters:
        - start_date: str (format: 'YYYY-MM') or None for all available
        - end_date: str (format: 'YYYY-MM') or None for all available
        """
        print("\n" + "="*60)
        print("EXTRACTING AUSTRALIAN RETAIL SALES DATA")
        print("="*60)
        
        try:
            url = f"{self.base_url}/ABS,{self.dataset_id},{self.version}/all"
            
            params = {
                'format': 'csv',
                'startPeriod': start_date if start_date else '2020-01',
                'endPeriod': end_date if end_date else datetime.now().strftime('%Y-%m')
            }
            
            print(f"\nFetching data from {params['startPeriod']} to {params['endPeriod']}...")
            
            response = requests.get(url, params=params, timeout=60)
            
            if response.status_code == 200:
                from io import StringIO
                df = pd.read_csv(StringIO(response.text))
                
                print(f"✅ Retrieved {len(df):,} raw records")
                
                # 🔧 CRITICAL FIX: Filter to M1 AND TSEST 20 (original, unadjusted series)
                # ABS returns:
                # - Multiple MEASURE types (M1, M4, etc.)
                # - Multiple TSEST types within each measure (10, 20, 30, etc.)
                # We only want M1 + TSEST 20 to get ONE clean record per date/category/state
                if 'MEASURE' in df.columns and 'TSEST' in df.columns:
                    before_filter = len(df)
                    df = df[(df['MEASURE'] == 'M1') & (df['TSEST'] == 20)].copy()
                    after_filter = len(df)
                    removed = before_filter - after_filter
                    print(f"✅ Filtered to M1 + TSEST 20 (original): {after_filter:,} records")
                    print(f"   Removed {removed:,} duplicate series")
                elif 'MEASURE' in df.columns:
                    before_filter = len(df)
                    df = df[df['MEASURE'] == 'M1'].copy()
                    after_filter = len(df)
                    removed = before_filter - after_filter
                    print(f"✅ Filtered to M1 measure: {after_filter:,} records")
                    print(f"   Removed {removed:,} duplicate series")
                    print(f"   ⚠️ Warning: TSEST column not found - may still have duplicates")
                else:
                    print("⚠️ Warning: MEASURE column not found - data may contain duplicates")
                
                return df
            else:
                print(f"❌ API Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Extraction failed: {str(e)}")
            return None


def main():
    """Test the ABS API extractor"""
    
    print("="*60)
    print("AUSTRALIAN BUREAU OF STATISTICS - DATA EXTRACTION TEST")
    print("="*60)
    
    extractor = ABSRetailDataExtractor()
    
    # Step 1: Test connection
    print("\n1. Testing API connection...")
    if extractor.test_connection():
        print("   Connection verified ✓")
    else:
        print("   Connection failed ✗")
        return
    
    # Step 2: Explore available data
    print("\n2. Exploring available retail data...")
    time.sleep(2)  # Be polite to the API
    
    df = extractor.explore_available_data()
    
    if df is not None:
        print("\n" + "="*60)
        print("✅ ABS API EXTRACTION TEST COMPLETE!")
        print("="*60)
        print("\nNext steps:")
        print("1. Review the sample data in data/abs_sample.csv")
        print("2. Understand the data structure")
        print("3. Build transformation logic")
    else:
        print("\n❌ Unable to retrieve data. Check API documentation.")


if __name__ == "__main__":
    main()