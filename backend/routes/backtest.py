"""
Backtest Comparison Endpoint

Provides predicted vs actual comparison data for visualization.
Based on the 3-month (12-week) backtest from the Colab notebook.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from prophet import Prophet
from data_loader import get_time_series, get_all_data
from ml.model import get_model
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

router = APIRouter()

# For hackathon: Use pre-trained model if compatible, otherwise train quick model
def get_prophet_model_for_backtest(train_df: pd.DataFrame, available_features: List[str]):
    """
    Get Prophet model for backtesting.
    For hackathon: Train a quick model that matches the data structure.
    (Pre-trained model may be trained on different data/features)
    """
    # Train a new model that matches the current data structure
    # This ensures compatibility and fast execution for the hackathon
    logger.info(f"Creating Prophet model for backtest with features: {available_features}")
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        changepoint_prior_scale=0.5
    )
    
    # Add regressors (features)
    for feat in available_features:
        model.add_regressor(feat)
    
    return model
    return model


@router.get("/comparison")
def get_backtest_comparison(
    store_id: Optional[int] = Query(default=None, description="Store ID (optional, returns all stores if not provided)"),
    weeks: int = Query(default=12, ge=1, le=26, description="Number of weeks to backtest (default: 12 weeks = 3 months)")
):
    """
    Get predicted vs actual comparison data for backtesting visualization.
    
    This performs a backtest similar to the Colab notebook:
    - Uses all data except last N weeks for training
    - Forecasts the last N weeks
    - Compares predictions to actual values
    - Returns data ready for visualization
    
    Returns:
    - List of comparison data points with Date, Actual, Forecast
    - Metrics: MAE, RMSE, MAPE
    """
    try:
        # Get all data
        all_data = get_all_data()
        if all_data.empty:
            raise HTTPException(status_code=404, detail="No data available")
        
        # Features used in the model
        # Walmart data uses "IsHoliday" not "Holiday_Flag"
        features = ["CPI", "Temperature", "IsHoliday", "Fuel_Price", "Unemployment"]
        
        results = []
        
        # Get stores to evaluate
        if store_id:
            stores = [store_id]
        else:
            # Use first store for demonstration (faster response)
            # Users can specify store_id to see other stores
            stores = [sorted(all_data["Store"].unique())[0]]
        
        for store in stores:
            try:
                # Get store data
                store_data = all_data[all_data["Store"] == store].sort_values("Date")
                
                # Aggregate by Date if there are multiple departments per store
                # (Walmart data has multiple departments per store per date)
                if "Dept" in store_data.columns:
                    # Check if we have multiple rows per date
                    dates_with_multiple = store_data.groupby("Date").size()
                    if (dates_with_multiple > 1).any():
                        logger.info(f"Store {store} has multiple departments per date. Aggregating by date...")
                        # Aggregate: sum Weekly_Sales, take mean of other numeric features
                        # Use 'first' for features that should be constant per date (avoids NaN from mean)
                        agg_dict = {"Weekly_Sales": "sum"}
                        for feat in features:
                            if feat in store_data.columns:
                                # Use 'first' to avoid NaN from mean() when some departments have NaN
                                # Features like CPI, Temperature, Fuel_Price should be same per date anyway
                                agg_dict[feat] = "first"
                        # Keep first value for non-numeric columns
                        for col in store_data.columns:
                            if col not in agg_dict and col not in ["Date", "Store", "Dept"]:
                                if pd.api.types.is_numeric_dtype(store_data[col]):
                                    agg_dict[col] = "mean"
                                else:
                                    agg_dict[col] = "first"
                        
                        store_data = store_data.groupby("Date", as_index=False).agg(agg_dict)
                        # Re-add Store column (lost during aggregation)
                        store_data["Store"] = store
                        
                        # Fill any remaining NaN values (in case 'first' still produces NaN)
                        for feat in features:
                            if feat in store_data.columns and store_data[feat].isna().any():
                                # Forward fill then backward fill
                                store_data[feat] = store_data[feat].ffill().bfill()
                                # If still NaN, use median of all values
                                if store_data[feat].isna().any():
                                    median_val = store_data[feat].median()
                                    if pd.notna(median_val):
                                        store_data[feat] = store_data[feat].fillna(median_val)
                                    else:
                                        # Last resort: fill with 0
                                        store_data[feat] = store_data[feat].fillna(0)
                        
                        logger.info(f"After aggregation: {len(store_data)} unique dates")
                
                logger.info(f"Processing store {store}: {len(store_data)} rows")
                
                if len(store_data) < weeks + 20:  # Need at least weeks + some training data
                    logger.warning(f"Store {store} has insufficient data for {weeks}-week backtest: {len(store_data)} rows (need at least {weeks + 20})")
                    continue
                
                # Split: all except last N weeks for training, last N weeks for testing
                train = store_data.iloc[:-weeks].copy()
                test = store_data.iloc[-weeks:].copy()
                
                # Prepare Prophet dataframe for training
                # Only use features that exist in the data
                available_features = [f for f in features if f in train.columns]
                missing_features = [f for f in features if f not in train.columns]
                
                if missing_features:
                    logger.warning(f"Store {store} missing features: {missing_features}")
                
                if not available_features:
                    logger.warning(f"Store {store} has no available features, skipping. Available columns: {train.columns.tolist()}")
                    continue
                
                logger.info(f"Store {store} using features: {available_features}")
                
                df_train = train[["Date", "Weekly_Sales"] + available_features].copy()
                
                # Check for NaN values and handle them
                nan_counts = df_train.isna().sum()
                if nan_counts.any():
                    logger.warning(f"Store {store} has NaN values: {nan_counts[nan_counts > 0].to_dict()}")
                    # Drop rows with NaN in required columns
                    df_train = df_train.dropna(subset=["Date", "Weekly_Sales"] + available_features)
                    logger.info(f"After dropping NaN rows: {len(df_train)} rows remaining")
                    if len(df_train) < 20:
                        logger.warning(f"Store {store} has too few rows after dropping NaN values")
                        continue
                
                df_train = df_train.rename(columns={"Date": "ds", "Weekly_Sales": "y"})
                
                # Ensure date column is datetime
                if not pd.api.types.is_datetime64_any_dtype(df_train["ds"]):
                    df_train["ds"] = pd.to_datetime(df_train["ds"])
                
                # Ensure all feature columns are numeric
                for feat in available_features:
                    if not pd.api.types.is_numeric_dtype(df_train[feat]):
                        df_train[feat] = pd.to_numeric(df_train[feat], errors='coerce')
                        df_train = df_train.dropna(subset=[feat])
                
                if len(df_train) < 20:
                    logger.warning(f"Store {store} has too few rows after data cleaning")
                    continue
                
                # Get and fit Prophet model for backtesting
                logger.info(f"Creating Prophet model for store {store}...")
                
                # Validate training data before fitting
                logger.info(f"Validating training data for store {store}...")
                logger.info(f"   Training rows: {len(df_train)}")
                logger.info(f"   Columns: {df_train.columns.tolist()}")
                logger.info(f"   Date range: {df_train['Date'].min()} to {df_train['Date'].max()}")
                logger.info(f"   Weekly_Sales range: {df_train['Weekly_Sales'].min():.2f} to {df_train['Weekly_Sales'].max():.2f}")
                for feat in available_features:
                    logger.info(f"   {feat}: min={df_train[feat].min():.2f}, max={df_train[feat].max():.2f}, NaN={df_train[feat].isna().sum()}")
                
                # Prepare training dataframe for Prophet
                df_train_prophet = df_train[["Date", "Weekly_Sales"] + available_features].copy()
                df_train_prophet = df_train_prophet.rename(columns={"Date": "ds", "Weekly_Sales": "y"})
                
                # Ensure df_train is sorted by date (Prophet requirement)
                df_train_prophet = df_train_prophet.sort_values("ds").reset_index(drop=True)
                
                # Final validation before fitting
                if df_train_prophet["y"].isna().any():
                    logger.error(f"❌ Training data still has NaN in 'y' column: {df_train_prophet['y'].isna().sum()} NaN values")
                    raise ValueError("Training data contains NaN in target variable 'y'")
                
                if df_train_prophet["ds"].isna().any():
                    logger.error(f"❌ Training data still has NaN in 'ds' column")
                    raise ValueError("Training data contains NaN in date column 'ds'")
                
                # Check for infinite values
                if np.isinf(df_train_prophet["y"]).any():
                    logger.error(f"❌ Training data contains infinite values in 'y' column")
                    raise ValueError("Training data contains infinite values in target variable 'y'")
                
                # Validate regressors and remove problematic ones
                valid_features = []
                for feat in available_features:
                    if df_train_prophet[feat].isna().any():
                        logger.warning(f"⚠️  Regressor '{feat}' has NaN values, skipping")
                        continue
                    
                    if np.isinf(df_train_prophet[feat]).any():
                        logger.warning(f"⚠️  Regressor '{feat}' has infinite values, skipping")
                        continue
                    
                    # Check if regressor is constant (all same value)
                    if df_train_prophet[feat].nunique() <= 1:
                        logger.warning(f"⚠️  Regressor '{feat}' is constant (all values are {df_train_prophet[feat].iloc[0]}), skipping")
                        continue
                    
                    # Check if regressor has zero variance
                    if df_train_prophet[feat].std() == 0:
                        logger.warning(f"⚠️  Regressor '{feat}' has zero variance, skipping")
                        continue
                    
                    valid_features.append(feat)
                
                # Update available_features to only valid ones
                if len(valid_features) < len(available_features):
                    logger.warning(f"⚠️  Removed {len(available_features) - len(valid_features)} problematic regressors. Using: {valid_features}")
                    available_features = valid_features
                
                if not available_features:
                    logger.warning(f"⚠️  No valid regressors available, will use model without regressors")
                
                # Try to fit model with regressors first
                model = None
                fit_success = False
                fit_error = None
                
                # Attempt 1: Model with regressors (if we have valid ones)
                if available_features:
                    try:
                        logger.info(f"Attempting to fit Prophet model WITH regressors for store {store}...")
                        model = get_prophet_model_for_backtest(df_train_prophet, available_features)
                        model.fit(df_train_prophet)
                        logger.info(f"✅ Model fitted successfully WITH regressors for store {store}")
                        fit_success = True
                    except Exception as e:
                        fit_error = e
                        logger.warning(f"⚠️ Model with regressors failed: {fit_error}")
                        logger.warning(f"   Trying simpler model WITHOUT regressors as fallback...")
                        fit_success = False
                else:
                    logger.info(f"No valid regressors available, using model WITHOUT regressors...")
                    fit_success = False
                
                # Attempt 2: Simple model without regressors (fallback or if no valid regressors)
                if not fit_success:
                    try:
                        logger.info(f"Attempting to fit simple Prophet model WITHOUT regressors for store {store}...")
                        model = Prophet(
                            yearly_seasonality=True,
                            weekly_seasonality=True,
                            daily_seasonality=False,
                            changepoint_prior_scale=0.5
                        )
                        # Use only ds and y columns
                        df_train_simple = df_train_prophet[["ds", "y"]].copy()
                        model.fit(df_train_simple)
                        logger.info(f"✅ Simple model fitted successfully (without regressors) for store {store}")
                        fit_success = True
                        # Update available_features to empty since we're not using regressors
                        available_features = []
                    except Exception as simple_fit_error:
                        logger.error(f"❌ Both model attempts failed!")
                        if fit_error:
                            logger.error(f"   With regressors: {fit_error}")
                        logger.error(f"   Without regressors: {simple_fit_error}")
                        logger.error(f"   Training data shape: {df_train_prophet.shape}")
                        logger.error(f"   Training data dtypes:\n{df_train_prophet.dtypes}")
                        logger.error(f"   Training data sample:\n{df_train_prophet.head()}")
                        logger.error(f"   Training data tail:\n{df_train_prophet.tail()}")
                        logger.error(f"   NaN counts:\n{df_train_prophet.isna().sum()}")
                        logger.error(f"   y stats: min={df_train_prophet['y'].min()}, max={df_train_prophet['y'].max()}, mean={df_train_prophet['y'].mean()}, std={df_train_prophet['y'].std()}")
                        raise ValueError(f"Prophet model fitting failed with and without regressors. Last error: {simple_fit_error}")
                
                if not fit_success or model is None:
                    raise ValueError("Failed to fit Prophet model")
                
                # Prepare future dataframe for testing period
                if available_features:
                    df_future = test[["Date"] + available_features].copy()
                else:
                    # No regressors, just dates
                    df_future = test[["Date"]].copy()
                
                # Handle NaN values in test data (only if we have regressors)
                if available_features:
                    nan_counts = df_future.isna().sum()
                    if nan_counts.any():
                        logger.warning(f"Store {store} test data has NaN values: {nan_counts[nan_counts > 0].to_dict()}")
                        # Forward fill NaN values for features (use last known value)
                        for feat in available_features:
                            if df_future[feat].isna().any():
                                # Use ffill (forward fill) then bfill (backward fill)
                                df_future[feat] = df_future[feat].ffill().bfill()
                                # If still NaN, use mean from training data
                                if df_future[feat].isna().any() and feat in df_train_prophet.columns:
                                    train_mean = df_train_prophet[feat].mean()
                                    df_future[feat] = df_future[feat].fillna(train_mean)
                                    logger.info(f"Filled NaN in {feat} with training mean: {train_mean}")
                                elif df_future[feat].isna().any():
                                    df_future[feat] = df_future[feat].fillna(0)
                                    logger.warning(f"Filled NaN in {feat} with 0 (no training data)")
                
                df_future = df_future.rename(columns={"Date": "ds"})
                
                # Ensure date column is datetime
                if not pd.api.types.is_datetime64_any_dtype(df_future["ds"]):
                    df_future["ds"] = pd.to_datetime(df_future["ds"])
                
                # Ensure all feature columns are numeric (only if we have regressors)
                if available_features:
                    for feat in available_features:
                        if not pd.api.types.is_numeric_dtype(df_future[feat]):
                            df_future[feat] = pd.to_numeric(df_future[feat], errors='coerce')
                            # Use training data mean if available
                            if feat in df_train_prophet.columns:
                                df_future[feat] = df_future[feat].fillna(df_train_prophet[feat].mean())
                            else:
                                df_future[feat] = df_future[feat].fillna(0)
                
                # Make predictions
                logger.info(f"Making predictions for {len(df_future)} test periods...")
                logger.info(f"   Future data columns: {df_future.columns.tolist()}")
                logger.info(f"   Future data shape: {df_future.shape}")
                
                # Validate future dataframe has all required regressors
                model_regressors = list(model.extra_regressors.keys()) if hasattr(model, 'extra_regressors') else []
                missing_in_future = [r for r in model_regressors if r not in df_future.columns]
                if missing_in_future:
                    logger.error(f"❌ Future dataframe missing regressors: {missing_in_future}")
                    raise ValueError(f"Future dataframe missing required regressors: {missing_in_future}")
                
                for feat in available_features:
                    logger.info(f"   {feat} in future: min={df_future[feat].min():.2f}, max={df_future[feat].max():.2f}, NaN={df_future[feat].isna().sum()}")
                
                # Ensure future dataframe is sorted by date
                df_future = df_future.sort_values("ds").reset_index(drop=True)
                
                # Final validation before prediction
                if df_future["ds"].isna().any():
                    logger.error(f"❌ Future data still has NaN in 'ds' column")
                    raise ValueError("Future data contains NaN in date column 'ds'")
                
                for feat in available_features:
                    if df_future[feat].isna().any():
                        logger.error(f"❌ Future data still has NaN in regressor '{feat}'")
                        # Try to fill with last known value from training
                        last_value = df_train[feat].iloc[-1]
                        df_future[feat] = df_future[feat].fillna(last_value)
                        logger.warning(f"   Filled NaN in '{feat}' with last training value: {last_value}")
                
                try:
                    forecast = model.predict(df_future)
                    logger.info(f"✅ Predictions generated successfully: {len(forecast)} rows")
                except Exception as predict_error:
                    logger.error(f"❌ Prophet model.predict() failed for store {store}: {predict_error}")
                    logger.error(f"   Future data shape: {df_future.shape}")
                    logger.error(f"   Future data sample:\n{df_future.head()}")
                    logger.error(f"   Future data dtypes:\n{df_future.dtypes}")
                    logger.error(f"   Model regressors: {model_regressors}")
                    logger.error(f"   Future columns: {df_future.columns.tolist()}")
                    raise  # Re-raise to be caught by outer exception handler
                
                # Create comparison dataframe
                compare = pd.DataFrame({
                    "date": test["Date"].values,
                    "actual": test["Weekly_Sales"].values,
                    "forecast": forecast["yhat"].values,
                    "forecast_lower": forecast["yhat_lower"].values,
                    "forecast_upper": forecast["yhat_upper"].values
                })
                
                # Calculate metrics
                mae = float(mean_absolute_error(compare["actual"], compare["forecast"]))
                rmse = float(np.sqrt(mean_squared_error(compare["actual"], compare["forecast"])))
                mape = float(np.mean(np.abs((compare["actual"] - compare["forecast"]) / compare["actual"])) * 100)
                
                # Convert to list of dictionaries for JSON response
                comparison_data = compare.to_dict(orient="records")
                
                # Format dates as strings
                for item in comparison_data:
                    if isinstance(item["date"], pd.Timestamp):
                        item["date"] = item["date"].strftime("%Y-%m-%d")
                
                results.append({
                    "store_id": int(store),
                    "comparison": comparison_data,
                    "metrics": {
                        "mae": mae,
                        "rmse": rmse,
                        "mape": mape
                    },
                    "weeks_backtested": weeks
                })
                
            except Exception as e:
                error_type = type(e).__name__
                error_msg = str(e)
                # CRITICAL: Log full error details so we can see what's failing
                logger.error("=" * 60)
                logger.error(f"❌ FAILED to backtest store {store}")
                logger.error(f"   Error Type: {error_type}")
                logger.error(f"   Error Message: {error_msg}")
                logger.error("=" * 60)
                import traceback
                full_traceback = traceback.format_exc()
                logger.error(f"Full traceback:\n{full_traceback}")
                logger.error("=" * 60)
                # Store error info for better error message
                continue
        
        if not results:
            # Provide detailed error message
            error_details = []
            if all_data.empty:
                error_details.append("Walmart_Sales.csv is empty or could not be loaded")
            else:
                first_store = sorted(all_data["Store"].unique())[0] if len(all_data["Store"].unique()) > 0 else None
                if first_store:
                    store_data_raw = all_data[all_data["Store"] == first_store]
                    # Check if aggregation would help
                    if "Dept" in store_data_raw.columns:
                        unique_dates = store_data_raw["Date"].nunique()
                        total_rows = len(store_data_raw)
                        error_details.append(f"First store ({first_store}) has {total_rows} rows across {unique_dates} unique dates (need at least {weeks + 20} dates)")
                        if total_rows > unique_dates:
                            error_details.append(f"⚠️ Multiple departments per date detected - aggregation should be applied")
                        
                        # Try to replicate aggregation to see what happens
                        try:
                            features = ["CPI", "Temperature", "IsHoliday", "Fuel_Price", "Unemployment"]
                            agg_dict = {"Weekly_Sales": "sum"}
                            for feat in features:
                                if feat in store_data_raw.columns:
                                    agg_dict[feat] = "mean"
                            
                            aggregated_test = store_data_raw.groupby("Date", as_index=False).agg(agg_dict)
                            error_details.append(f"After aggregation test: {len(aggregated_test)} unique dates")
                            
                            if len(aggregated_test) >= weeks + 20:
                                error_details.append(f"✅ Aggregation produces sufficient data ({len(aggregated_test)} >= {weeks + 20})")
                                error_details.append("❌ Error likely occurs during Prophet model fitting - check backend logs for detailed exception")
                            else:
                                error_details.append(f"❌ Even after aggregation: insufficient data ({len(aggregated_test)} < {weeks + 20})")
                        except Exception as agg_test_error:
                            error_details.append(f"⚠️ Error during aggregation test: {agg_test_error}")
                    else:
                        error_details.append(f"First store ({first_store}) has {len(store_data_raw)} rows (need at least {weeks + 20})")
                    
                    available_features = [f for f in features if f in store_data_raw.columns]
                    missing_features = [f for f in features if f not in store_data_raw.columns]
                    if missing_features:
                        error_details.append(f"Missing features: {missing_features}")
                    error_details.append(f"Available columns: {store_data_raw.columns.tolist()}")
                    error_details.append("🔍 Check backend terminal logs for the ACTUAL exception (look for '❌ FAILED to backtest store')")
                else:
                    error_details.append("No stores found in data")
            
            error_msg = "Failed to generate backtest for any stores. " + " | ".join(error_details)
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
        
        # Always return single store result for now (simpler for frontend)
        # If multiple stores evaluated, return first one
        result = results[0]
        
        logger.info(f"Backtest completed: Store {result['store_id']}, {len(result['comparison'])} data points")
        
        return result
        
    except Exception as e:
        logger.error(f"Error generating backtest comparison: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating backtest comparison: {str(e)}")

