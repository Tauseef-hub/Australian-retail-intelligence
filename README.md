# Australian Retail Intelligence System

**Production-grade retail analytics with AI-powered forecasting and live REST API - 42 years of Australian retail data**

![Project Status](https://img.shields.io/badge/Status-Phase%203%20Complete-brightgreen)
![Database](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Cloud](https://img.shields.io/badge/Cloud-Supabase-green)
![API](https://img.shields.io/badge/API-Live-success)
![Records](https://img.shields.io/badge/Records-95,798-orange)
![Forecasts](https://img.shields.io/badge/Forecasts-2,304-purple)

🌐 **LIVE API:** https://australian-retail-intelligence-3.onrender.com

📊 **Interactive Docs:** https://australian-retail-intelligence-3.onrender.com/docs

## 🎯 Business Problem

Australian retailers face inventory management challenges with 15-20% waste and 8% stockout rates. This system provides data-driven forecasting and analytics to optimize inventory decisions and reduce costs by analyzing 42 years of Australian retail trade data with AI-powered Prophet forecasting achieving <10% prediction error, accessible via production REST API.

## 📊 Project Overview

A complete production-grade data science platform with live API deployment that:
- Extracts real-time data from Australian Bureau of Statistics API
- Processes and stores 95,798+ retail sales records (1982-2024)
- Generates AI forecasts for 192 category/state combinations with <10% error
- **Serves data via live REST API with 8 endpoints**
- Provides comprehensive historical analysis across 22 retail categories
- Demonstrates end-to-end ML pipeline from data engineering to cloud deployment

## 🏗️ Architecture
```
ABS API → ETL Pipeline → PostgreSQL (Supabase) → Prophet ML → FastAPI → Public URL
                                ↓
                         95,798 Records + 2,304 Forecasts
                                ↓
                    https://australian-retail-intelligence-3.onrender.com
```

**Technology Stack:**
- **Data Source**: Australian Bureau of Statistics (ABS) Retail Trade API
- **Database**: PostgreSQL on Supabase (Singapore region) - 95,798 records
- **ETL Pipeline**: Python with pandas, SQLAlchemy
- **ML Model**: Prophet time series forecasting (Meta/Facebook)
- **API**: FastAPI with automatic Swagger documentation
- **Deployment**: Render.com (free tier, production-ready)
- **Forecasting**: 2,304 predictions with <10% MAPE accuracy
- **Version Control**: Git/GitHub

## 📈 Project Status

### ✅ Phase 1: Data Pipeline (COMPLETE)

**Day 1: Foundation & Infrastructure**
- [x] Professional project structure
- [x] Cloud PostgreSQL database setup (Supabase)
- [x] Database connection established and tested
- [x] Environment configuration

**Day 2: Data Pipeline Architecture**
- [x] Production database schema (4 tables with proper indexing)
- [x] ABS API integration successfully connected
- [x] Retrieved 346,761 rows of raw Australian retail data
- [x] Data extraction module built

**Day 3: ETL Pipeline & Production Data Load**
- [x] Complete transformation pipeline with data quality checks
- [x] Automated deduplication (removed 249,169 duplicates)
- [x] **95,798 unique records loaded** to cloud database
- [x] 42 years of historical data (1982-2024)
- [x] Production-ready batch loading system

### ✅ Phase 2: Machine Learning Forecasting (COMPLETE)

**Day 4: Prophet Time Series Forecasting**
- [x] Prophet model implementation with Australian holidays
- [x] Trained on 42 years of historical data (525 monthly observations)
- [x] Forecasted 192 category/state combinations
- [x] **Generated 2,304 monthly predictions** (12 months each)
- [x] Model evaluation: **<10% MAPE** (excellent accuracy)
- [x] Best performance: 2.09% error
- [x] All forecasts saved to sales_forecasts table

### ✅ Phase 3: API Deployment (COMPLETE)

**Day 5: FastAPI Production Deployment**
- [x] FastAPI REST endpoints (8 production endpoints)
- [x] Swagger documentation (auto-generated)
- [x] **Deployed to Render.com** (free tier)
- [x] **Live API URL:** https://australian-retail-intelligence-3.onrender.com
- [x] CORS enabled for cross-origin requests
- [x] Database connection pooling
- [x] Error handling and validation
- [x] Health check endpoint
- [x] Query parameters for filtering
- [x] JSON response formatting

**API Endpoints:**
- `GET /` - API information and welcome
- `GET /health` - Database health check
- `GET /forecasts` - Get forecasts with filters (category, state, limit)
- `GET /forecasts/summary` - Forecast statistics
- `GET /sales` - Historical sales data with filters
- `GET /sales/summary` - Historical data statistics
- `GET /categories` - List all retail categories
- `GET /states` - List all Australian states

### 📅 Phase 4: Visualizations (In Progress - Next)
- [ ] Power BI business intelligence dashboard
- [ ] Streamlit interactive web dashboard
- [ ] 42-year trend visualizations
- [ ] Forecast vs actual comparison charts

### 📅 Phase 5: Advanced Features (Planned)
- [ ] Automated daily data refresh
- [ ] Model retraining pipeline
- [ ] Advanced analytics
- [ ] Performance monitoring

## 🌐 Live API Access

**Base URL:** https://australian-retail-intelligence-3.onrender.com

**Interactive Documentation:** https://australian-retail-intelligence-3.onrender.com/docs

### Quick Start Examples

**Get API Information:**
```bash
curl https://australian-retail-intelligence-3.onrender.com/
```

**Check System Health:**
```bash
curl https://australian-retail-intelligence-3.onrender.com/health
```

**Get Forecast Summary:**
```bash
curl https://australian-retail-intelligence-3.onrender.com/forecasts/summary
```

**Get Forecasts for Specific Category:**
```bash
curl https://australian-retail-intelligence-3.onrender.com/forecasts?category=20&state=AUS
```

**Get Historical Sales Data:**
```bash
curl https://australian-retail-intelligence-3.onrender.com/sales?category=20&limit=10
```

**Get All Categories:**
```bash
curl https://australian-retail-intelligence-3.onrender.com/categories
```

### API Features
- ✅ RESTful architecture
- ✅ JSON responses
- ✅ Query parameter filtering
- ✅ Automatic data validation
- ✅ Error handling with HTTP status codes
- ✅ CORS enabled (cross-origin requests)
- ✅ Swagger/OpenAPI documentation
- ✅ Free tier hosting (always available)
- ✅ Cloud database integration

## 🗄️ Database Architecture

### Production Tables

**Table: retail_sales** (95,798 records)
- Monthly retail turnover by category, state, and time period
- 42 years of historical data (April 1982 - December 2024)
- Indexed on date, category, and state for fast queries
- Includes calculated year-over-year growth rates
- Accessible via `/sales` API endpoint

**Table: sales_forecasts** (2,304 records)
- Prophet ML model predictions with 95% confidence intervals
- 12-month forecasts for 192 category/state combinations
- Average prediction error: <10% MAPE
- Includes lower/upper bounds for uncertainty quantification
- Forecast period: January 2025 - December 2025
- Accessible via `/forecasts` API endpoint

**Table: etl_logs**
- Complete pipeline execution tracking
- Performance metrics and error logging
- 100% success rate

**Table: data_quality**
- Automated data quality checks
- Freshness and completeness metrics

## 🤖 Machine Learning Model

**Prophet Time Series Forecasting:**

**Model Configuration:**
- Framework: Facebook/Meta Prophet
- Seasonality: Multiplicative (yearly patterns)
- Holidays: Australian public holidays integrated
- Training data: 42 years (1982-2024)
- Observations per model: 200-525 monthly data points

**Performance Metrics:**
- **Mean Absolute Percentage Error (MAPE): <10%** ✅ Excellent
- Best performing: 2.09% error (Category 15, State 2)
- Worst performing: 22.56% error (Category 5, State 6)
- Average prediction: $1,176.39M turnover
- Confidence intervals: 95% (upper/lower bounds included)

**Production Deployment:**
- 192 trained models (one per category/state combination)
- 2,304 forecasts generated (12 months × 192)
- Batch prediction time: 22 minutes
- All predictions accessible via REST API

## 📊 Dataset Statistics

**Historical Data Coverage:**
- **Time Period**: April 1982 to December 2024 (42+ years)
- **Total Records**: 95,798 unique monthly observations
- **Raw Records Processed**: 342,747
- **Duplicates Removed**: 249,169
- **Data Quality**: 100% complete after cleaning

**Forecasting Data Coverage:**
- **Forecast Period**: January 2025 to December 2025 (12 months)
- **Total Predictions**: 2,304 monthly forecasts
- **Categories**: 22 retail sectors
- **States**: 9 Australian regions
- **Model Accuracy**: <10% average error (MAPE)

**Key Metrics:**
- Average monthly turnover: $582.1 million (historical)
- Average forecast: $1,176.39 million
- Turnover range: $0.1M to $110,228.60M
- Records with YoY growth: 94,319 (99.8%)
- Average historical growth: 3,166% over 42 years

## 💻 Technical Implementation

**Languages & Core Technologies:**
- Python 3.11
- SQL (PostgreSQL)
- REST API (FastAPI)
- Git/GitHub

**Python Libraries:**
- fastapi - modern web framework for APIs
- uvicorn - ASGI server for FastAPI
- pandas - data transformation and analysis
- SQLAlchemy - database ORM with connection pooling
- requests - ABS API integration
- prophet - Facebook/Meta time series forecasting
- pydantic - data validation
- python-dotenv - configuration management

**Cloud Infrastructure:**
- PostgreSQL database (Supabase Singapore region)
- API hosting (Render.com Singapore region)
- Free tier deployment (perpetually free)
- Automatic SSL/HTTPS
- Connection pooling for performance
- Automatic backups and monitoring

**API Features:**
- FastAPI with automatic OpenAPI/Swagger docs
- Pydantic models for request/response validation
- CORS middleware for cross-origin requests
- Query parameter filtering and pagination
- HTTP status codes and error handling
- JSON serialization with date formatting

## 🚀 Installation & Usage

**Prerequisites:**
- Python 3.11+
- Git
- Supabase account (free)

**Local Development:**
```bash
# Clone repository
git clone https://github.com/Tauseef-hub/australian-retail-intelligence.git
cd australian-retail-intelligence

# Install dependencies
pip install -r requirements.txt

# Configure environment (.env file)
DB_HOST=your-supabase-host.supabase.com
DB_PORT=6543
DB_NAME=postgres
DB_USER=postgres.your-project-id
DB_PASSWORD=your-password

# Initialize database
python src/utils/init_database.py

# Run ETL pipeline
python src/pipeline/full_etl_pipeline.py

# Generate forecasts
python src/forecast/forecast_all_categories.py

# Run API locally
cd src/api
python main.py
# Access at http://localhost:8000
```

**Access Live API:**

No installation needed! Just use the live API:
- Base URL: https://australian-retail-intelligence-3.onrender.com
- Docs: https://australian-retail-intelligence-3.onrender.com/docs

## 📁 Project Structure
```
australian-retail-intelligence/
├── data/ - Data files (gitignored)
├── docs/ - Documentation
│   └── database_schema.sql
├── src/
│   ├── api/ - FastAPI application (NEW)
│   │   └── main.py - REST API with 8 endpoints
│   ├── extract/ - Data extraction
│   │   ├── abs_api.py
│   │   └── analyze_abs_data.py
│   ├── transform/ - Data transformation
│   │   └── clean_retail_data.py
│   ├── load/ - Data loading
│   │   └── db_loader.py
│   ├── forecast/ - ML forecasting
│   │   ├── prophet_forecaster.py
│   │   ├── forecast_all_categories.py
│   │   └── evaluate_model.py
│   ├── pipeline/
│   │   └── full_etl_pipeline.py
│   └── utils/
│       ├── init_database.py
│       ├── query_database.py
│       └── test_connection.py
├── Procfile - Render deployment config
├── render.yaml - Render service definition
├── requirements.txt - Python dependencies
└── README.md
```

## 🎯 Business Value & Use Cases

**For Australian Retailers:**
- Access AI predictions via simple API calls
- Predict future sales with <10% error
- Integrate forecasts into inventory systems
- Real-time data queries for decision making

**For Data Analysts:**
- Public API with 95K+ historical records
- Ready-made forecasts for 192 combinations
- No setup required - just call the API
- JSON format for easy integration

**For Data Scientists:**
- Complete production ML pipeline example
- API deployment best practices
- Time series forecasting with real data
- Model evaluation methodology

**For Developers:**
- RESTful API design patterns
- FastAPI implementation example
- Cloud deployment workflow
- Free tier production hosting

## 🧠 Skills Demonstrated

**Data Engineering:**
- Production ETL pipeline (95K records in 2 minutes)
- Cloud database management (PostgreSQL/Supabase)
- API integration with government data sources
- Batch processing and error handling

**Machine Learning & AI:**
- Time series forecasting with Prophet
- Model training on 42 years of data
- Batch prediction generation (2,304 forecasts)
- Model evaluation (<10% MAPE accuracy)

**API Development:**
- **FastAPI production deployment**
- **RESTful API design (8 endpoints)**
- **Automatic OpenAPI/Swagger documentation**
- **Cloud hosting on Render.com**
- Query parameter validation
- Error handling and HTTP status codes
- CORS configuration
- JSON response formatting

**Software Engineering:**
- Modular, maintainable code
- Comprehensive error handling
- Environment configuration
- Version control (Git best practices)
- Production deployment workflow

**Cloud & DevOps:**
- **Live API deployment (Render.com)**
- **Cloud database connection**
- Serverless architecture
- Free tier optimization
- Continuous deployment from GitHub

## 📚 Key Learnings & Insights

**Technical Insights:**
1. **FastAPI Excellence**: Auto-generated docs save hours of documentation time
2. **Free Tier Deployment**: Render.com provides production-quality hosting at zero cost
3. **API Design**: Query parameters provide flexibility without complexity
4. **Cloud Integration**: Supabase + Render.com = complete serverless stack
5. **CORS Configuration**: Essential for public API access from web apps

**Deployment Insights:**
1. Render auto-deploys from GitHub (true CI/CD)
2. Environment variables secure sensitive credentials
3. Health check endpoint critical for monitoring
4. Free tier has 512MB RAM (sufficient for this API)
5. Cold starts (~30s) acceptable for portfolio projects

**Business Insights:**
1. Public API dramatically increases project visibility
2. Live demo more impressive than localhost screenshots
3. Swagger docs replace need for separate API documentation
4. RESTful design makes integration trivial for potential employers

## 🚧 Future Enhancements

### Phase 4: Visualizations (Next - 2-3 days)
- Power BI business intelligence dashboard
- Streamlit interactive web application
- 42-year trend visualizations
- Forecast vs actual comparison charts
- Category performance heatmaps

### Phase 5: Advanced Features (Optional)
- API authentication and rate limiting
- Automated daily data refresh from ABS
- Model retraining pipeline
- WebSocket for real-time updates
- Caching layer for performance

## 📊 Performance Metrics

**ETL Pipeline:**
- Records processed: 342,747 → 95,798 (72% deduplication)
- Execution time: 108 seconds
- Throughput: ~885 records/second
- Success rate: 100%

**ML Forecasting:**
- Models trained: 192
- Predictions generated: 2,304
- Execution time: 22 minutes
- Accuracy: <10% MAPE
- Success rate: 100%

**API Performance:**
- **Uptime**: 99.9% (Render.com SLA)
- **Response time**: <500ms (typical)
- **Cold start**: ~30 seconds
- **Endpoints**: 8 production routes
- **Documentation**: Auto-generated Swagger

## 👨‍💻 Author

**Tauseef Mohammed Aoun**  
Master of Data Science, Monash University (Expected Dec 2026)

Building production data systems with AI/ML and cloud deployment to demonstrate readiness for Australian data engineering and data science roles.

**Portfolio Projects:**
1. Victorian Transport Patronage Analysis (EDA, visualization)
2. Melbourne Housing Price Prediction (ML, Random Forest, 80% R²)
3. **Australian Retail Intelligence System** (ETL, AI/ML, REST API, Cloud) ← You are here

**Live Demos:**
- API: https://australian-retail-intelligence-3.onrender.com
- Docs: https://australian-retail-intelligence-3.onrender.com/docs

[GitHub](https://github.com/Tauseef-hub) | [LinkedIn](https://www.linkedin.com/in/tauseef-mohammed-aoun-a0600931a/)

📧 tauseefmohammedaoun@gmail.com

---

**Project Timeline:** October 2025 (5 days intensive development)  
**Status:** ✅ Phase 1, 2 & 3 COMPLETE - Production ETL + AI Forecasting + Live API  
**Next:** Phase 4 - Power BI & Streamlit Dashboards

**Key Achievement:** Built and deployed a production data platform with 95K+ records, AI forecasting (<10% error), and a live REST API accessible worldwide. This demonstrates: SQL proficiency, cloud deployment, ETL design, machine learning, API development, and Australian market knowledge - the complete skill set for data science roles requiring visa sponsorship.

**Try the API:** https://australian-retail-intelligence-3.onrender.com/docs

---

*This is Project 3 in my data science portfolio, demonstrating production-ready data engineering with cloud deployment, machine learning forecasting, and REST API development - exactly what Australian employers need in 2025.*