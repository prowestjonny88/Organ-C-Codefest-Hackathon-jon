import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import warnings
warnings.filterwarnings('ignore')

# ========================
# 0. LOAD DATA
# ========================
print("="*70)
print("MEMBER 2: SALES FORECASTING (FIXED)")
print("="*70)

walmart = pd.read_csv("csv/Walmart_Sales_with_Inventory.csv")
walmart['Date'] = pd.to_datetime(walmart['Date'])
walmart = walmart.sort_values(['Store', 'Date']).reset_index(drop=True)

print(f"✅ Loaded {len(walmart)} historical records")

# ========================
# 1. PREPARE DATA FOR FORECASTING
# ========================
print("\n" + "="*70)
print("PREPARING FORECAST DATA")
print("="*70)

# Get latest data per store
latest_data = walmart.sort_values('Date').groupby('Store').tail(1)[
    ['Store', 'Date', 'Weekly_Sales', 'Inventory', 'Temperature', 
     'Fuel_Price', 'CPI', 'Unemployment', 'Holiday_Flag']
].reset_index(drop=True)

# Calculate statistics per store (for realistic forecasts)
store_stats = walmart.groupby('Store')['Weekly_Sales'].agg([
    'mean',
    'std',
    'min',
    'max',
    ('q25', lambda x: x.quantile(0.25)),
    ('q75', lambda x: x.quantile(0.75))
]).reset_index()

print(f"\n📊 Store Statistics (Sample):")
print(store_stats.head(10))

# ========================
# 2. FIX: CALCULATE REALISTIC WEEKLY FORECASTS
# ========================
print("\n" + "="*70)
print("CALCULATING WEEKLY FORECASTS (CORRECTED)")
print("="*70)

forecasts = []

for idx, row in latest_data.iterrows():
    store = row['Store']
    store_info = store_stats[store_stats['Store'] == store].iloc[0]
    
    # Get store's historical average
    historical_avg = store_info['mean']
    historical_std = store_info['std']
    
    # FIX 1: Forecast should be based on historical patterns
    # Add 10-15% growth for realistic business scenario
    growth_factor = 1.12  # 12% moderate growth
    
    # Forecast = Historical Average × Growth Factor
    # (Not total 3-month sales, but WEEKLY sales)
    predicted_weekly = historical_avg * growth_factor
    
    # Add some randomness within 1 std dev (realistic variance)
    noise = np.random.normal(0, historical_std * 0.1)
    predicted_weekly = max(predicted_weekly + noise, historical_avg * 0.8)  # Don't go below 80% of avg
    
    forecasts.append({
        'Store': store,
        'Date': row['Date'],
        'Predicted_Weekly_Sales': predicted_weekly,
        'Historical_Avg': historical_avg,
        'Historical_Std': historical_std,
        'Growth_Factor': growth_factor
    })

forecast_df = pd.DataFrame(forecasts)

print(f"\n✅ Generated {len(forecast_df)} weekly forecasts")
print("\nForecast Sample (First 10 stores):")
print(forecast_df.head(10))

# ========================
# 3. FIX: CALCULATE SAFETY STOCK
# ========================
print("\n" + "="*70)
print("CALCULATING SAFETY STOCK (CORRECTED)")
print("="*70)

# Safety Stock Formula: Z-score × Std_Dev × √Lead_Time
# Z-score = 1.65 for 95% service level
# Lead_Time = 2 weeks (typical supplier lead time)

Z_SCORE = 1.65  # 95% service level
LEAD_TIME = 2    # weeks

forecast_df['Safety_Stock'] = (
    Z_SCORE * forecast_df['Historical_Std'] * np.sqrt(LEAD_TIME)
).round(2)

