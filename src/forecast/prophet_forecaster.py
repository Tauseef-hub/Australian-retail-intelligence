import pandas as pd
import numpy as np
from prophet import Prophet
from datetime import datetime
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import warnings
warnings.filterwarnings('ignore')

load_dotenv()

class RetailForecaster:
    """
    Time series forecasting for Australian retail sales using Prophet
    """
    
    def __init__(self):
        self.engine = self._create_engine()
        self.models = {}
        
    def _create_engine(self):
        """Create database connection"""
        connection_string = (
            f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )
        return create_engine(connection_string, pool_pre_ping=True)
    
    def load_historical_data(self, category=None, state=None):
        """Load historical retail sales from database"""
        
        print("="*70)
        print("LOADING HISTORICAL DATA FOR FORECASTING")
        print("="*70)
        
        query = """
            SELECT 
                sale_date,
                category,
                state,
                turnover_millions,
                growth_rate_yoy
            FROM retail_sales
            WHERE sale_date >= '1982-01-01'
        """
        
        # Add filters if specified
        filters = []
        if category:
            filters.append(f"category = '{category}'")
        if state:
            filters.append(f"state = '{state}'")
        
        if filters:
            query += " AND " + " AND ".join(filters)
        
        query += " ORDER BY sale_date"
        
        df = pd.read_sql(query, self.engine)
        
        print(f"✅ Loaded {len(df):,} historical records")
        print(f"   Date range: {df['sale_date'].min()} to {df['sale_date'].max()}")
        print(f"   Categories: {df['category'].nunique()}")
        print(f"   States: {df['state'].nunique()}")
        
        return df
    
    def prepare_prophet_data(self, df, category, state):
        """Prepare data in Prophet format (ds, y)"""
        
        # Filter for specific category and state
        mask = (df['category'] == category) & (df['state'] == state)
        data = df[mask].copy()
        
        if len(data) == 0:
            return None
        
        # Prophet requires columns named 'ds' (date) and 'y' (value)
        prophet_df = pd.DataFrame({
            'ds': data['sale_date'],
            'y': data['turnover_millions']
        })
        
        return prophet_df
    
    def train_forecast_model(self, category, state='AUS', periods=12):
        """
        Train Prophet model and generate forecasts
        
        Parameters:
        - category: Retail category to forecast
        - state: Australian state (default 'AUS' for national)
        - periods: Number of months to forecast
        """
        
        print(f"\n{'='*70}")
        print(f"FORECASTING: Category {category}, State {state}")
        print(f"{'='*70}")
        
        # Load data
        df = self.load_historical_data()
        
        # Prepare for Prophet
        prophet_df = self.prepare_prophet_data(df, category, state)
        
        if prophet_df is None or len(prophet_df) < 24:
            print(f"❌ Insufficient data for category {category}, state {state}")
            return None
        
        print(f"\nTraining data: {len(prophet_df)} monthly observations")
        print(f"Date range: {prophet_df['ds'].min()} to {prophet_df['ds'].max()}")
        print(f"Average turnover: ${prophet_df['y'].mean():.2f}M")
        
        # Initialize Prophet model
        print("\nTraining Prophet model...")
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
            seasonality_mode='multiplicative',
            changepoint_prior_scale=0.05
        )
        
        # Add Australian holidays
        model.add_country_holidays(country_name='AU')
        
        # Fit model
        model.fit(prophet_df)
        
        print("✅ Model trained successfully")
        
        # Generate future dates
        future = model.make_future_dataframe(periods=periods, freq='MS')
        
        # Make predictions
        forecast = model.predict(future)
        
        # Store model
        model_key = f"{category}_{state}"
        self.models[model_key] = {
            'model': model,
            'forecast': forecast,
            'historical': prophet_df
        }
        
        # Display results
        self._display_forecast_results(forecast, prophet_df, periods)
        
        return forecast
    
    def _display_forecast_results(self, forecast, historical, periods):
        """Display forecast summary"""
        
        # Get forecast period only
        forecast_only = forecast.tail(periods)
        
        print(f"\n{'='*70}")
        print("FORECAST RESULTS")
        print(f"{'='*70}")
        
        print(f"\nNext {periods} months forecast:")
        print(f"{'Date':<15} {'Predicted':<15} {'Lower Bound':<15} {'Upper Bound':<15}")
        print("-" * 70)
        
        for _, row in forecast_only.head(6).iterrows():
            print(f"{row['ds'].strftime('%Y-%m-%d'):<15} "
                  f"${row['yhat']:>10,.2f}M    "
                  f"${row['yhat_lower']:>10,.2f}M    "
                  f"${row['yhat_upper']:>10,.2f}M")
        
        if periods > 6:
            print("...")
        
        # Summary statistics
        avg_forecast = forecast_only['yhat'].mean()
        avg_historical = historical['y'].tail(12).mean()
        growth = ((avg_forecast - avg_historical) / avg_historical) * 100
        
        print(f"\n📊 Forecast Summary:")
        print(f"   Average historical (last 12 months): ${avg_historical:,.2f}M")
        print(f"   Average forecast (next {periods} months): ${avg_forecast:,.2f}M")
        print(f"   Projected growth: {growth:+.2f}%")
    
    def save_forecasts_to_database(self, category, state, forecast, periods):
        """Save forecasts to sales_forecasts table"""
        
        print(f"\nSaving forecasts to database...")
        
        # Get forecast period only
        forecast_only = forecast.tail(periods).copy()
        
        # Prepare for database
        forecast_only['category'] = category
        forecast_only['state'] = state
        forecast_only['predicted_turnover'] = forecast_only['yhat']
        forecast_only['lower_bound'] = forecast_only['yhat_lower']
        forecast_only['upper_bound'] = forecast_only['yhat_upper']
        forecast_only['confidence_interval'] = 0.95
        forecast_only['model_name'] = 'Prophet'
        forecast_only['model_version'] = '1.0'
        
        # Select columns for database
        db_forecast = forecast_only[[
            'ds', 'category', 'state', 
            'predicted_turnover', 'lower_bound', 'upper_bound',
            'confidence_interval', 'model_name', 'model_version'
        ]].copy()
        
        db_forecast.rename(columns={'ds': 'forecast_date'}, inplace=True)
        
        # Save to database
        db_forecast.to_sql('sales_forecasts', self.engine, if_exists='append', index=False)
        
        print(f"✅ Saved {len(db_forecast)} forecast records to database")


def main():
    """Test the forecasting model"""
    
    print("="*70)
    print("AUSTRALIAN RETAIL SALES FORECASTING")
    print("="*70)
    
    forecaster = RetailForecaster()
    
    # Example: Forecast for category 20 (common category), state AUS
    # You can change these based on your data
    forecast = forecaster.train_forecast_model(
        category='20',
        state='AUS',
        periods=12  # Forecast next 12 months
    )
    
    if forecast is not None:
        # Save to database
        forecaster.save_forecasts_to_database('20', 'AUS', forecast, periods=12)
        
        print("\n" + "="*70)
        print("✅ FORECASTING COMPLETE!")
        print("="*70)

if __name__ == "__main__":
    main()