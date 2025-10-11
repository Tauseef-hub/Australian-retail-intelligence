from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def test_database_connection():
    """Test connection to Supabase PostgreSQL"""
    
    print("Testing database connection...")
    print(f"Host: {os.getenv('DB_HOST')}")
    print(f"Database: {os.getenv('DB_NAME')}")
    
    try:
        # Create connection string
        connection_string = (
            f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )
        
        # Create engine
        engine = create_engine(connection_string, pool_pre_ping=True)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            print("\n✅ DATABASE CONNECTION SUCCESSFUL!")
            print(f"Test query result: {result.fetchone()}")
            
        return True
        
    except Exception as e:
        print(f"\n❌ CONNECTION FAILED!")
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_database_connection()