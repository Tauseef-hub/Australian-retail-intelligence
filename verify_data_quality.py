from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

def comprehensive_data_check():
    """Thorough verification of cleaned data"""
    
    print("="*80)
    print("COMPREHENSIVE DATA QUALITY VERIFICATION")
    print("="*80)
    
    connection_string = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    engine = create_engine(connection_string, pool_pre_ping=True)
    
    # CHECK 1: Total Records
    print("\n📊 CHECK 1: TOTAL RECORDS")
    print("-" * 80)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM retail_sales"))
        total = result.fetchone()[0]
        print(f"Total records: {total:,}")
    
    # CHECK 2: Date Range Coverage
    print("\n📅 CHECK 2: DATE RANGE COVERAGE")
    print("-" * 80)
    query = """
        SELECT 
            MIN(sale_date) as earliest,
            MAX(sale_date) as latest,
            COUNT(DISTINCT sale_date) as unique_dates
        FROM retail_sales
    """
    df = pd.read_sql(query, engine)
    print(f"Earliest date: {df['earliest'].iloc[0]}")
    print(f"Latest date: {df['latest'].iloc[0]}")
    print(f"Unique dates: {df['unique_dates'].iloc[0]:,}")
    
    # CHECK 3: Categories and States
    print("\n🏪 CHECK 3: CATEGORIES & STATES")
    print("-" * 80)
    query = """
        SELECT 
            COUNT(DISTINCT category) as categories,
            COUNT(DISTINCT state) as states
        FROM retail_sales
    """
    df = pd.read_sql(query, engine)
    print(f"Unique categories: {df['categories'].iloc[0]}")
    print(f"Unique states: {df['states'].iloc[0]}")
    
    # CHECK 4: Duplicate Check (CRITICAL!)
    print("\n🔍 CHECK 4: DUPLICATE DETECTION (CRITICAL)")
    print("-" * 80)
    query = """
        SELECT sale_date, category, state, COUNT(*) as count
        FROM retail_sales
        GROUP BY sale_date, category, state
        HAVING COUNT(*) > 1
        ORDER BY count DESC
        LIMIT 10
    """
    duplicates = pd.read_sql(query, engine)
    
    if len(duplicates) > 0:
        print(f"❌ FOUND {len(duplicates)} DUPLICATE COMBINATIONS!")
        print("\nTop duplicates:")
        print(duplicates.to_string(index=False))
    else:
        print("✅ NO DUPLICATES FOUND! Perfect!")
    
    # CHECK 5: Value Range Check
    print("\n💰 CHECK 5: VALUE RANGE & STATISTICS")
    print("-" * 80)
    query = """
        SELECT 
            MIN(turnover_millions) as min_value,
            MAX(turnover_millions) as max_value,
            AVG(turnover_millions) as avg_value,
            STDDEV(turnover_millions) as std_dev,
            COUNT(*) FILTER (WHERE turnover_millions < 0) as negative_count,
            COUNT(*) FILTER (WHERE turnover_millions = 0) as zero_count,
            COUNT(*) FILTER (WHERE turnover_millions IS NULL) as null_count
        FROM retail_sales
    """
    df = pd.read_sql(query, engine)
    print(f"Min value: ${df['min_value'].iloc[0]:,.2f}M")
    print(f"Max value: ${df['max_value'].iloc[0]:,.2f}M")
    print(f"Average: ${df['avg_value'].iloc[0]:,.2f}M")
    print(f"Std Dev: ${df['std_dev'].iloc[0]:,.2f}M")
    print(f"\nData quality:")
    print(f"  Negative values: {df['negative_count'].iloc[0]}")
    print(f"  Zero values: {df['zero_count'].iloc[0]}")
    print(f"  Null values: {df['null_count'].iloc[0]}")
    
    # CHECK 6: Sample Multiple Categories
    print("\n📋 CHECK 6: SAMPLE DATA ACROSS CATEGORIES")
    print("-" * 80)
    query = """
        SELECT category, state, COUNT(*) as records,
               MIN(turnover_millions) as min_val,
               MAX(turnover_millions) as max_val,
               AVG(turnover_millions) as avg_val
        FROM retail_sales
        WHERE state = 'AUS'
        GROUP BY category, state
        ORDER BY category
        LIMIT 10
    """
    df = pd.read_sql(query, engine)
    print("\nFirst 10 categories (Australia totals):")
    print(df.to_string(index=False))
    
    # CHECK 7: Monthly Consistency Check
    print("\n📈 CHECK 7: MONTHLY CONSISTENCY (Category 20, AUS)")
    print("-" * 80)
    query = """
        SELECT 
            TO_CHAR(sale_date, 'YYYY-MM') as month,
            turnover_millions,
            LAG(turnover_millions) OVER (ORDER BY sale_date) as prev_month,
            turnover_millions - LAG(turnover_millions) OVER (ORDER BY sale_date) as change
        FROM retail_sales
        WHERE category = '20' AND state = 'AUS'
        ORDER BY sale_date DESC
        LIMIT 12
    """
    df = pd.read_sql(query, engine)
    print("\nLast 12 months:")
    print(df.to_string(index=False))
    
    # Calculate volatility
    if 'change' in df.columns:
        volatility = df['change'].std()
        print(f"\nMonth-to-month volatility (std dev): ${volatility:,.2f}M")
        if volatility < 2000:
            print("✅ Low volatility - data looks smooth!")
        else:
            print("⚠️ High volatility - check for spikes")
    
    # CHECK 8: Records per Category/State
    print("\n📊 CHECK 8: RECORD DISTRIBUTION")
    print("-" * 80)
    query = """
        SELECT 
            COUNT(*) FILTER (WHERE state = 'AUS') as australia_total,
            COUNT(*) FILTER (WHERE state != 'AUS') as state_level,
            COUNT(DISTINCT category || '-' || state) as unique_combinations
        FROM retail_sales
    """
    df = pd.read_sql(query, engine)
    print(f"Australia (national) records: {df['australia_total'].iloc[0]:,}")
    print(f"State-level records: {df['state_level'].iloc[0]:,}")
    print(f"Unique category/state combinations: {df['unique_combinations'].iloc[0]:,}")
    
    # FINAL VERDICT
    print("\n" + "="*80)
    print("FINAL VERIFICATION SUMMARY")
    print("="*80)
    
    # Re-check duplicates for verdict
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT COUNT(*) FROM (
                SELECT sale_date, category, state, COUNT(*) as count
                FROM retail_sales
                GROUP BY sale_date, category, state
                HAVING COUNT(*) > 1
            ) duplicates
        """))
        dup_count = result.fetchone()[0]
    
    if dup_count == 0:
        print("✅ NO DUPLICATES - Data is clean!")
        print("✅ Ready to generate forecasts!")
        return True
    else:
        print(f"❌ FOUND {dup_count} DUPLICATES - Need to fix!")
        print("❌ DO NOT generate forecasts yet!")
        return False

if __name__ == "__main__":
    is_clean = comprehensive_data_check()
    
    if is_clean:
        print("\n🎉 ALL CHECKS PASSED!")
        print("\nNext step: python src/forecast/forecast_all_categories.py")
    else:
        print("\n⚠️ DATA QUALITY ISSUES DETECTED!")
        print("\nInvestigate issues before generating forecasts")