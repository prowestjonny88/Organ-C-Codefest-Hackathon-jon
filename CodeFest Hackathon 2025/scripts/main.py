# Member 5 - Dashboard & Prescriptive Intelligence
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ------------------------------
# 1. Load predicted sales
# ------------------------------
predictions = pd.read_csv("next_3months_forecast.csv")  # output of Member 2
predictions['Date'] = pd.to_datetime(predictions['Date'])

# 2. Simulate current inventory (replace with actual inventory CSV)
num_stores = len(predictions['Store'].unique())
inventory = pd.DataFrame({
    'Store': predictions['Store'].unique(),
    'Current_Stock': np.random.uniform(5000, 50000, num_stores)  # generate random stock for ALL stores
})

# ------------------------------
# 3. Simulate Supplier Dimensions (lead time, reliability)
# ------------------------------
np.random.seed(42)
suppliers = pd.DataFrame({
    'Store': predictions['Store'].unique(),
    'Lead_Time': np.random.gamma(shape=2.0, scale=3.0, size=len(predictions['Store'].unique())),  # avg ~6 days
    'Lead_Time_SD': np.random.uniform(0.5, 2.0, size=len(predictions['Store'].unique())),
    'Reliability': np.random.beta(a=5, b=1.5, size=len(predictions['Store'].unique()))
})

# Merge predictions with inventory and supplier info
df = predictions.merge(inventory, on='Store', how='left')
df = df.merge(suppliers, on='Store', how='left')

# ------------------------------
# 4. Compute forecast volatility (σ_D) over rolling 4 weeks as example
# ------------------------------
df['Forecast_SD'] = df.groupby('Store')['Predicted_Weekly_Sales'].transform(lambda x: x.rolling(4, min_periods=1).std())
df['Forecast_SD'] = df['Forecast_SD'].fillna(df['Forecast_SD'].mean())

# ------------------------------
# 5. Compute Safety Stock (SS)
# SS = Zα * sqrt( (L_bar * σ_D^2) + (D_bar^2 * σ_L^2) )
# ------------------------------
Z_alpha = 1.65  # 95% service level
df['Avg_Forecast'] = df.groupby('Store')['Predicted_Weekly_Sales'].transform('mean')
df['Safety_Stock'] = Z_alpha * np.sqrt(
    (df['Lead_Time'] * df['Forecast_SD']**2) + 
    (df['Avg_Forecast']**2 * df['Lead_Time_SD']**2 / df['Reliability'])
)

# ------------------------------
# 6. Compute EOQ
# EOQ = sqrt( 2 * D * S / H )
# ------------------------------
ordering_cost = 50  # example $ per order
holding_cost_percent = 0.25  # 25% of unit cost per year
unit_cost = df['Predicted_Weekly_Sales'] * 0.5  # assume 50% of sales price
annual_demand = df['Predicted_Weekly_Sales'] * 52  # weekly -> annual

df['EOQ'] = np.sqrt(2 * annual_demand * ordering_cost / (holding_cost_percent * unit_cost))

# ------------------------------
# 7. Compute Stock Risk
# ------------------------------
df['Stock_Risk'] = df['Predicted_Weekly_Sales'] - df['Current_Stock']  # simple example
df['Risk_Flag'] = np.where(df['Stock_Risk'] > 0, 'Low Stock',
                           np.where(df['Stock_Risk'] < -df['Current_Stock']*0.5, 'Overstock', 'OK'))

# ------------------------------
# 8. Export Actionable CSV
# ------------------------------
output_cols = ['Store', 'Date', 'Predicted_Weekly_Sales', 'Current_Stock', 'Safety_Stock', 'EOQ', 'Stock_Risk', 'Risk_Flag']
df[output_cols].to_csv("sales_recommendations_full.csv", index=False)
print("Actionable recommendations exported to sales_recommendations_full.csv")

# ------------------------------
# 9. Generate per-store charts
# ------------------------------
output_folder = "store_charts"
os.makedirs(output_folder, exist_ok=True)

stores = df['Store'].unique()
for store in stores:
    store_data = df[df['Store'] == store]
    plt.figure(figsize=(10,5))
    plt.bar(store_data['Date'], store_data['Current_Stock'], label='Current Stock', alpha=0.6)
    plt.plot(store_data['Date'], store_data['Predicted_Weekly_Sales'], color='red', marker='o', label='Predicted Sales')
    plt.plot(store_data['Date'], store_data['Safety_Stock'], color='green', linestyle='--', label='Safety Stock')
    plt.title(f"Store {store} - Predicted Sales vs Stock & Safety Stock")
    plt.xlabel("Date")
    plt.ylabel("Units")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{output_folder}/store_{store}_forecast.png")
    plt.close()

print(f"Charts saved in folder '{output_folder}'")



