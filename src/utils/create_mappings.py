from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

def create_mapping_tables():
    """Create both state and category mapping tables"""
    
    print("="*70)
    print("CREATING STATE AND CATEGORY MAPPING TABLES")
    print("="*70)
    
    connection_string = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    engine = create_engine(connection_string, pool_pre_ping=True)
    
    with engine.connect() as conn:
        # ==============================================================
        # TABLE 1: STATE MAPPING
        # ==============================================================
        print("\n1. Creating state_mapping table...")
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS state_mapping (
                state_code VARCHAR(10) PRIMARY KEY,
                state_name VARCHAR(100) NOT NULL,
                state_full_name VARCHAR(200) NOT NULL
            );
        """))
        conn.commit()
        
        # Insert Australian states (ABS standard codes)
        conn.execute(text("""
            INSERT INTO state_mapping (state_code, state_name, state_full_name) VALUES
            ('1', 'NSW', 'New South Wales'),
            ('2', 'VIC', 'Victoria'),
            ('3', 'QLD', 'Queensland'),
            ('4', 'SA', 'South Australia'),
            ('5', 'WA', 'Western Australia'),
            ('6', 'TAS', 'Tasmania'),
            ('7', 'NT', 'Northern Territory'),
            ('8', 'ACT', 'Australian Capital Territory'),
            ('AUS', 'Australia', 'Australia (Total)')
            ON CONFLICT (state_code) DO NOTHING;
        """))
        conn.commit()
        
        print("✅ State mapping created!")
        
        # Verify states
        result = conn.execute(text("SELECT * FROM state_mapping ORDER BY state_code"))
        print("\nState Mappings:")
        for row in result:
            print(f"  {row[0]} → {row[1]} ({row[2]})")
        
        # ==============================================================
        # TABLE 2: CATEGORY MAPPING
        # ==============================================================
        print("\n2. Creating category_mapping table...")
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS category_mapping (
                category_code VARCHAR(10) PRIMARY KEY,
                category_name VARCHAR(200) NOT NULL,
                category_description VARCHAR(500)
            );
        """))
        conn.commit()
        
        # Insert retail categories (ABS Retail Trade categories)
        # These are the standard ANZSIC industry codes used by ABS
        conn.execute(text("""
            INSERT INTO category_mapping (category_code, category_name, category_description) VALUES
            ('20', 'Total Retail Trade', 'Total of all retail trade industries'),
            ('1', 'Food Retailing', 'Supermarkets, grocery stores, fresh food'),
            ('2', 'Household Goods Retailing', 'Furniture, electrical, hardware'),
            ('3', 'Clothing & Footwear', 'Fashion, apparel, shoes, accessories'),
            ('4', 'Department Stores', 'Large department stores and variety stores'),
            ('5', 'Other Retailing', 'Other specialized retail stores'),
            ('6', 'Cafes & Restaurants', 'Food service and dining establishments'),
            ('7', 'Takeaway Food Services', 'Fast food, takeaway outlets'),
            ('8', 'Recreational Goods', 'Sports, toys, books, music'),
            ('9', 'Pharmaceutical & Cosmetic', 'Pharmacies, beauty products'),
            ('10', 'Motor Vehicle Retailing', 'Car dealerships, automotive retail'),
            ('11', 'Fuel Retailing', 'Petrol stations, fuel outlets'),
            ('12', 'Liquor Retailing', 'Bottle shops, liquor stores'),
            ('13', 'Newspaper & Book Retailing', 'News agencies, bookstores'),
            ('14', 'Other Store-Based Retailing', 'Miscellaneous retail stores'),
            ('15', 'Non-Store Retailing', 'Online shopping, mail order')
            ON CONFLICT (category_code) DO NOTHING;
        """))
        conn.commit()
        
        print("✅ Category mapping created!")
        
        # Verify categories
        result = conn.execute(text("SELECT * FROM category_mapping ORDER BY category_code"))
        print("\nCategory Mappings:")
        for row in result:
            print(f"  {row[0]} → {row[1]}")
        
        print("\n" + "="*70)
        print("✅ ALL MAPPING TABLES CREATED SUCCESSFULLY!")
        print("="*70)

if __name__ == "__main__":
    create_mapping_tables()