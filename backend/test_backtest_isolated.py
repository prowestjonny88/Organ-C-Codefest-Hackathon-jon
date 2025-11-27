"""
ISOLATED BACKTEST TEST - Test the backtest feature independently
Run this to debug the backtest without the API complexity
"""
import pandas as pd
import numpy as np
from prophet import Prophet
from data_loader import get_all_data
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

print("=" * 80)
print("ISOLATED BACKTEST TEST")
print("=" * 80)

try:
    # Step 1: Load data
    print("\n[STEP 1] Loading data...")
    all_data = get_all_data()
    print(f"✅ Loaded {all_data.shape[0]} rows, {all_data.shape[1]} columns")
    
    # Step 2: Get first store
    print("\n[STEP 2] Getting first store...")
    first_store = sorted(all_data["Store"].unique())[0]
    store_data = all_data[all_data["Store"] == first_store].sort_values("Date")
    print(f"✅ Store {first_store}: {len(store_data)} rows")
    print(f"   Unique dates: {store_data['Date'].nunique()}")
    
    # Step 3: Aggregate by date
    print("\n[STEP 3] Aggregating by date...")
    features = ["CPI", "Temperature", "IsHoliday", "Fuel_Price", "Unemployment"]
    
    # Check if multiple departments per date
    dept_counts = store_data.groupby("Date").size()
    if (dept_counts > 1).any():
        print(f"   Multiple departments per date detected. Aggregating...")
        agg_dict = {"Weekly_Sales": "sum"}
        for feat in features:
            if feat in store_data.columns:
                agg_dict[feat] = "first"  # Use first to avoid NaN from mean
        
        aggregated = store_data.groupby("Date", as_index=False).agg(agg_dict)
        aggregated["Store"] = first_store
        
        # Fill any remaining NaN
        for feat in features:
            if feat in aggregated.columns and aggregated[feat].isna().any():
                aggregated[feat] = aggregated[feat].ffill().bfill()
                if aggregated[feat].isna().any():
                    median_val = aggregated[feat].median()
                    if pd.notna(median_val):
                        aggregated[feat] = aggregated[feat].fillna(median_val)
                    else:
                        aggregated[feat] = aggregated[feat].fillna(0)
        
        store_data = aggregated
        print(f"✅ After aggregation: {len(store_data)} unique dates")
    else:
        print(f"✅ One row per date, no aggregation needed")
    
    # Step 4: Split data
    print("\n[STEP 4] Splitting data...")
    weeks = 12
    if len(store_data) < weeks + 20:
        print(f"❌ Insufficient data: {len(store_data)} < {weeks + 20}")
        exit(1)
    
    train = store_data.iloc[:-weeks].copy()
    test = store_data.iloc[-weeks:].copy()
    print(f"✅ Training: {len(train)} rows")
    print(f"✅ Test: {len(test)} rows")
    
    # Step 5: Prepare Prophet data
    print("\n[STEP 5] Preparing Prophet data...")
    available_features = [f for f in features if f in train.columns]
    print(f"   Available features: {available_features}")
    
    df_train = train[["Date", "Weekly_Sales"] + available_features].copy()
    df_train = df_train.rename(columns={"Date": "ds", "Weekly_Sales": "y"})
    df_train = df_train.sort_values("ds").reset_index(drop=True)
    
    # Step 6: Validate and clean data
    print("\n[STEP 6] Validating data...")
    
    # Check for NaN
    nan_counts = df_train.isna().sum()
    if nan_counts.any():
        print(f"   ⚠️  NaN values found:")
        for col, count in nan_counts[nan_counts > 0].items():
            print(f"      {col}: {count}")
        print(f"   Dropping rows with NaN...")
        before = len(df_train)
        df_train = df_train.dropna()
        after = len(df_train)
        print(f"   Dropped {before - after} rows. Remaining: {after}")
    
    # Check for infinite values
    inf_cols = []
    for col in df_train.columns:
        if np.isinf(df_train[col]).any():
            inf_cols.append(col)
            print(f"   ⚠️  Infinite values in {col}")
    
    if inf_cols:
        print(f"   Replacing infinite values...")
        for col in inf_cols:
            df_train[col] = df_train[col].replace([np.inf, -np.inf], np.nan)
            df_train[col] = df_train[col].fillna(df_train[col].median())
    
    # Validate regressors
    valid_features = []
    for feat in available_features:
        if feat not in df_train.columns:
            print(f"   ⚠️  {feat} not in dataframe, skipping")
            continue
        
        if df_train[feat].isna().any():
            print(f"   ⚠️  {feat} has NaN, skipping")
            continue
        
        if np.isinf(df_train[feat]).any():
            print(f"   ⚠️  {feat} has infinite values, skipping")
            continue
        
        if df_train[feat].nunique() <= 1:
            print(f"   ⚠️  {feat} is constant (value={df_train[feat].iloc[0]}), skipping")
            continue
        
        if df_train[feat].std() == 0:
            print(f"   ⚠️  {feat} has zero variance, skipping")
            continue
        
        valid_features.append(feat)
        print(f"   ✅ {feat}: min={df_train[feat].min():.2f}, max={df_train[feat].max():.2f}, std={df_train[feat].std():.2f}")
    
    available_features = valid_features
    print(f"\n   Valid features: {available_features}")
    
    # Step 7: Try simple model first (no regressors)
    print("\n[STEP 7] Testing simple Prophet model (NO regressors)...")
    try:
        model_simple = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            changepoint_prior_scale=0.5
        )
        
        df_simple = df_train[["ds", "y"]].copy()
        print(f"   Fitting with {len(df_simple)} rows...")
        model_simple.fit(df_simple)
        print(f"   ✅ Simple model fitted successfully!")
        
        # Test prediction
        df_future_simple = test[["Date"]].copy()
        df_future_simple = df_future_simple.rename(columns={"Date": "ds"})
        df_future_simple["ds"] = pd.to_datetime(df_future_simple["ds"])
        df_future_simple = df_future_simple.sort_values("ds").reset_index(drop=True)
        
        forecast_simple = model_simple.predict(df_future_simple)
        print(f"   ✅ Prediction successful! Forecast shape: {forecast_simple.shape}")
        
        # Calculate metrics
        actual = test["Weekly_Sales"].values
        predicted = forecast_simple["yhat"].values
        
        mae = np.mean(np.abs(actual - predicted))
        rmse = np.sqrt(np.mean((actual - predicted) ** 2))
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100
        
        print(f"\n   📊 Metrics (Simple Model):")
        print(f"      MAE: {mae:.2f}")
        print(f"      RMSE: {rmse:.2f}")
        print(f"      MAPE: {mape:.2f}%")
        
        print("\n" + "=" * 80)
        print("✅ SUCCESS! Simple model works!")
        print("=" * 80)
        print("\n💡 Solution: Use simple Prophet model without regressors for backtest")
        print("   This is acceptable for hackathon demo.")
        
    except Exception as e:
        print(f"\n   ❌ Simple model failed:")
        print(f"   Error Type: {type(e).__name__}")
        print(f"   Error Message: {str(e)}")
        import traceback
        print(f"\n   Full traceback:")
        print(traceback.format_exc())
        print("\n" + "=" * 80)
        print("❌ EVEN SIMPLE MODEL FAILED - CHECK DATA QUALITY")
        print("=" * 80)
        exit(1)
    
    # Step 8: Try with regressors (optional)
    if available_features:
        print("\n[STEP 8] Testing Prophet model WITH regressors (optional)...")
        try:
            model_with_reg = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=False,
                changepoint_prior_scale=0.5
            )
            
            for feat in available_features:
                model_with_reg.add_regressor(feat)
            
            print(f"   Fitting with {len(df_train)} rows and {len(available_features)} regressors...")
            model_with_reg.fit(df_train)
            print(f"   ✅ Model with regressors fitted successfully!")
            
            # Test prediction
            df_future_reg = test[["Date"] + available_features].copy()
            df_future_reg = df_future_reg.rename(columns={"Date": "ds"})
            df_future_reg["ds"] = pd.to_datetime(df_future_reg["ds"])
            
            # Fill NaN in future
            for feat in available_features:
                if df_future_reg[feat].isna().any():
                    df_future_reg[feat] = df_future_reg[feat].fillna(df_train[feat].mean())
            
            df_future_reg = df_future_reg.sort_values("ds").reset_index(drop=True)
            
            forecast_reg = model_with_reg.predict(df_future_reg)
            print(f"   ✅ Prediction successful! Forecast shape: {forecast_reg.shape}")
            
            print("\n" + "=" * 80)
            print("✅ SUCCESS! Model with regressors also works!")
            print("=" * 80)
            
        except Exception as e:
            print(f"\n   ⚠️  Model with regressors failed (but simple model works):")
            print(f"   Error: {str(e)}")
            print(f"   This is OK - we can use simple model for hackathon")
    
    print("\n" + "=" * 80)
    print("✅ TEST COMPLETE - Backtest feature is working!")
    print("=" * 80)

except Exception as e:
    print(f"\n❌ CRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()
    exit(1)


