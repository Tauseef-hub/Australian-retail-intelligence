-- =============================================
-- AUSTRALIAN RETAIL SALES DATABASE SCHEMA
-- =============================================

-- Table 1: Retail Sales Facts
-- Stores actual sales data from ABS
CREATE TABLE retail_sales (
    sale_id SERIAL PRIMARY KEY,
    sale_date DATE NOT NULL,
    category VARCHAR(200),
    state VARCHAR(50),
    turnover_millions DECIMAL(15, 2),
    month_name VARCHAR(20),
    year INTEGER,
    growth_rate_yoy DECIMAL(5, 2),
    data_source VARCHAR(100) DEFAULT 'ABS_MHSI',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for faster queries
CREATE INDEX idx_sale_date ON retail_sales(sale_date);
CREATE INDEX idx_category ON retail_sales(category);
CREATE INDEX idx_state ON retail_sales(state);
CREATE INDEX idx_year_month ON retail_sales(year, month_name);

-- Table 2: Sales Forecasts
-- Stores ML model predictions
CREATE TABLE sales_forecasts (
    forecast_id SERIAL PRIMARY KEY,
    forecast_date DATE NOT NULL,
    category VARCHAR(200),
    state VARCHAR(50),
    predicted_turnover DECIMAL(15, 2),
    lower_bound DECIMAL(15, 2),
    upper_bound DECIMAL(15, 2),
    confidence_interval DECIMAL(5, 2),
    model_name VARCHAR(100),
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_forecast_date ON sales_forecasts(forecast_date);
CREATE INDEX idx_forecast_category ON sales_forecasts(category);

-- Table 3: ETL Job Logs
-- Track data pipeline runs
CREATE TABLE etl_logs (
    log_id SERIAL PRIMARY KEY,
    job_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    records_processed INTEGER DEFAULT 0,
    records_inserted INTEGER DEFAULT 0,
    records_updated INTEGER DEFAULT 0,
    error_message TEXT,
    execution_time_seconds DECIMAL(10, 2),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE INDEX idx_job_name ON etl_logs(job_name);
CREATE INDEX idx_status ON etl_logs(status);
CREATE INDEX idx_started_at ON etl_logs(started_at);

-- Table 4: Data Quality Metrics
-- Track data freshness and quality
CREATE TABLE data_quality (
    quality_id SERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    metric_name VARCHAR(100),
    metric_value DECIMAL(15, 2),
    check_passed BOOLEAN,
    notes TEXT,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);