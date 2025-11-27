"""Quick test to verify backtest works"""
from data_loader import get_all_data
import pandas as pd

print("=" * 60)
print("QUICK BACKTEST DATA CHECK")
print("=" * 60)

# Load data
all_data = get_all_data()
print(f"\n✅ Data loaded: {all_data.shape}")

# Check first store
first_store = sorted(all_data["Store"].unique())[0]
store_data = all_data[all_data["Store"] == first_store].sort_values("Date")
print(f"\n📊 Store {first_store}:")
print(f"   Total rows: {len(store_data)}")
print(f"   Unique dates: {store_data['Date'].nunique()}")

# Check if aggregation needed
if "Dept" in store_data.columns:
    dept_counts = store_data.groupby("Date").size()
    multiple_depts = (dept_counts > 1).sum()
    print(f"   Dates with multiple depts: {multiple_depts}")
    
    if multiple_depts > 0:
        print(f"\n   ⚠️  Need to aggregate!")
        print(f"   Example dates with multiple depts:")
        for date, count in dept_counts[dept_counts > 1].head(3).items():
            print(f"      {date}: {count} departments")
        
        # Test aggregation
        features = ["CPI", "Temperature", "IsHoliday", "Fuel_Price", "Unemployment"]
        agg_dict = {"Weekly_Sales": "sum"}
        for feat in features:
            if feat in store_data.columns:
                agg_dict[feat] = "mean"
        
        aggregated = store_data.groupby("Date", as_index=False).agg(agg_dict)
        aggregated["Store"] = first_store
        
        print(f"\n   ✅ After aggregation:")
        print(f"      Rows: {len(aggregated)}")
        print(f"      Columns: {aggregated.columns.tolist()}")
        print(f"      Date range: {aggregated['Date'].min()} to {aggregated['Date'].max()}")
        
        # Check for NaN
        print(f"\n   🔍 NaN check:")
        for col in ["Weekly_Sales"] + features:
            if col in aggregated.columns:
                nan_count = aggregated[col].isna().sum()
                if nan_count > 0:
                    print(f"      ⚠️  {col}: {nan_count} NaN")
                else:
                    print(f"      ✅ {col}: No NaN")
        
        # Check if enough data for 12-week backtest
        weeks_needed = 12 + 20
        if len(aggregated) >= weeks_needed:
            print(f"\n   ✅ Sufficient data for 12-week backtest ({len(aggregated)} >= {weeks_needed})")
        else:
            print(f"\n   ❌ Insufficient data ({len(aggregated)} < {weeks_needed})")
    else:
        print(f"   ✅ One row per date, no aggregation needed")

print("\n" + "=" * 60)


