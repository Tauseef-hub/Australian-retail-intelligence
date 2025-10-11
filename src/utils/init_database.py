from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

def create_database_tables():
    """Initialize database schema in Supabase"""
    
    print("Initializing database schema...")
    
    # Create connection
    connection_string = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    
    engine = create_engine(connection_string, pool_pre_ping=True)
    
    # Read SQL schema file
    with open('docs/database_schema.sql', 'r') as f:
        schema_sql = f.read()
    
    # Split by semicolons and execute each statement
    statements = [s.strip() for s in schema_sql.split(';') if s.strip()]
    
    try:
        with engine.connect() as conn:
            for i, statement in enumerate(statements, 1):
                if statement:
                    print(f"Executing statement {i}/{len(statements)}...")
                    conn.execute(text(statement))
                    conn.commit()
        
        print("\n✅ DATABASE SCHEMA CREATED SUCCESSFULLY!")
        print("Tables created:")
        print("  - retail_sales")
        print("  - sales_forecasts")
        print("  - etl_logs")
        print("  - data_quality")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR creating schema:")
        print(f"{str(e)}")
        return False

if __name__ == "__main__":
    create_database_tables()