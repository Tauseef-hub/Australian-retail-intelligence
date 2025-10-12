import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from forecast.prophet_forecaster import RetailForecaster
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

load_dotenv()

def get_all_categories():
    """Get list of all categories and states from database"""
    
    connection_string = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    engine = create_engine(connection_string, pool_pre_ping=True)
    
    query = """
        SELECT DISTINCT 
            category,
            state,
            COUNT(*) as record_count
        FROM retail_sales
        WHERE sale_date >= '1982-01-01'
        GROUP BY category, state
        HAVING COUNT(*) >= 24
        ORDER BY category, state
    """
    
    df = pd.read_sql(query, engine)
    return df

def clear_existing_forecasts():
    """Clear existing forecasts from database"""
    
    connection_string = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    engine = create_engine(connection_string, pool_pre_ping=True)
    
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM sales_forecasts"))
        conn.commit()
    
    print("✅ Cleared existing forecasts")

def forecast_all_categories():
    """Generate forecasts for all categories and states"""
    
    print("="*80)
    print("FORECASTING ALL RETAIL CATEGORIES")
    print("="*80)
    
    start_time = datetime.now()
    
    # Get all category/state combinations
    categories_df = get_all_categories()
    
    print(f"\n📊 Found {len(categories_df)} category/state combinations to forecast")
    print(f"   Total categories: {categories_df['category'].nunique()}")
    print(f"   Total states: {categories_df['state'].nunique()}")
    
    # Clear existing forecasts
    clear_existing_forecasts()
    
    # Initialize forecaster
    forecaster = RetailForecaster()
    
    # Track results
    successful = 0
    failed = 0
    failed_list = []
    
    print("\n" + "="*80)
    print("GENERATING FORECASTS...")
    print("="*80)
    
    # Forecast each combination
    for idx, row in categories_df.iterrows():
        category = row['category']
        state = row['state']
        
        print(f"\n[{idx+1}/{len(categories_df)}] Category: {category}, State: {state}")
        
        try:
            # Generate forecast
            forecast = forecaster.train_forecast_model(
                category=category,
                state=state,
                periods=12
            )
            
            if forecast is not None:
                # Save to database
                forecaster.save_forecasts_to_database(
                    category, state, forecast, periods=12
                )
                successful += 1
            else:
                failed += 1
                failed_list.append(f"{category}-{state}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:100]}")
            failed += 1
            failed_list.append(f"{category}-{state}")
    
    # Summary
    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds()
    
    print("\n" + "="*80)
    print("✅ FORECASTING COMPLETE!")
    print("="*80)
    print(f"\nResults:")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total forecasts generated: {successful * 12} monthly predictions")
    print(f"  Execution time: {execution_time:.2f} seconds ({execution_time/60:.2f} minutes)")
    
    if failed_list:
        print(f"\nFailed combinations:")
        for item in failed_list[:10]:
            print(f"  - {item}")
        if len(failed_list) > 10:
            print(f"  ... and {len(failed_list) - 10} more")
    
    # Verify database
    connection_string = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    engine = create_engine(connection_string, pool_pre_ping=True)
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM sales_forecasts"))
        total_forecasts = result.fetchone()[0]
    
    print(f"\n📊 Total forecast records in database: {total_forecasts:,}")

if __name__ == "__main__":
    forecast_all_categories()