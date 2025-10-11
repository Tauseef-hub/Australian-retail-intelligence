import pandas as pd

def analyze_abs_data():
    """Analyze the ABS sample data to understand structure"""
    
    print("="*70)
    print("ANALYZING AUSTRALIAN RETAIL DATA STRUCTURE")
    print("="*70)
    
    # Load the sample
    df = pd.read_csv('data/abs_sample.csv')
    
    print(f"\n📊 Dataset Overview:")
    print(f"   Total rows: {len(df):,}")
    print(f"   Total columns: {len(df.columns)}")
    
    print(f"\n📋 Columns:")
    for col in df.columns:
        print(f"   - {col}")
    
    print(f"\n🔍 Sample Data:")
    print(df.head(10))
    
    # Unique values analysis
    print(f"\n📈 Unique Values Per Column:")
    for col in df.columns:
        unique_count = df[col].nunique()
        print(f"   {col}: {unique_count} unique values")
        if unique_count < 20:  # Show values if less than 20
            print(f"      → {sorted(df[col].unique())}")
    
    # Time period analysis
    print(f"\n📅 Time Period Range:")
    print(f"   Earliest: {df['TIME_PERIOD'].min()}")
    print(f"   Latest: {df['TIME_PERIOD'].max()}")
    
    # Value analysis
    print(f"\n💰 Sales Value (OBS_VALUE) Statistics:")
    print(f"   Min: {df['OBS_VALUE'].min():.2f}")
    print(f"   Max: {df['OBS_VALUE'].max():.2f}")
    print(f"   Mean: {df['OBS_VALUE'].mean():.2f}")
    print(f"   Median: {df['OBS_VALUE'].median():.2f}")
    
    # Missing values
    print(f"\n⚠️ Missing Values:")
    missing = df.isnull().sum()
    for col in missing[missing > 0].index:
        print(f"   {col}: {missing[col]} ({missing[col]/len(df)*100:.1f}%)")
    
    # MEASURE breakdown
    print(f"\n📊 MEASURE Types:")
    print(df['MEASURE'].value_counts())
    
    # INDUSTRY breakdown
    print(f"\n🏪 INDUSTRY Codes:")
    print(df['INDUSTRY'].value_counts().head(10))
    
    # REGION breakdown
    print(f"\n🗺️ REGION Codes:")
    print(df['REGION'].value_counts())
    
    print("\n" + "="*70)
    print("✅ ANALYSIS COMPLETE!")
    print("="*70)
    
    return df

if __name__ == "__main__":
    df = analyze_abs_data()