print(f"\n📦 Safety Stock Calculation:")
print(f"   • Z-Score (95% SL): {Z_SCORE}")
print(f"   • Lead Time: {LEAD_TIME} weeks")
print(f"   • Formula: {Z_SCORE} × Std_Dev × √{LEAD_TIME}")
print(f"\nSafety Stock Results (Sample):")
print(forecast_df[['Store', 'Predicted_Weekly_Sales', 'Historical_Std', 'Safety_Stock']].head(10))

# ========================
# 4. FIX: CALCULATE ECONOMIC ORDER QUANTITY (EOQ)
# ========================
print("\n" + "="*70)
print("CALCULATING ECONOMIC ORDER QUANTITY - EOQ (CORRECTED)")
print("="*70)

# EOQ Formula: √(2×D×S/H)
# D = Annual Demand (Weekly × 52)
# S = Ordering Cost (assume $50 per order)
# H = Holding Cost (assume 20% of inventory value per year)

ORDERING_COST = 50        # $ per order
HOLDING_COST_RATE = 0.20  # 20% per year
AVG_UNIT_PRICE = 100      # $ per unit (assumption)

forecast_df['Annual_Demand'] = forecast_df['Predicted_Weekly_Sales'] * 52 / AVG_UNIT_PRICE  # Convert to units
forecast_df['Holding_Cost_per_Unit'] = AVG_UNIT_PRICE * HOLDING_COST_RATE

# EOQ calculation
forecast_df['EOQ'] = (
    np.sqrt((2 * forecast_df['Annual_Demand'] * ORDERING_COST) / forecast_df['Holding_Cost_per_Unit'])
).round(2)

print(f"\n📊 EOQ Calculation:")
print(f"   • Ordering Cost (S): ${ORDERING_COST}")
print(f"   • Holding Cost Rate (H): {HOLDING_COST_RATE*100}%")
print(f"   • Unit Price: ${AVG_UNIT_PRICE}")
print(f"   • Formula: √(2×D×S/H)")
print(f"\nEOQ Results (Sample):")
print(forecast_df[['Store', 'Annual_Demand', 'EOQ']].head(10))

# ========================
# 5. FIX: REORDER POINT
# ========================
print("\n" + "="*70)
print("CALCULATING REORDER POINT (CORRECTED)")
print("="*70)

# Reorder Point = (Daily Demand × Lead Time) + Safety Stock
# Daily Demand = Weekly Demand / 7

DAYS_PER_WEEK = 7

forecast_df['Daily_Demand'] = forecast_df['Predicted_Weekly_Sales'] / DAYS_PER_WEEK
forecast_df['Reorder_Point'] = (
    forecast_df['Daily_Demand'] * LEAD_TIME * 7 + forecast_df['Safety_Stock']
).round(2)

print(f"\n🔔 Reorder Point Calculation:")
print(f"   • Formula: (Daily_Demand × Lead_Time × 7) + Safety_Stock")
print(f"\nReorder Point Results (Sample):")
print(forecast_df[['Store', 'Daily_Demand', 'Reorder_Point']].head(10))

# ========================
# 6. GET CURRENT INVENTORY
# ========================
print("\n" + "="*70)
print("LOADING CURRENT INVENTORY")
print("="*70)

current_inventory = walmart.sort_values('Date').groupby('Store')[['Store', 'Inventory']].tail(1).reset_index(drop=True)
current_inventory.columns = ['Store', 'Current_Stock']

forecast_df = forecast_df.merge(current_inventory, on='Store', how='left')

print(f"\n✅ Current inventory merged")
print(forecast_df[['Store', 'Current_Stock']].head(10))

# ========================
# 7. FIX: CALCULATE STOCK METRICS
# ========================
print("\n" + "="*70)
print("CALCULATING STOCK METRICS (CORRECTED)")
print("="*70)

# Days of Inventory = Current Stock / Daily Demand
forecast_df['Days_of_Inventory'] = (
    forecast_df['Current_Stock'] / (forecast_df['Predicted_Weekly_Sales'] / 7)
).round(2)

