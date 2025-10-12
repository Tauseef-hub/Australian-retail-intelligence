from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

def get_db_engine():
    """Create database connection"""
    connection_string = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    return create_engine(connection_string, pool_pre_ping=True)

def run_analysis_queries():
    """Run SQL queries to analyze retail sales data"""
    
    engine = get_db_engine()
    
    print("="*70)
    print("ANALYZING RETAIL SALES DATA IN CLOUD DATABASE")
    print("="*70)
    
    # Query 1: Basic stats
    print("\n📊 QUERY 1: Basic Statistics")
    query1 = text("""
        SELECT 
            COUNT(*) as total_records,
            MIN(sale_date) as earliest_date,
            MAX(sale_date) as latest_date,
            MIN(turnover_millions) as min_turnover,
            MAX(turnover_millions) as max_turnover,
            AVG(turnover_millions) as avg_turnover,
            COUNT(DISTINCT category) as unique_categories,
            COUNT(DISTINCT state) as unique_states
        FROM retail_sales;
    """)
    
    with engine.connect() as conn:
        result = pd.read_sql(query1, conn)
        print(result.to_string(index=False))
    
    # Query 2: Monthly average
    print("\n📈 QUERY 2: Average Turnover by Month")
    query2 = text("""
        SELECT 
            month_name,
            COUNT(*) as record_count,
            ROUND(AVG(turnover_millions), 2) as avg_turnover,
            ROUND(MIN(turnover_millions), 2) as min_turnover,
            ROUND(MAX(turnover_millions), 2) as max_turnover
        FROM retail_sales
        GROUP BY month_name
        ORDER BY 
            CASE month_name
                WHEN 'January' THEN 1
                WHEN 'February' THEN 2
                WHEN 'March' THEN 3
                WHEN 'April' THEN 4
                WHEN 'May' THEN 5
                WHEN 'June' THEN 6
                WHEN 'July' THEN 7
                WHEN 'August' THEN 8
                WHEN 'September' THEN 9
                WHEN 'October' THEN 10
                WHEN 'November' THEN 11
                WHEN 'December' THEN 12
            END;
    """)
    
    with engine.connect() as conn:
        result = pd.read_sql(query2, conn)
        print(result.to_string(index=False))
    
    # Query 3: Year-over-year growth
    print("\n📊 QUERY 3: Records with Growth Data")
    query3 = text("""
        SELECT 
            COUNT(*) as total_with_growth,
            ROUND(AVG(growth_rate_yoy), 2) as avg_growth_rate,
            ROUND(MIN(growth_rate_yoy), 2) as min_growth_rate,
            ROUND(MAX(growth_rate_yoy), 2) as max_growth_rate
        FROM retail_sales
        WHERE growth_rate_yoy IS NOT NULL;
    """)
    
    with engine.connect() as conn:
        result = pd.read_sql(query3, conn)
        print(result.to_string(index=False))
    
    # Query 4: Sample records
    print("\n📋 QUERY 4: Sample Records (First 10)")
    query4 = text("""
        SELECT 
            sale_date,
            category,
            state,
            turnover_millions,
            month_name,
            year,
            growth_rate_yoy
        FROM retail_sales
        ORDER BY sale_date
        LIMIT 10;
    """)
    
    with engine.connect() as conn:
        result = pd.read_sql(query4, conn)
        print(result.to_string(index=False))
    
    # Query 5: ETL logs
    print("\n📝 QUERY 5: ETL Job History")
    query5 = text("""
        SELECT 
            job_name,
            status,
            records_processed,
            records_inserted,
            execution_time_seconds,
            started_at
        FROM etl_logs
        ORDER BY started_at DESC;
    """)
    
    with engine.connect() as conn:
        result = pd.read_sql(query5, conn)
        print(result.to_string(index=False))
    
    print("\n" + "="*70)
    print("✅ ANALYSIS COMPLETE!")
    print("="*70)

if __name__ == "__main__":
    run_analysis_queries()