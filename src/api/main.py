from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import os
from datetime import datetime
from typing import Optional, List

load_dotenv()

# Initialize FastAPI
app = FastAPI(
    title="Australian Retail Intelligence API",
    description="Production API for Australian retail sales forecasts and historical data (1982-2024)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS (allow API access from any domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
def get_db_engine():
    connection_string = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    return create_engine(connection_string, pool_pre_ping=True)

engine = get_db_engine()

# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/")
def root():
    """Welcome endpoint with API information"""
    return {
        "message": "Australian Retail Intelligence API",
        "version": "1.0.0",
        "author": "Tauseef Mohammed Aoun",
        "description": "Production API providing 42 years of Australian retail data and AI-powered forecasts",
        "data_coverage": {
            "historical_records": "95,798 records (1982-2024)",
            "forecasts": "2,304 predictions (2025)",
            "categories": 22,
            "states": 9
        },
        "endpoints": {
            "documentation": "/docs",
            "health": "/health",
            "forecasts": "/forecasts",
            "historical": "/sales",
            "categories": "/categories",
            "states": "/states"
        },
        "github": "https://github.com/Tauseef-hub/australian-retail-intelligence"
    }

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health")
def health_check():
    """Check API and database health"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# ============================================================================
# FORECAST ENDPOINTS
# ============================================================================

@app.get("/forecasts")
def get_forecasts(
    category: Optional[str] = Query(None, description="Retail category (e.g., '20')"),
    state: Optional[str] = Query(None, description="Australian state (e.g., 'AUS', 'NSW')"),
    limit: Optional[int] = Query(None, ge=1, le=100000, description="Number of records to return (no limit if not specified)")
):
    """
    Get retail sales forecasts
    
    - **category**: Filter by retail category (optional)
    - **state**: Filter by Australian state (optional)
    - **limit**: Maximum number of records (optional, returns all if not specified)
    """
    try:
        query = """
            SELECT 
                forecast_date,
                category,
                state,
                predicted_turnover,
                lower_bound,
                upper_bound,
                confidence_interval,
                model_name,
                model_version
            FROM sales_forecasts
            WHERE 1=1
        """
        
        params = {}
        
        if category:
            query += " AND category = :category"
            params['category'] = category
        
        if state:
            query += " AND state = :state"
            params['state'] = state
        
        query += " ORDER BY forecast_date"
        
        if limit:
            query += " LIMIT :limit"
            params['limit'] = limit
        
        df = pd.read_sql(text(query), engine, params=params)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No forecasts found")
        
        # Convert to dict and format dates
        df['forecast_date'] = df['forecast_date'].astype(str)
        
        return {
            "count": len(df),
            "forecasts": df.to_dict(orient='records')
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/forecasts/summary")
def get_forecast_summary():
    """Get summary statistics of all forecasts"""
    try:
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
        
        df = pd.read_sql(text(query), engine)
        result = df.to_dict(orient='records')[0]
        
        # Format dates
        result['earliest_forecast'] = str(result['earliest_forecast'])
        result['latest_forecast'] = str(result['latest_forecast'])
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# HISTORICAL DATA ENDPOINTS
# ============================================================================

@app.get("/sales")
def get_sales(
    category: Optional[str] = Query(None, description="Retail category"),
    state: Optional[str] = Query(None, description="Australian state"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: Optional[int] = Query(None, ge=1, le=100000, description="Number of records (returns all if not specified)")
):
    """
    Get historical retail sales data
    
    - **category**: Filter by retail category (optional)
    - **state**: Filter by Australian state (optional)
    - **start_date**: Filter from this date (optional)
    - **end_date**: Filter until this date (optional)
    - **limit**: Maximum records (optional, returns all if not specified)
    """
    try:
        query = """
            SELECT 
                sale_date,
                category,
                state,
                turnover_millions,
                month_name,
                year,
                growth_rate_yoy
            FROM retail_sales
            WHERE 1=1
        """
        
        params = {}
        
        if category:
            query += " AND category = :category"
            params['category'] = category
        
        if state:
            query += " AND state = :state"
            params['state'] = state
        
        if start_date:
            query += " AND sale_date >= :start_date"
            params['start_date'] = start_date
        
        if end_date:
            query += " AND sale_date <= :end_date"
            params['end_date'] = end_date
        
        query += " ORDER BY sale_date DESC"
        
        if limit:
            query += " LIMIT :limit"
            params['limit'] = limit
        
        df = pd.read_sql(text(query), engine, params=params)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No sales data found")
        
        # Convert dates
        df['sale_date'] = df['sale_date'].astype(str)
        
        return {
            "count": len(df),
            "sales": df.to_dict(orient='records')
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sales/summary")
def get_sales_summary():
    """Get summary statistics of historical sales"""
    try:
        query = """
            SELECT 
                COUNT(*) as total_records,
                MIN(sale_date) as earliest_date,
                MAX(sale_date) as latest_date,
                COUNT(DISTINCT category) as categories,
                COUNT(DISTINCT state) as states,
                AVG(turnover_millions) as avg_turnover,
                MIN(turnover_millions) as min_turnover,
                MAX(turnover_millions) as max_turnover
            FROM retail_sales
        """
        
        df = pd.read_sql(text(query), engine)
        result = df.to_dict(orient='records')[0]
        
        # Format dates
        result['earliest_date'] = str(result['earliest_date'])
        result['latest_date'] = str(result['latest_date'])
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# METADATA ENDPOINTS
# ============================================================================

@app.get("/categories")
def get_categories():
    """Get list of all retail categories"""
    try:
        query = """
            SELECT DISTINCT category
            FROM retail_sales
            ORDER BY category
        """
        
        df = pd.read_sql(text(query), engine)
        
        return {
            "count": len(df),
            "categories": df['category'].tolist()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/states")
def get_states():
    """Get list of all Australian states/territories"""
    try:
        query = """
            SELECT DISTINCT state
            FROM retail_sales
            ORDER BY state
        """
        
        df = pd.read_sql(text(query), engine)
        
        return {
            "count": len(df),
            "states": df['state'].tolist()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)