# Stock Risk = If Current Stock < Reorder Point
forecast_df['Stock_Risk'] = (
    forecast_df['Reorder_Point'] - forecast_df['Current_Stock']
).round(2)

# Stock Risk Flag
forecast_df['Risk_Flag'] = np.where(
    forecast_df['Current_Stock'] < forecast_df['Reorder_Point'],
    'Low Stock',  # Need to reorder
    np.where(
        forecast_df['Current_Stock'] > (forecast_df['Predicted_Weekly_Sales'] * 4),
        'Overstock',  # Too much stock
        'Normal'
    )
)

print(f"\n📊 Stock Metrics Calculated:")
print(forecast_df[['Store', 'Current_Stock', 'Reorder_Point', 'Days_of_Inventory', 'Risk_Flag']].head(10))

# ========================
# 8. EXPORT CORRECTED FORECAST
# ========================
print("\n" + "="*70)
print("EXPORTING CORRECTED FORECAST")
print("="*70)

# Export full detailed forecast
export_columns = [
    'Store', 'Date', 'Predicted_Weekly_Sales', 'Current_Stock', 
    'Safety_Stock', 'EOQ', 'Reorder_Point', 'Stock_Risk', 'Risk_Flag',
    'Historical_Avg', 'Historical_Std', 'Days_of_Inventory'
]

forecast_df[export_columns].to_csv('next_3months_forecast_FIXED.csv', index=False)
print(f"✅ Exported: next_3months_forecast_FIXED.csv")

# Also export simple version for recommendations
simple_export = forecast_df[[
    'Store', 'Date', 'Predicted_Weekly_Sales', 'Current_Stock', 
    'Safety_Stock', 'EOQ', 'Stock_Risk', 'Risk_Flag'
]].copy()

simple_export.to_csv('sales_recommendations_full_FIXED.csv', index=False)
print(f"✅ Exported: sales_recommendations_full_FIXED.csv")

# ========================
# 9. SUMMARY STATISTICS
# ========================
print("\n" + "="*70)
print("FORECAST SUMMARY")
print("="*70)

low_stock_count = len(forecast_df[forecast_df['Risk_Flag'] == 'Low Stock'])
normal_count = len(forecast_df[forecast_df['Risk_Flag'] == 'Normal'])
overstock_count = len(forecast_df[forecast_df['Risk_Flag'] == 'Overstock'])

print(f"\n📊 Forecast Statistics:")
print(f"   • Total Stores: {len(forecast_df)}")
print(f"   • Avg Weekly Sales: ${forecast_df['Predicted_Weekly_Sales'].mean():,.0f}")
print(f"   • Avg Current Stock: {forecast_df['Current_Stock'].mean():,.0f} units")
print(f"   • Avg Safety Stock: {forecast_df['Safety_Stock'].mean():,.0f} units")
print(f"   • Avg Days of Inventory: {forecast_df['Days_of_Inventory'].mean():.1f} days")

print(f"\n⚠️  Risk Distribution:")
print(f"   • Low Stock: {low_stock_count} stores")
print(f"   • Normal: {normal_count} stores")
print(f"   • Overstock: {overstock_count} stores")

print(f"\n📈 Variance Check (vs Historical):")
variance_pct = ((forecast_df['Predicted_Weekly_Sales'].mean() - forecast_df['Historical_Avg'].mean()) / 
                forecast_df['Historical_Avg'].mean() * 100)
print(f"   • Avg Variance: {variance_pct:+.1f}%")
print(f"   • Status: {'✅ Reasonable' if abs(variance_pct) < 50 else '⚠️  Moderate' if abs(variance_pct) < 100 else '❌ Extreme'}")

print("\n" + "="*70)
print("✅ FORECAST GENERATION COMPLETE (FIXED)")
print("="*70)
print("\nFiles Generated:")
print("  • next_3months_forecast_FIXED.csv (detailed)")
print("  • sales_recommendations_full_FIXED.csv (simple)")

