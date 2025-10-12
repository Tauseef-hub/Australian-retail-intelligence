import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from forecast.prophet_forecaster import RetailForecaster
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

load_dotenv()

class ModelEvaluator:
    """Evaluate Prophet forecasting model accuracy"""
    
    def __init__(self):
        self.engine = self._create_engine()
        
    def _create_engine(self):
        connection_string = (
            f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )
        return create_engine(connection_string, pool_pre_ping=True)
    
    def evaluate_recent_accuracy(self, test_months=6):
        """
        Evaluate model by training on historical data 
        and testing on recent months
        """
        
        print("="*70)
        print("MODEL ACCURACY EVALUATION")
        print("="*70)
        
        # Get a sample category with lots of data
        query = """
            SELECT category, state, COUNT(*) as cnt
            FROM retail_sales
            WHERE sale_date >= '1982-01-01'
            GROUP BY category, state
            HAVING COUNT(*) > 200
            ORDER BY COUNT(*) DESC
            LIMIT 5
        """
        
        top_categories = pd.read_sql(query, self.engine)
        
        print(f"\nTesting on {len(top_categories)} top categories...")
        
        results = []
        
        for _, row in top_categories.iterrows():
            category = row['category']
            state = row['state']
            
            result = self._test_category(category, state, test_months)
            if result:
                results.append(result)
        
        # Summary
        self._display_evaluation_summary(results)
        
        return results
    
    def _test_category(self, category, state, test_months):
        """Test single category/state combination"""
        
        print(f"\nTesting: Category {category}, State {state}")
        
        # Get all data
        query = f"""
            SELECT sale_date, turnover_millions
            FROM retail_sales
            WHERE category = '{category}'
            AND state = '{state}'
            AND sale_date >= '1982-01-01'
            ORDER BY sale_date
        """
        
        df = pd.read_sql(query, self.engine)
        
        if len(df) < 50:
            return None
        
        # Split: train on all except last N months
        train_df = df.iloc[:-test_months].copy()
        test_df = df.iloc[-test_months:].copy()
        
        print(f"  Training on {len(train_df)} months")
        print(f"  Testing on {len(test_df)} months")
        
        # Train model
        from prophet import Prophet
        
        prophet_df = pd.DataFrame({
            'ds': train_df['sale_date'],
            'y': train_df['turnover_millions']
        })
        
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
            seasonality_mode='multiplicative'
        )
        model.add_country_holidays(country_name='AU')
        model.fit(prophet_df)
        
        # Predict test period
        future = model.make_future_dataframe(periods=test_months, freq='MS')
        forecast = model.predict(future)
        
        # Get predictions for test period
        predictions = forecast.tail(test_months)
        
        # Calculate errors
        actual = test_df['turnover_millions'].values
        predicted = predictions['yhat'].values
        
        mae = np.mean(np.abs(actual - predicted))
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100
        rmse = np.sqrt(np.mean((actual - predicted) ** 2))
        
        print(f"  MAE: ${mae:,.2f}M")
        print(f"  MAPE: {mape:.2f}%")
        print(f"  RMSE: ${rmse:,.2f}M")
        
        return {
            'category': category,
            'state': state,
            'mae': mae,
            'mape': mape,
            'rmse': rmse,
            'test_months': test_months
        }
    
    def _display_evaluation_summary(self, results):
        """Display summary of evaluation results"""
        
        if not results:
            print("\n❌ No evaluation results")
            return
        
        results_df = pd.DataFrame(results)
        
        print("\n" + "="*70)
        print("EVALUATION SUMMARY")
        print("="*70)
        
        print(f"\nTested on {len(results)} category/state combinations")
        print(f"\nAverage Performance:")
        print(f"  Mean Absolute Error (MAE): ${results_df['mae'].mean():,.2f}M")
        print(f"  Mean Absolute Percentage Error (MAPE): {results_df['mape'].mean():.2f}%")
        print(f"  Root Mean Squared Error (RMSE): ${results_df['rmse'].mean():,.2f}M")
        
        print(f"\nBest Performing:")
        best = results_df.nsmallest(1, 'mape').iloc[0]
        print(f"  Category {best['category']}, State {best['state']}")
        print(f"  MAPE: {best['mape']:.2f}%")
        
        print(f"\nWorst Performing:")
        worst = results_df.nlargest(1, 'mape').iloc[0]
        print(f"  Category {worst['category']}, State {worst['state']}")
        print(f"  MAPE: {worst['mape']:.2f}%")
        
        print(f"\nInterpretation:")
        avg_mape = results_df['mape'].mean()
        if avg_mape < 10:
            print("  ✅ Excellent accuracy (<10% error)")
        elif avg_mape < 20:
            print("  ✅ Good accuracy (10-20% error)")
        elif avg_mape < 30:
            print("  ⚠️ Moderate accuracy (20-30% error)")
        else:
            print("  ⚠️ Lower accuracy (>30% error) - consider model tuning")
    
    def get_forecast_summary(self):
        """Get summary of all forecasts in database"""
        
        print("\n" + "="*70)
        print("FORECAST DATABASE SUMMARY")
        print("="*70)
        
        query = """
            SELECT 
                COUNT(*) as total_forecasts,
                COUNT(DISTINCT category) as categories,
                COUNT(DISTINCT state) as states,
                MIN(forecast_date) as earliest_forecast,
                MAX(forecast_date) as latest_forecast,
                AVG(predicted_turnover) as avg_prediction,
                MIN(predicted_turnover) as min_prediction,
                MAX(predicted_turnover) as max_prediction
            FROM sales_forecasts
        """
        
        summary = pd.read_sql(query, self.engine)
        
        print(f"\nTotal forecasts: {summary['total_forecasts'].iloc[0]:,}")
        print(f"Categories covered: {summary['categories'].iloc[0]}")
        print(f"States covered: {summary['states'].iloc[0]}")
        print(f"Forecast period: {summary['earliest_forecast'].iloc[0]} to {summary['latest_forecast'].iloc[0]}")
        print(f"Average prediction: ${summary['avg_prediction'].iloc[0]:,.2f}M")
        print(f"Range: ${summary['min_prediction'].iloc[0]:,.2f}M to ${summary['max_prediction'].iloc[0]:,.2f}M")

def main():
    """Run model evaluation"""
    
    evaluator = ModelEvaluator()
    
    # Evaluate on recent data
    results = evaluator.evaluate_recent_accuracy(test_months=6)
    
    # Get forecast summary
    evaluator.get_forecast_summary()
    
    print("\n" + "="*70)
    print("✅ MODEL EVALUATION COMPLETE!")
    print("="*70)

if __name__ == "__main__":
    main()