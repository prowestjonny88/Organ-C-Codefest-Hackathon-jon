"""Quick diagnostic script to check Walmart_Sales.csv data"""
from data_loader import get_all_data
import pandas as pd

try:
    df = get_all_data()
    print(f"✅ Data loaded successfully")
    print(f"   Shape: {df.shape}")
    print(f"   Columns: {df.columns.tolist()}")
    print(f"   Date range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"   Unique stores: {sorted(df['Store'].unique())[:10]}")
    
    # Check first store
    first_store = sorted(df['Store'].unique())[0]
    store_data = df[df['Store'] == first_store].sort_values('Date')
    print(f"\n📊 Store {first_store} analysis:")
    print(f"   Rows: {len(store_data)}")
    print(f"   Date range: {store_data['Date'].min()} to {store_data['Date'].max()}")
    
    # Check required features
    required_features = ["CPI", "Temperature", "IsHoliday", "Fuel_Price", "Unemployment"]
    available_features = [f for f in required_features if f in df.columns]
    missing_features = [f for f in required_features if f not in df.columns]
    
    print(f"\n🔍 Feature check:")
    print(f"   Available: {available_features}")
    if missing_features:
        print(f"   ❌ Missing: {missing_features}")
    
    # Check if enough data for 12-week backtest
    weeks_needed = 12 + 20  # 12 weeks test + 20 weeks training
    if len(store_data) >= weeks_needed:
        print(f"   ✅ Sufficient data for 12-week backtest ({len(store_data)} >= {weeks_needed})")
    else:
        print(f"   ❌ Insufficient data for 12-week backtest ({len(store_data)} < {weeks_needed})")
    
    # Check for NaN values in required columns
    if available_features:
        print(f"\n🔍 Data quality check:")
        for feat in available_features:
            nan_count = store_data[feat].isna().sum()
            if nan_count > 0:
                print(f"   ⚠️  {feat}: {nan_count} NaN values")
            else:
                print(f"   ✅ {feat}: No NaN values")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()


