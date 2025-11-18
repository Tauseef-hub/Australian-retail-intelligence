# Australian Retail Intelligence System

**Production-grade retail analytics platform with AI forecasting, live REST API, and executive dashboards - 42 years of Australian retail data**

![Project Status](https://img.shields.io/badge/Status-Phase%204%20Complete-brightgreen)
![Database](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Cloud](https://img.shields.io/badge/Cloud-Supabase-green)
![API](https://img.shields.io/badge/API-Live-success)
![Records](https://img.shields.io/badge/Records-93,578-orange)
![Forecasts](https://img.shields.io/badge/Forecasts-2,304-purple)

🌐 **LIVE API:** https://australian-retail-intelligence-1.onrender.com

📊 **Interactive Docs:** https://australian-retail-intelligence-1.onrender.com/docs

📈 **Power BI Dashboard:** Complete with historical analysis and AI forecasts

## 🎯 Business Problem

Australian retailers face inventory management challenges with 15-20% waste and 8% stockout rates. This system provides data-driven forecasting and analytics to optimize inventory decisions and reduce costs by analyzing 42 years of Australian retail trade data with AI-powered Prophet forecasting achieving <10% prediction error, accessible via production REST API and interactive dashboards.

## 📊 Project Overview

A complete production-grade data science platform demonstrating the full ML lifecycle:

- ✅ **Real-time data extraction** from Australian Bureau of Statistics API
- ✅ **Production ETL pipeline** processing 93,578 clean records (1982-2024)
- ✅ **AI forecasting** for 192 category/state combinations with <10% error
- ✅ **Live REST API** with 8 endpoints and automatic Swagger documentation
- ✅ **Power BI dashboards** with historical analysis and business recommendations
- ✅ **End-to-end deployment** from data engineering to executive reporting

## 🏗️ Architecture
```
ABS API → ETL Pipeline → PostgreSQL (Supabase) → Prophet ML → FastAPI → Power BI
   ↓            ↓                ↓                    ↓           ↓          ↓
Extract    Transform        93,578 Records      2,304 Forecasts  Live API  Dashboard
```

**Technology Stack:**
- **Data Source**: Australian Bureau of Statistics (ABS) Retail Trade API
- **Database**: PostgreSQL on Supabase - 93,578 clean records
- **ETL Pipeline**: Python, pandas, SQLAlchemy
- **ML Model**: Prophet time series forecasting (Meta/Facebook)
- **API**: FastAPI with automatic OpenAPI documentation
- **Visualization**: Power BI Desktop with executive dashboards
- **Deployment**: Render.com (free tier, production-ready)
- **Version Control**: Git/GitHub

## 📈 Project Status

### ✅ Phase 1: Data Pipeline (COMPLETE)

**Foundation & Infrastructure:**
- [x] Professional project structure with modular design
- [x] Cloud PostgreSQL database setup (Supabase Singapore)
- [x] Database connection tested and production-ready
- [x] Environment configuration with secure credentials

**Data Pipeline Architecture:**
- [x] Production database schema (4 tables with proper indexing)
- [x] ABS API integration with data quality filtering
- [x] Retrieved and filtered 342,747 raw records → 101,574 clean records
- [x] **Critical fix**: Filtered to M1 (original) + TSEST 20 to eliminate duplicate series
- [x] Data extraction module with comprehensive error handling

**ETL Pipeline & Production Load:**
- [x] Complete transformation pipeline with data quality validation
- [x] Automated deduplication and null value handling
- [x] **93,578 unique records loaded** to cloud database
- [x] 42 years of monthly data (April 1982 - December 2024)
- [x] Production-ready batch loading with progress tracking

### ✅ Phase 2: Machine Learning Forecasting (COMPLETE)

**Prophet Time Series Implementation:**
- [x] Prophet model with Australian holiday integration
- [x] Trained on clean 42-year historical dataset
- [x] Forecasted 192 category/state combinations
- [x] **Generated 2,304 monthly predictions** (12 months × 192)
- [x] Model evaluation: **<10% MAPE** (excellent accuracy)
- [x] Best performance: 2.09% error
- [x] Confidence intervals (95%) for all predictions
- [x] All forecasts persisted to sales_forecasts table

### ✅ Phase 3: API Deployment (COMPLETE)

**FastAPI Production Deployment:**
- [x] 8 production REST endpoints with full CRUD operations
- [x] Automatic Swagger/OpenAPI documentation
- [x] **Deployed to Render.com** with automatic SSL
- [x] **Live API:** https://australian-retail-intelligence-1.onrender.com
- [x] CORS enabled for cross-origin web requests
- [x] Database connection pooling for performance
- [x] Comprehensive error handling and validation
- [x] Health check endpoint for monitoring
- [x] Query parameters with filtering and pagination
- [x] JSON response formatting with proper serialization

**API Endpoints:**
- `GET /` - API information and welcome
- `GET /health` - Database connection health check
- `GET /forecasts` - AI forecasts with category/state filters
- `GET /forecasts/summary` - Aggregate forecast statistics
- `GET /sales` - Historical sales data with date range filtering
- `GET /sales/summary` - Historical data statistics
- `GET /categories` - List all retail categories with proper names
- `GET /states` - List all Australian states/territories

### ✅ Phase 4: Power BI Dashboard (COMPLETE)

**Interactive Business Intelligence Dashboard:**

**Page 1: Historical Retail Analysis (1982-2024)**
- [x] Executive KPI cards showing:
  - Total records (93,578)
  - Average monthly sales ($582.1M)
  - Data coverage (42 years)
  - Growth trends
- [x] Main visualization: "42 Years of Australian Retail Growth"
  - Smooth monthly trend line
  - Data labels for key points
  - Professional blue color scheme
- [x] Interactive filters for states and categories
- [x] Clean, executive-ready design

**Page 2: AI-Powered Forecasts & Recommendations**
- [x] 4 Executive KPI Cards:
  - Forecast Growth: **3.5%** (projected 2025 growth)
  - Model Accuracy: **<10%** MAPE
  - Average Forecast: **$37.5M** monthly
  - Total Predictions: **2,304** forecasts generated
- [x] Main forecast visualization (Jan-Dec 2025):
  - Clean upward trend (36.96K → 38.25K)
  - Data labels on all points
  - Professional formatting
- [x] Confidence Interval Chart:
  - Predicted values with 95% confidence bands
  - Upper and lower bounds visualized
  - Demonstrates ML uncertainty understanding
- [x] **Strategic Business Recommendations:**
  - Inventory planning (Q4 increase guidance)
  - Workforce optimization (staffing recommendations)
  - Cash flow management (April slowdown mitigation)
  - Risk mitigation strategies
  - Supply chain coordination

**Dashboard Features:**
- Real-time connection to production API
- One-click data refresh capability
- Professional executive-ready design
- Demonstrates complete ML deployment workflow
- Business communication with actionable insights

### 📅 Phase 5: Advanced Features (OPTIONAL)

**Potential Enhancements:**
- [ ] Automated daily data refresh from ABS API
- [ ] Model retraining pipeline with performance monitoring
- [ ] API authentication and rate limiting
- [ ] WebSocket for real-time updates
- [ ] Caching layer for improved performance
- [ ] Email alerts for forecast deviations
- [ ] Streamlit interactive web dashboard

## 🌐 Live API Access

**Base URL:** https://australian-retail-intelligence-1.onrender.com

**Interactive Documentation:** https://australian-retail-intelligence-1.onrender.com/docs

### Quick Start Examples

**Get API Information:**
```bash
curl https://australian-retail-intelligence-1.onrender.com/
```

**Check System Health:**
```bash
curl https://australian-retail-intelligence-1.onrender.com/health
```

**Get Forecast Summary:**
```bash
curl https://australian-retail-intelligence-1.onrender.com/forecasts/summary
```

**Get 2025 Forecasts for Total Retail (Australia):**
```bash
curl https://australian-retail-intelligence-1.onrender.com/forecasts?category=20&state=AUS&limit=12
```

**Get Historical Sales Data:**
```bash
curl https://australian-retail-intelligence-1.onrender.com/sales?category=20&state=AUS&limit=100
```

**Get All Categories with Names:**
```bash
curl https://australian-retail-intelligence-1.onrender.com/categories
```

**Get All States:**
```bash
curl https://australian-retail-intelligence-1.onrender.com/states
```

### API Features
- ✅ RESTful architecture following best practices
- ✅ JSON responses with proper date formatting
- ✅ Query parameter filtering and pagination
- ✅ Automatic Pydantic data validation
- ✅ HTTP status codes and error handling
- ✅ CORS enabled for web applications
- ✅ Automatic Swagger/OpenAPI documentation
- ✅ Free tier hosting (perpetually available)
- ✅ Cloud database with connection pooling
- ✅ Category and state name mapping (readable labels)

## 🗄️ Database Architecture

### Production Tables

**Table: retail_sales** (93,578 records)
- Monthly retail turnover by category, state, and date
- 42 years of historical data (April 1982 - December 2024)
- Indexed on date, category, and state for optimized queries
- Includes calculated year-over-year growth rates
- **Data Quality**: 100% clean after M1+TSEST filtering
- Accessible via `/sales` API endpoint

**Table: sales_forecasts** (2,304 records)
- Prophet ML model predictions with 95% confidence intervals
- 12-month forecasts for 192 category/state combinations
- Average prediction error: <10% MAPE
- Includes upper/lower bounds for uncertainty quantification
- Forecast period: January 2025 - December 2025
- Accessible via `/forecasts` API endpoint

**Table: etl_logs**
- Complete pipeline execution tracking
- Performance metrics and timing data
- Error logging with stack traces
- 100% success rate after optimization

**Table: data_quality**
- Automated data quality checks
- Freshness and completeness metrics
- Historical quality tracking

**Mapping Tables:**
- **state_mapping**: Maps state codes to readable names (NSW, VIC, etc.)
- **category_mapping**: Maps category codes to retail sector names

## 🤖 Machine Learning Model

**Prophet Time Series Forecasting:**

**Model Configuration:**
- Framework: Facebook/Meta Prophet (industry-standard)
- Seasonality: Multiplicative (captures percentage-based patterns)
- Holidays: Australian public holidays integrated
- Training data: 42 years (April 1982 - December 2024)
- Observations per model: 200-525 monthly data points
- Changepoint prior scale: 0.05 (moderate trend flexibility)

**Performance Metrics:**
- **Mean Absolute Percentage Error (MAPE): <10%** ✅ Excellent
- Best performing: 2.09% error (Category 15, State 2)
- Worst performing: 22.56% error (Category 5, State 6)
- Average prediction: $37,476.37M monthly turnover
- Confidence intervals: 95% (statistically rigorous)
- Month-to-month volatility: $152.82M (smooth predictions)

**Production Deployment:**
- 192 trained models (one per category/state combination)
- 2,304 forecasts generated (12 months × 192 combinations)
- Batch prediction time: 23.72 minutes
- All predictions accessible via REST API and Power BI
- Zero failed forecasts (100% success rate)

## 📊 Dataset Statistics

**Historical Data Coverage:**
- **Time Period**: April 1982 to December 2024 (42+ years)
- **Total Clean Records**: 93,578 unique monthly observations
- **Raw Records Retrieved**: 342,747
- **After M1 Filtering**: 101,574
- **Final After Deduplication**: 93,578
- **Data Quality**: 100% complete, zero nulls, no duplicates
- **Unique Dates**: 513 months
- **Categories**: 22 retail sectors
- **States/Territories**: 9 regions

**Data Cleaning Process:**
- **Critical Fix**: Filtered to M1 (original series) + TSEST 20 only
- Removed seasonally adjusted series (avoiding triplicates)
- Removed trend estimates
- Result: Clean monthly data with smooth trends

**Forecasting Data Coverage:**
- **Forecast Period**: January 2025 to December 2025 (12 months)
- **Total Predictions**: 2,304 monthly forecasts
- **Categories**: 22 retail sectors
- **States**: 9 Australian regions
- **Model Accuracy**: <10% average error (MAPE)
- **Confidence Level**: 95% (upper/lower bounds provided)

**Key Metrics:**
- Average monthly turnover: $582.1 million (historical)
- Average 2025 forecast: $37.5 million
- Turnover range: $0.40M to $36,967.40M
- Projected 2025 growth: +3.5%
- Records with YoY growth: 93,319 (99.7%)

## 💻 Technical Implementation

**Languages & Core Technologies:**
- Python 3.11
- SQL (PostgreSQL 14)
- REST API (FastAPI)
- DAX (Power BI)
- Git/GitHub

**Python Libraries:**
- **fastapi** - Modern async web framework for REST APIs
- **uvicorn** - ASGI server for production deployment
- **pandas** - Data transformation and analysis
- **SQLAlchemy** - Database ORM with connection pooling
- **requests** - ABS API integration
- **prophet** - Facebook/Meta time series forecasting
- **pydantic** - Data validation and settings management
- **python-dotenv** - Environment configuration
- **psycopg2** - PostgreSQL database adapter

**Cloud Infrastructure:**
- **Database**: PostgreSQL on Supabase (Singapore region)
- **API Hosting**: Render.com (Singapore region)
- **Deployment**: Free tier (perpetually free)
- **SSL/HTTPS**: Automatic with custom domain support
- **Connection Pooling**: Optimized for concurrent requests
- **Automatic Backups**: Daily snapshots
- **Monitoring**: Built-in health checks

**API Architecture:**
- FastAPI with automatic OpenAPI/Swagger documentation
- Pydantic models for request/response validation
- CORS middleware for web application access
- Query parameter filtering with type validation
- HTTP status codes following REST standards
- JSON serialization with proper date formatting
- Error handling with descriptive messages
- Connection pooling for database efficiency

**Power BI Implementation:**
- Direct Query to REST API endpoints
- Custom DAX measures for KPIs
- Professional blue color theme
- Interactive filters and slicers
- Executive-ready visualizations
- Business recommendations text box

## 🚀 Installation & Usage

**Prerequisites:**
- Python 3.11+
- Git
- Supabase account (free tier)
- Power BI Desktop (for dashboard)

**Local Development:**
```bash
# Clone repository
git clone https://github.com/Tauseef-hub/australian-retail-intelligence.git
cd australian-retail-intelligence

# Install dependencies
pip install -r requirements.txt

# Configure environment (.env file)
DB_HOST=your-supabase-host.supabase.co
DB_PORT=6543
DB_NAME=postgres
DB_USER=postgres.your-project-id
DB_PASSWORD=your-password

# Initialize database schema
python src/utils/init_database.py

# Run ETL pipeline (extracts, transforms, loads data)
python src/pipeline/full_etl_pipeline.py

# Generate ML forecasts
python src/forecast/forecast_all_categories.py

# Run API locally
python src/api/main.py
# Access at http://localhost:8000
# Docs at http://localhost:8000/docs
```

**Access Live API:**

No installation needed! Use the production API:
- **Base URL**: https://australian-retail-intelligence-1.onrender.com
- **Interactive Docs**: https://australian-retail-intelligence-1.onrender.com/docs

**Power BI Dashboard:**

1. Open `visuals/Australian_Retail_Intelligence_Dashboard.pbix`
2. Refresh data to load latest from API
3. Explore both pages (Historical + Forecasts)

## 📁 Project Structure
```
australian-retail-intelligence/
├── data/                              # Data files (gitignored)
├── docs/                              # Documentation
│   └── database_schema.sql           # Production database schema
├── src/
│   ├── api/                          # FastAPI application
│   │   └── main.py                   # REST API with 8 endpoints
│   ├── extract/                      # Data extraction
│   │   ├── abs_api.py                # ABS API integration (M1+TSEST filter)
│   │   └── analyze_abs_data.py       # Data exploration utilities
│   ├── transform/                    # Data transformation
│   │   └── clean_retail_data.py      # Cleaning and validation logic
│   ├── load/                         # Data loading
│   │   └── db_loader.py              # Database insertion with batching
│   ├── forecast/                     # ML forecasting
│   │   ├── prophet_forecaster.py     # Prophet model implementation
│   │   ├── forecast_all_categories.py # Batch forecast generation
│   │   └── evaluate_model.py         # Model accuracy evaluation
│   ├── pipeline/                     # ETL orchestration
│   │   └── full_etl_pipeline.py      # Complete ETL workflow
│   └── utils/                        # Utilities
│       ├── init_database.py          # Database initialization
│       ├── query_database.py         # Data verification queries
│       ├── create_mappings.py        # Category/state name mappings
│       └── test_connection.py        # Connection testing
├── visuals/                          # Power BI files (NEW)
│   ├── Australian_Retail_Intelligence_Dashboard.pbix
│   ├── Australian_Retail_Dashboard_Page_1.png
│   └── Australian_Retail_Dashboard_Page_2.png
├── Procfile                          # Render deployment config
├── render.yaml                       # Render service definition
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git exclusions
└── README.md                         # This file
```

## 🎯 Business Value & Use Cases

**For Australian Retailers:**
- Access AI predictions via simple API calls
- Predict future sales with <10% error rate
- Integrate forecasts into existing inventory systems
- Make data-driven purchasing decisions
- Reduce waste and stockout rates

**For Data Analysts:**
- Public API with 93K+ historical records
- Ready-made forecasts for 192 combinations
- No setup required - just call the API
- JSON format for easy Excel/BI tool integration
- Power BI dashboard for immediate insights

**For Data Scientists:**
- Complete production ML pipeline example
- API deployment best practices demonstrated
- Time series forecasting with real-world data
- Model evaluation methodology
- Clean, documented codebase for learning

**For Business Executives:**
- Power BI dashboard with strategic recommendations
- Clear KPIs and growth projections
- Confidence intervals showing forecast reliability
- Actionable insights for operational planning

## 🧠 Skills Demonstrated

**Data Engineering:**
- Production ETL pipeline (93K records processed)
- Cloud database management (PostgreSQL/Supabase)
- API integration with government data sources
- Data quality engineering (duplicate detection/removal)
- Batch processing with progress tracking

**Machine Learning & AI:**
- Time series forecasting with Prophet
- Model training on 42 years of data
- Batch prediction generation (2,304 forecasts)
- Model evaluation and accuracy measurement (<10% MAPE)
- Confidence interval calculation

**API Development & Deployment:**
- FastAPI production implementation
- RESTful API design (8 endpoints)
- Automatic OpenAPI/Swagger documentation
- Cloud hosting on Render.com
- Query parameter validation
- Error handling with proper HTTP codes
- CORS configuration for web access
- JSON response formatting

**Data Visualization:**
- Power BI dashboard design
- Executive KPI card creation
- Interactive filtering and slicing
- Confidence interval visualization
- Business storytelling with recommendations

**Software Engineering:**
- Modular, maintainable code architecture
- Comprehensive error handling
- Environment configuration management
- Version control with Git
- Production deployment workflow
- Documentation and code comments

**Cloud & DevOps:**
- Live API deployment (Render.com)
- Cloud database configuration (Supabase)
- Serverless architecture
- Environment variable management
- Continuous deployment from GitHub
- Free tier optimization

**Business Communication:**
- Strategic recommendation writing
- Executive dashboard design
- Technical to business translation
- Actionable insight generation

## 📚 Key Learnings & Insights

**Critical Data Quality Fix:**
- **Problem**: ABS API returns multiple data series per date (MEASURE × TSEST combinations)
- **Impact**: Created triplicates in database (95K records with quarterly spikes)
- **Solution**: Filter to M1 (original series) + TSEST 20 only
- **Result**: Clean 93K unique records with smooth monthly trends

**Technical Insights:**
1. **API Design**: Query parameters provide flexibility without complexity
2. **Cloud Integration**: Supabase + Render = complete free-tier stack
3. **Prophet Excellence**: <10% error achievable with proper data cleaning
4. **FastAPI Benefits**: Auto-generated docs save documentation time
5. **Power BI Integration**: Direct API connection enables real-time dashboards

**Deployment Insights:**
1. Render.com auto-deploys from GitHub (true CI/CD)
2. Environment variables essential for security
3. Health check endpoints critical for monitoring
4. Free tier sufficient for portfolio projects
5. Cold starts (~30s) acceptable for demos

**Business Insights:**
1. Forecasts without recommendations lack business value
2. Confidence intervals demonstrate ML understanding
3. Executive dashboards require different design than analyst tools
4. Australian market knowledge strengthens visa applications

## 🚧 Optional Future Enhancements

**Advanced Features:**
- API authentication and rate limiting
- Automated daily data refresh from ABS
- Model retraining pipeline with drift detection
- WebSocket for real-time updates
- Redis caching layer for performance
- Email alerts for forecast deviations
- Streamlit web application
- Docker containerization
- Kubernetes deployment
- CI/CD pipeline with testing
- Load balancing for scale

## 📊 Performance Metrics

**ETL Pipeline:**
- Raw records retrieved: 342,747
- After M1+TSEST filtering: 101,574
- Final clean records: 93,578
- Execution time: 67.32 seconds
- Throughput: ~1,390 records/second
- Success rate: 100%

**ML Forecasting:**
- Models trained: 192
- Predictions generated: 2,304
- Execution time: 23.72 minutes
- Average accuracy: <10% MAPE
- Best model: 2.09% error
- Success rate: 100%

**API Performance:**
- Uptime: 99.9% (Render.com SLA)
- Response time: <500ms (typical)
- Cold start: ~30 seconds
- Endpoints: 8 production routes
- Documentation: Auto-generated Swagger
- CORS: Enabled for all origins

**Power BI Dashboard:**
- Data refresh time: ~30-60 seconds
- Pages: 2 (Historical + Forecasts)
- Visualizations: 8 (cards, charts, recommendations)
- Interactivity: Filters, slicers, drill-through

## 👨‍💻 Author

**Tauseef Mohammed Aoun**  
Master of Data Science, Monash University (Expected December 2026)  
Melbourne, Australia

**Building production data systems**

**Portfolio Projects:**
1. Victorian Transport Patronage Analysis (EDA, Visualization)
2. Melbourne Housing Price Prediction (ML, Random Forest, 80% R²)
3. **Australian Retail Intelligence System** (ETL, ML, API, Dashboard) ← You are here

**Live Demonstrations:**
- **API**: https://australian-retail-intelligence-1.onrender.com
- **Docs**: https://australian-retail-intelligence-1.onrender.com/docs
- **Dashboard**: Available in repository (`visuals/` folder)

**Connect:**
- [GitHub](https://github.com/Tauseef-hub)
- [LinkedIn](https://www.linkedin.com/in/tauseef-mohammed-aoun-a0600931a/)
- 📧 tauseefmohammedaoun@gmail.com

---

## 📅 Project Timeline

**Development Period:** October-November 2025 (6 weeks)  
**Total Hours:** ~50 hours intensive development

- **Week 1-2**: ETL Pipeline & Data Quality (Phase 1)
- **Week 3**: Machine Learning Forecasting (Phase 2)
- **Week 4**: API Development & Deployment (Phase 3)
- **Week 5-6**: Power BI Dashboard & Documentation (Phase 4)

---

## ✅ Project Status

**Current Status:** ✅ **ALL PHASES COMPLETE - PRODUCTION READY**

**What's Deployed:**
- ✅ 93,578 clean historical records in cloud database
- ✅ 2,304 AI forecasts with <10% accuracy
- ✅ Live REST API with 8 endpoints
- ✅ Power BI dashboard with business recommendations
- ✅ Complete documentation and code

**Optional Next Steps:**
- Advanced features (authentication, caching, automation)
- Additional visualizations (Streamlit web app)
- Model improvements (ensemble methods, feature engineering)

---

## 🌟 Key Achievement

Built and deployed a **complete production data science platform** demonstrating:

✅ **Technical Excellence**
- SQL database design and optimization
- Python ETL pipeline with data quality engineering
- Machine learning model training and evaluation
- REST API development and cloud deployment
- Business intelligence dashboard creation

✅ **Business Acumen**
- Translated ML forecasts into strategic recommendations
- Created executive-ready visualizations
- Demonstrated understanding of retail operations
- Showed ability to communicate with non-technical stakeholders

✅ **Visa Sponsorship Readiness**
- Production-quality code and documentation
- Australian market knowledge (ABS data, local context)
- End-to-end project ownership
- Senior-level technical and business skills

**This project proves I can build production systems, not just run notebooks.**

---

**Try the Live API:** https://australian-retail-intelligence-1.onrender.com/docs

---

*This is Project 3 in my data science portfolio, demonstrating the complete ML lifecycle from data engineering through deployment to executive reporting.*