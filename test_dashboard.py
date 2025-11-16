"""
Test script to verify dashboard functionality
"""
import pandas as pd
import sys

def test_data_loading():
    """Test loading the sample data"""
    try:
        df = pd.read_csv('sample_data.csv')
        print(f"✅ Data loaded successfully: {len(df)} rows, {len(df.columns)} columns")
        return df
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def test_data_validation(df):
    """Test data validation"""
    required_columns = ['representative', 'doctor', 'division', 'date']
    missing = [col for col in required_columns if col not in df.columns]
    
    if missing:
        print(f"❌ Missing required columns: {missing}")
        return False
    else:
        print(f"✅ All required columns present")
        return True

def test_metrics_calculation(df):
    """Test metrics calculation"""
    try:
        total_calls = len(df)
        total_reps = df['representative'].nunique()
        total_doctors = df['doctor'].nunique()
        total_divisions = df['division'].nunique()
        
        print(f"✅ Metrics calculated successfully:")
        print(f"   - Total Calls: {total_calls}")
        print(f"   - Total Representatives: {total_reps}")
        print(f"   - Total Doctors: {total_doctors}")
        print(f"   - Total Divisions: {total_divisions}")
        return True
    except Exception as e:
        print(f"❌ Error calculating metrics: {e}")
        return False

def test_date_processing(df):
    """Test date column processing"""
    try:
        df['date'] = pd.to_datetime(df['date'])
        print(f"✅ Date processing successful")
        print(f"   - Date range: {df['date'].min()} to {df['date'].max()}")
        return True
    except Exception as e:
        print(f"❌ Error processing dates: {e}")
        return False

def main():
    print("=" * 60)
    print("Call Report Dashboard - Functionality Tests")
    print("=" * 60)
    print()
    
    # Test 1: Data Loading
    print("Test 1: Data Loading")
    df = test_data_loading()
    if df is None:
        sys.exit(1)
    print()
    
    # Test 2: Data Validation
    print("Test 2: Data Validation")
    if not test_data_validation(df):
        sys.exit(1)
    print()
    
    # Test 3: Metrics Calculation
    print("Test 3: Metrics Calculation")
    if not test_metrics_calculation(df):
        sys.exit(1)
    print()
    
    # Test 4: Date Processing
    print("Test 4: Date Processing")
    if not test_date_processing(df.copy()):
        sys.exit(1)
    print()
    
    print("=" * 60)
    print("✅ All tests passed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
