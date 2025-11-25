import pandas as pd
import numpy as np

# ========================
# Load Walmart CSV
# ========================
df = pd.read_csv("csv/Walmart_Sales.csv")
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
df = df.sort_values(['Store', 'Date']).reset_index(drop=True)

# ========================
# Check if Inventory already exists
# ========================
if 'Inventory' in df.columns:
    print("✅ Inventory column already exists. Converting to integers...")
    df['Inventory'] = df['Inventory'].astype(int)  # ← Convert to int
else:
    print("📝 Inventory column not found. Adding estimated inventory...")
    
    # Estimate baseline demand (4-week rolling average per store)
    df['Baseline_Demand'] = df.groupby('Store')['Weekly_Sales'].transform(
        lambda x: x.rolling(window=4, min_periods=1).mean()
    )
    
    # Assume each store keeps 2.5-3 weeks of buffer stock
    # Add 15% safety margin for unpredictable demand
    df['Inventory'] = df['Baseline_Demand'] * 2.8 * np.random.uniform(0.9, 1.1, len(df))
    
    # Ensure inventory is realistic (positive, reasonable bounds)
    df['Inventory'] = df['Inventory'].clip(lower=df['Weekly_Sales'] * 0.5)
    
    # ← CONVERT TO INTEGER (round to nearest whole number)
    df['Inventory'] = df['Inventory'].astype(int)
    
    # Remove temporary baseline column
    df = df.drop('Baseline_Demand', axis=1)
    
    print("✅ Inventory estimated based on historical sales patterns")

# ========================
# Save updated CSV
# ========================
df.to_csv("csv/Walmart_Sales_with_Inventory.csv", index=False)
print("✅ Updated CSV saved: csv/Walmart_Sales_with_Inventory.csv")

# Show sample
print("\n--- Sample Data ---")
print(df[['Store', 'Date', 'Weekly_Sales', 'Inventory']].head(10))