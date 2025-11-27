"""Test script to debug backtest issues"""
from data_loader import get_all_data
from routes.backtest import get_backtest_comparison
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

print("=" * 60)
print("BACKTEST DIAGNOSTIC TEST")
print("=" * 60)

try:
    # Step 1: Load data
    print("\n[Step 1] Loading data...")
    all_data = get_all_data()
    print(f"✅ Data loaded: {all_data.shape}")
    print(f"   Columns: {all_data.columns.tolist()}")
    
    # Step 2: Check first store
    print("\n[Step 2] Analyzing first store...")
    first_store = sorted(all_data["Store"].unique())[0]
    store_data = all_data[all_data["Store"] == first_store].sort_values("Date")
    print(f"✅ Store {first_store}: {len(store_data)} rows")
    print(f"   Date range: {store_data['Date'].min()} to {store_data['Date'].max()}")
    
    # Step 3: Check for multiple departments
    print("\n[Step 3] Checking for multiple departments per date...")
    if "Dept" in store_data.columns:
        dept_counts = store_data.groupby("Date").size()
        print(f"   Unique dates: {len(dept_counts)}")
        print(f"   Dates with multiple depts: {(dept_counts > 1).sum()}")
        if (dept_counts > 1).any():
            print(f"   ⚠️  Need to aggregate! Example: {dept_counts[dept_counts > 1].head(3).to_dict()}")
            
            # Test aggregation
            features = ["CPI", "Temperature", "IsHoliday", "Fuel_Price", "Unemployment"]
            agg_dict = {"Weekly_Sales": "sum"}
            for feat in features:
                if feat in store_data.columns:
                    agg_dict[feat] = "mean"
            
            aggregated = store_data.groupby("Date", as_index=False).agg(agg_dict)
            print(f"   ✅ After aggregation: {len(aggregated)} rows")
            print(f"   Aggregated columns: {aggregated.columns.tolist()}")
        else:
            print(f"   ✅ One row per date, no aggregation needed")
    
    # Step 4: Check features
    print("\n[Step 4] Checking required features...")
    features = ["CPI", "Temperature", "IsHoliday", "Fuel_Price", "Unemployment"]
    available = [f for f in features if f in store_data.columns]
    missing = [f for f in features if f not in store_data.columns]
    print(f"   Available: {available}")
    if missing:
        print(f"   ❌ Missing: {missing}")
    
    # Step 5: Check for NaN values
    print("\n[Step 5] Checking for NaN values...")
    if available:
        for feat in available:
            nan_count = store_data[feat].isna().sum()
            if nan_count > 0:
                print(f"   ⚠️  {feat}: {nan_count} NaN values ({nan_count/len(store_data)*100:.1f}%)")
            else:
                print(f"   ✅ {feat}: No NaN values")
    
    # Step 6: Test actual backtest endpoint
    print("\n[Step 6] Testing backtest endpoint...")
    print("   Calling get_backtest_comparison(store_id=1, weeks=12)...")
    try:
        result = get_backtest_comparison(store_id=1, weeks=12)
        print(f"   ✅ SUCCESS!")
        print(f"   Store ID: {result['store_id']}")
        print(f"   Comparison points: {len(result['comparison'])}")
        print(f"   Metrics: MAE={result['metrics']['mae']:.2f}, RMSE={result['metrics']['rmse']:.2f}, MAPE={result['metrics']['mape']:.2f}%")
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        import traceback
        print("\n   Full traceback:")
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ CRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()


