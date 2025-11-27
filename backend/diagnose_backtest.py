"""
Comprehensive diagnostic script to find the exact issue with backtest
"""
from data_loader import get_all_data
import pandas as pd
from prophet import Prophet
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("=" * 80)
print("COMPREHENSIVE BACKTEST DIAGNOSTIC")
print("=" * 80)

try:
    # Step 1: Load data
    print("\n[STEP 1] Loading data...")
    all_data = get_all_data()
    print(f"✅ Data loaded: {all_data.shape}")
    
    # Step 2: Get first store
    print("\n[STEP 2] Getting first store...")
    first_store = sorted(all_data["Store"].unique())[0]
    store_data = all_data[all_data["Store"] == first_store].sort_values("Date")
    print(f"✅ Store {first_store}: {len(store_data)} rows")
    print(f"   Unique dates: {store_data['Date'].nunique()}")
    
    # Step 3: Aggregate
    print("\n[STEP 3] Aggregating by date...")
    features = ["CPI", "Temperature", "IsHoliday", "Fuel_Price", "Unemployment"]
    agg_dict = {"Weekly_Sales": "sum"}
    for feat in features:
        if feat in store_data.columns:
            agg_dict[feat] = "mean"
    
    aggregated = store_data.groupby("Date", as_index=False).agg(agg_dict)
    aggregated["Store"] = first_store
    print(f"✅ After aggregation: {len(aggregated)} rows")
    
    # Step 4: Check for NaN
    print("\n[STEP 4] Checking for NaN values...")
    nan_info = {}
    for col in ["Weekly_Sales"] + features:
        if col in aggregated.columns:
            nan_count = aggregated[col].isna().sum()
            nan_info[col] = nan_count
            if nan_count > 0:
                print(f"   ❌ {col}: {nan_count} NaN values ({nan_count/len(aggregated)*100:.1f}%)")
                # Show which dates have NaN
                nan_dates = aggregated[aggregated[col].isna()]["Date"].head(5)
                print(f"      Example dates with NaN: {nan_dates.tolist()}")
            else:
                print(f"   ✅ {col}: No NaN")
    
    # Step 5: Split data
    print("\n[STEP 5] Splitting data (12 weeks test)...")
    weeks = 12
    if len(aggregated) < weeks + 20:
        print(f"   ❌ Insufficient data: {len(aggregated)} < {weeks + 20}")
    else:
        train = aggregated.iloc[:-weeks].copy()
        test = aggregated.iloc[-weeks:].copy()
        print(f"   ✅ Training: {len(train)} rows")
        print(f"   ✅ Test: {len(test)} rows")
        
        # Step 6: Prepare Prophet training data
        print("\n[STEP 6] Preparing Prophet training data...")
        available_features = [f for f in features if f in train.columns]
        print(f"   Available features: {available_features}")
        
        df_train = train[["Date", "Weekly_Sales"] + available_features].copy()
        df_train = df_train.rename(columns={"Date": "ds", "Weekly_Sales": "y"})
        df_train = df_train.sort_values("ds").reset_index(drop=True)
        
        # Check for NaN again after selection
        print(f"   Checking selected columns for NaN...")
        for col in df_train.columns:
            nan_count = df_train[col].isna().sum()
            if nan_count > 0:
                print(f"      ❌ {col}: {nan_count} NaN")
            else:
                print(f"      ✅ {col}: No NaN")
        
        # Step 7: Check data types
        print("\n[STEP 7] Checking data types...")
        print(f"   ds (date): {df_train['ds'].dtype}")
        print(f"   y (sales): {df_train['y'].dtype}")
        for feat in available_features:
            print(f"   {feat}: {df_train[feat].dtype}")
        
        # Convert date if needed
        if not pd.api.types.is_datetime64_any_dtype(df_train["ds"]):
            print(f"   Converting 'ds' to datetime...")
            df_train["ds"] = pd.to_datetime(df_train["ds"])
        
        # Ensure numeric
        for feat in available_features:
            if not pd.api.types.is_numeric_dtype(df_train[feat]):
                print(f"   Converting '{feat}' to numeric...")
                df_train[feat] = pd.to_numeric(df_train[feat], errors='coerce')
                nan_after = df_train[feat].isna().sum()
                if nan_after > 0:
                    print(f"      ⚠️  {nan_after} NaN values after conversion")
        
        # Step 8: Drop any remaining NaN
        print("\n[STEP 8] Dropping rows with NaN...")
        before_drop = len(df_train)
        df_train = df_train.dropna()
        after_drop = len(df_train)
        if before_drop > after_drop:
            print(f"   ⚠️  Dropped {before_drop - after_drop} rows with NaN")
        print(f"   Final training rows: {after_drop}")
        
        if after_drop < 20:
            print(f"   ❌ Too few rows after dropping NaN: {after_drop} < 20")
        else:
            # Step 9: Try to create Prophet model
            print("\n[STEP 9] Creating Prophet model...")
            try:
                model = Prophet(
                    yearly_seasonality=True,
                    weekly_seasonality=True,
                    daily_seasonality=False,
                    changepoint_prior_scale=0.5
                )
                
                # Add regressors
                for feat in available_features:
                    print(f"   Adding regressor: {feat}")
                    model.add_regressor(feat)
                
                # Step 10: Try to fit
                print("\n[STEP 10] Attempting to fit Prophet model...")
                print(f"   Training data shape: {df_train.shape}")
                print(f"   Training data columns: {df_train.columns.tolist()}")
                print(f"   Training data sample:")
                print(df_train.head())
                
                model.fit(df_train)
                print(f"   ✅ Model fitted successfully!")
                
                # Step 11: Try to predict
                print("\n[STEP 11] Preparing future data...")
                df_future = test[["Date"] + available_features].copy()
                df_future = df_future.rename(columns={"Date": "ds"})
                
                # Handle NaN in future
                for feat in available_features:
                    if df_future[feat].isna().any():
                        df_future[feat] = df_future[feat].fillna(df_train[feat].mean())
                
                df_future["ds"] = pd.to_datetime(df_future["ds"])
                df_future = df_future.sort_values("ds").reset_index(drop=True)
                
                print(f"   Future data shape: {df_future.shape}")
                print(f"   Future data sample:")
                print(df_future.head())
                
                print("\n[STEP 12] Attempting to predict...")
                forecast = model.predict(df_future)
                print(f"   ✅ Prediction successful!")
                print(f"   Forecast shape: {forecast.shape}")
                print(f"   Forecast columns: {forecast.columns.tolist()}")
                print(f"   Forecast sample:")
                print(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].head())
                
                print("\n" + "=" * 80)
                print("✅ ALL STEPS PASSED - BACKTEST SHOULD WORK!")
                print("=" * 80)
                
            except Exception as e:
                print(f"\n   ❌ ERROR at step 9/10/11/12:")
                print(f"   Error Type: {type(e).__name__}")
                print(f"   Error Message: {str(e)}")
                import traceback
                print(f"\n   Full traceback:")
                print(traceback.format_exc())
                print("\n" + "=" * 80)
                print("❌ DIAGNOSTIC FAILED - THIS IS THE ROOT CAUSE!")
                print("=" * 80)

except Exception as e:
    print(f"\n❌ CRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()


