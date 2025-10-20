from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import numpy as np
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
    limit: int = Query(96000, ge=1, le=100000, description="Number of records (default 96000)")
):
    """
    Get retail sales forecasts WITH proper state and category names
    
    - **category**: Filter by retail category (optional)
    - **state**: Filter by Australian state (optional)
    - **limit**: Maximum number of records (default 96000)
    """
    try:
        query = """
            SELECT 
                sf.forecast_date,
                sf.category as category_code,
                COALESCE(cm.category_name, sf.category) as category_name,
                sf.state as state_code,
                COALESCE(sm.state_name, sf.state) as state_name,
                COALESCE(sm.state_full_name, sf.state) as state_full_name,
                sf.predicted_turnover,
                sf.lower_bound,
                sf.upper_bound,
                sf.confidence_interval,
                sf.model_name,
                sf.model_version
            FROM sales_forecasts sf
            LEFT JOIN state_mapping sm ON sf.state = sm.state_code
            LEFT JOIN category_mapping cm ON sf.category = cm.category_code
            WHERE 1=1
        """
        
        params = {}
        
        if category:
            query += " AND sf.category = :category"
            params['category'] = category
        
        if state:
            query += " AND sf.state = :state"
            params['state'] = state
        
        query += " ORDER BY sf.forecast_date LIMIT :limit"
        params['limit'] = limit
        
        df = pd.read_sql(text(query), engine, params=params)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No forecasts found")
        
        # Replace NaN/NA values with None (JSON compliant)
        df = df.replace({np.nan: None, pd.NA: None, pd.NaT: None})
        df = df.where(pd.notna(df), None)
        
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
    limit: int = Query(96000, ge=1, le=100000, description="Number of records (default 96000)")
):
    """
    Get historical retail sales data WITH proper state and category names
    
    - **category**: Filter by retail category (optional)
    - **state**: Filter by Australian state (optional)
    - **start_date**: Filter from this date (optional)
    - **end_date**: Filter until this date (optional)
    - **limit**: Maximum records (default 96000)
    """
    try:
        query = """
            SELECT 
                rs.sale_date,
                rs.category as category_code,
                COALESCE(cm.category_name, rs.category) as category_name,
                rs.state as state_code,
                COALESCE(sm.state_name, rs.state) as state_name,
                COALESCE(sm.state_full_name, rs.state) as state_full_name,
                rs.turnover_millions,
                rs.month_name,
                rs.year,
                rs.growth_rate_yoy
            FROM retail_sales rs
            LEFT JOIN state_mapping sm ON rs.state = sm.state_code
            LEFT JOIN category_mapping cm ON rs.category = cm.category_code
            WHERE 1=1
        """
        
        params = {}
        
        if category:
            query += " AND rs.category = :category"
            params['category'] = category
        
        if state:
            query += " AND rs.state = :state"
            params['state'] = state
        
        if start_date:
            query += " AND rs.sale_date >= :start_date"
            params['start_date'] = start_date
        
        if end_date:
            query += " AND rs.sale_date <= :end_date"
            params['end_date'] = end_date
        
        query += " ORDER BY rs.sale_date DESC LIMIT :limit"
        params['limit'] = limit
        
        df = pd.read_sql(text(query), engine, params=params)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No sales data found")
        
        # Replace NaN/NA values with None (JSON compliant)
        df = df.replace({np.nan: None, pd.NA: None, pd.NaT: None})
        df = df.where(pd.notna(df), None)
        
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
    """Get list of all retail categories WITH proper names"""
    try:
        query = """
            SELECT DISTINCT 
                rs.category as category_code,
                COALESCE(cm.category_name, rs.category) as category_name
            FROM retail_sales rs
            LEFT JOIN category_mapping cm ON rs.category = cm.category_code
            ORDER BY rs.category
        """
        
        df = pd.read_sql(text(query), engine)
        
        return {
            "count": len(df),
            "categories": df.to_dict(orient='records')
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/states")
def get_states():
    """Get list of all Australian states/territories WITH proper names"""
    try:
        query = """
            SELECT DISTINCT 
                rs.state as state_code,
                COALESCE(sm.state_name, rs.state) as state_name,
                COALESCE(sm.state_full_name, rs.state) as state_full_name
            FROM retail_sales rs
            LEFT JOIN state_mapping sm ON rs.state = sm.state_code
            ORDER BY rs.state
        """
        
        df = pd.read_sql(text(query), engine)
        
        return {
            "count": len(df),
            "states": df.to_dict(orient='records')
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)