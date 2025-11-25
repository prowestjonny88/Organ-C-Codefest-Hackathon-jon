import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

sns.set_style("whitegrid")

# ========================
# 0. SETUP
# ========================
os.makedirs('outputs', exist_ok=True)
os.makedirs('outputs/charts', exist_ok=True)

# ========================
# 1. LOAD DATA
# ========================
recommendations = pd.read_csv("sales_recommendations_full.csv")
walmart = pd.read_csv("csv/Walmart_Sales_with_Inventory.csv")

recommendations['Date'] = pd.to_datetime(recommendations['Date'])
walmart['Date'] = pd.to_datetime(walmart['Date'])

print("="*70)
print("WALMART INVENTORY & SALES FORECAST REPORT")
print("="*70)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Forecast Date: {recommendations['Date'].iloc[0].date()}")
print(f"Total Stores: {len(recommendations)}")

# ========================
# 2. RISK ANALYSIS
# ========================
print("\n" + "="*70)
print("INVENTORY RISK SUMMARY")
print("="*70)

low_stock = recommendations[recommendations['Risk_Flag'] == 'Low Stock']
normal = recommendations[recommendations['Risk_Flag'] == 'Normal']
overstock = recommendations[recommendations['Risk_Flag'] == 'Overstock']

total_predicted_sales = recommendations['Predicted_Weekly_Sales'].sum()
total_current_stock = recommendations['Current_Stock'].sum()
stock_coverage = (total_current_stock / total_predicted_sales) * 100

print(f"\n📊 Overall Status:")
print(f"   • Total Predicted Sales (3 months out): ${total_predicted_sales:,.0f}")
print(f"   • Total Current Stock: {total_current_stock:,.0f} units")
print(f"   • Stock Coverage: {stock_coverage:.2f}%")

print(f"\n🔴 LOW STOCK ALERT: {len(low_stock)} stores")
print(f"   • Stores at risk: {', '.join(map(str, map(int, low_stock['Store'].values)))}")
print(f"   • Total stock shortage: ${low_stock['Stock_Risk'].sum():,.0f}")
print(f"   • Average shortage per store: ${low_stock['Stock_Risk'].mean():,.0f}")

print(f"\n✅ NORMAL: {len(normal)} stores")
print(f"   • Inventory is adequate")

print(f"\n📦 OVERSTOCK: {len(overstock)} stores")
if len(overstock) > 0:
    print(f"   • Stores with excess: {', '.join(map(str, map(int, overstock['Store'].values)))}")

# ========================
# 3. HISTORICAL CONTEXT
# ========================
print("\n" + "="*70)
print("HISTORICAL SALES & INVENTORY CONTEXT")
print("="*70)

ecent_sales = walmart.groupby('Store')['Weekly_Sales'].apply(lambda x: x.tail(4).mean())
avg_sales = walmart.groupby('Store')['Weekly_Sales'].mean()
avg_inventory = walmart.groupby('Store')['Inventory'].mean()

print(f"\n📈 Sales Metrics (All-time):")
print(f"   • Avg Weekly Sales per Store: ${avg_sales.mean():,.0f}")
print(f"   • Highest: Store {int(avg_sales.idxmax())} (${avg_sales.max():,.0f})")
print(f"   • Lowest: Store {int(avg_sales.idxmin())} (${avg_sales.min():,.0f})")

print(f"\n📦 Inventory Metrics (Historical Avg):")
print(f"   • Avg Inventory per Store: {avg_inventory.mean():,.0f} units")
print(f"   • Highest: Store {int(avg_inventory.idxmax())} ({avg_inventory.max():,.0f})")
print(f"   • Lowest: Store {int(avg_inventory.idxmin())} ({avg_inventory.min():,.0f})")

# ========================
# 4. COMPARISON: Predicted vs Historical
# ========================
print("\n" + "="*70)
print("FORECAST vs HISTORICAL COMPARISON")
print("="*70)

# Merge historical avg with forecasts
forecast_vs_history = recommendations.copy()
forecast_vs_history['Historical_Avg_Sales'] = forecast_vs_history['Store'].map(avg_sales)
forecast_vs_history['Sales_Change_%'] = (
    (forecast_vs_history['Predicted_Weekly_Sales'] - forecast_vs_history['Historical_Avg_Sales']) / 
    forecast_vs_history['Historical_Avg_Sales'] * 100
)

increase = len(forecast_vs_history[forecast_vs_history['Sales_Change_%'] > 10])
decrease = len(forecast_vs_history[forecast_vs_history['Sales_Change_%'] < -10])
stable = len(forecast_vs_history[(forecast_vs_history['Sales_Change_%'] >= -10) & (forecast_vs_history['Sales_Change_%'] <= 10)])

print(f"\n📊 Sales Trend Forecast:")
print(f"   • 📈 Increasing (>10%): {increase} stores")
print(f"   • 📉 Decreasing (<-10%): {decrease} stores")
print(f"   • ➡️  Stable (±10%): {stable} stores")

top_increases = forecast_vs_history.nlargest(5, 'Sales_Change_%')[['Store', 'Predicted_Weekly_Sales', 'Sales_Change_%']]
print(f"\n   Top Increases:")
for idx, row in top_increases.iterrows():
    print(f"      Store {int(row['Store'])}: {row['Sales_Change_%']:+.1f}% (${row['Predicted_Weekly_Sales']:,.0f})")

# ========================
# 5. ACTIONABLE RECOMMENDATIONS
# ========================
print("\n" + "="*70)
print("ACTIONABLE RECOMMENDATIONS")
print("="*70)

print(f"""
🔴 CRITICAL ACTIONS (Low Stock Stores):
   Priority 1 - URGENT RESTOCKING REQUIRED:
   • Stores: {', '.join(map(str, map(int, low_stock.nlargest(5, 'Stock_Risk')['Store'].values)))}
   • Shortage Value: ${low_stock['Stock_Risk'].sum():,.0f}
   • Action: Contact suppliers immediately for expedited delivery
   
📦 SECONDARY ACTIONS (If Applicable):
   Priority 2 - INVENTORY REBALANCING:
   • Implement cross-store transfers from low-demand to high-demand stores
   • Consider temporary price increases to manage demand
   
💡 STRATEGIC ACTIONS:
   Priority 3 - LONG-TERM IMPROVEMENTS:
   • Review ordering patterns - current stock is only {stock_coverage:.1f}% of 3-month forecast
   • Increase safety stock multiplier from 1x to 1.5x weekly sales
   • Implement weekly demand forecasting instead of monthly
   • Set up automated reorder triggers at 50% of average weekly sales
   
📊 IMPLEMENTATION TIMELINE:
   Week 1: Emergency restocking for {len(low_stock)} at-risk stores
   Week 2-3: Implement cross-store inventory transfers
   Week 4: Review and adjust forecasting models
""")

# ========================
# 6. FINANCIAL IMPACT
# ========================
print("\n" + "="*70)
print("FINANCIAL IMPACT ANALYSIS")
print("="*70)

# Assume 30% profit margin
profit_margin = 0.30
potential_lost_revenue = low_stock['Stock_Risk'].sum()
potential_lost_profit = potential_lost_revenue * profit_margin

# Assume 5% holding cost per unit per week
holding_cost = total_current_stock * 0.05

print(f"\n💰 Cost-Benefit Analysis:")
print(f"   • Potential Lost Profit (Stockouts): ${potential_lost_profit:,.0f}")
print(f"   • Weekly Holding Cost: ${holding_cost:,.0f}")
print(f"   • Cost of Emergency Restocking: ~${(potential_lost_revenue * 0.15):,.0f} (15% rush fee)")
print(f"   ───────────────────────────────────")
print(f"   • Net Impact of Inaction: ${(potential_lost_profit + holding_cost):,.0f}/week")

# ========================
# 7. STORE-BY-STORE BREAKDOWN
# ========================
print("\n" + "="*70)
print("STORE-BY-STORE DETAILED BREAKDOWN")
print("="*70)

for idx, row in recommendations.iterrows():
    store_num = int(row['Store'])
    status_icon = "🔴" if row['Risk_Flag'] == 'Low Stock' else "✅" if row['Risk_Flag'] == 'Normal' else "📦"
    
    print(f"\n{status_icon} Store {store_num}:")
    print(f"   Predicted Sales: ${row['Predicted_Weekly_Sales']:,.0f}")
    print(f"   Current Stock: {row['Current_Stock']:,.0f} units")
    print(f"   Stock Risk: ${row['Stock_Risk']:,.0f}")
    print(f"   Status: {row['Risk_Flag']}")
    
    # Show historical context
    store_hist_avg = avg_sales.get(store_num, 0)
    if store_hist_avg > 0:
        change = ((row['Predicted_Weekly_Sales'] - store_hist_avg) / store_hist_avg) * 100
        print(f"   Historical Avg: ${store_hist_avg:,.0f} ({change:+.1f}%)")

# ========================
# 8. CHARTS
# ========================
print("\n" + "="*70)
print("📊 GENERATING CHARTS...")
print("="*70)

# Chart 1: Risk Distribution
fig, ax = plt.subplots(figsize=(10, 6))
risk_counts = recommendations['Risk_Flag'].value_counts()
colors = ['#E74C3C' if 'Low' in x else '#2ECC71' if 'Normal' in x else '#F39C12' for x in risk_counts.index]
ax.barh(risk_counts.index, risk_counts.values, color=colors)
ax.set_xlabel('Number of Stores')
ax.set_title('Inventory Risk Distribution (3-Month Forecast)', fontsize=14, fontweight='bold')
for i, v in enumerate(risk_counts.values):
    ax.text(v + 0.5, i, str(v), va='center', fontweight='bold')
plt.tight_layout()
plt.savefig('outputs/charts/01_risk_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Chart 1: Risk Distribution")

# Chart 2: Stock Coverage
fig, ax = plt.subplots(figsize=(12, 6))
coverage_data = recommendations.sort_values('Store')
colors_coverage = ['#E74C3C' if x == 'Low Stock' else '#2ECC71' if x == 'Normal' else '#F39C12' 
                   for x in coverage_data['Risk_Flag']]
ax.bar(coverage_data['Store'], coverage_data['Current_Stock'], label='Current Stock', alpha=0.7, color='blue')
ax.plot(coverage_data['Store'], coverage_data['Predicted_Weekly_Sales'], 
        color='red', marker='o', linewidth=2, label='Predicted Sales', markersize=4)
ax.set_xlabel('Store')
ax.set_ylabel('Units')
ax.set_title('Current Stock vs Predicted Sales by Store', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(alpha=0.3, axis='y')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('outputs/charts/02_stock_vs_sales.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Chart 2: Stock vs Sales")

# Chart 3: Stock Risk by Store
fig, ax = plt.subplots(figsize=(14, 6))
risk_by_store = recommendations.sort_values('Stock_Risk', ascending=False).head(15)
colors_risk = ['#E74C3C' if x > 0 else '#2ECC71' for x in risk_by_store['Stock_Risk']]
ax.barh(risk_by_store['Store'].astype(str), risk_by_store['Stock_Risk'], color=colors_risk)
ax.set_xlabel('Stock Risk ($)')
ax.set_title('Top 15 Stores with Highest Stock Risk', fontsize=14, fontweight='bold')
ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
plt.tight_layout()
plt.savefig('outputs/charts/03_top_risk_stores.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Chart 3: Top Risk Stores")

# Chart 4: Financial Impact
fig, ax = plt.subplots(figsize=(10, 6))
impact_data = [potential_lost_profit, holding_cost]
labels = [f'Lost Profit\n${potential_lost_profit:,.0f}', f'Holding Cost\n${holding_cost:,.0f}']
colors_impact = ['#E74C3C', '#F39C12']
ax.pie(impact_data, labels=labels, colors=colors_impact, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 11})
ax.set_title('Weekly Financial Impact of Current Inventory', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('outputs/charts/04_financial_impact.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Chart 4: Financial Impact")

print("\n✅ All charts saved to outputs/charts/")

# ========================
# 9. EXPORT DETAILED REPORT
# ========================
detailed_report = forecast_vs_history[['Store', 'Predicted_Weekly_Sales', 'Current_Stock', 
                                       'Historical_Avg_Sales', 'Sales_Change_%', 'Stock_Risk', 'Risk_Flag']]
detailed_report = detailed_report.sort_values('Stock_Risk', ascending=False)
detailed_report.to_csv('outputs/detailed_forecast_report.csv', index=False)
print("✅ Detailed report exported: outputs/detailed_forecast_report.csv")

# ========================
# 10. SUMMARY REPORT
# ========================
summary_stats = pd.DataFrame({
    'Metric': [
        'Total Stores',
        'Low Stock (Risk)',
        'Normal',
        'Overstock',
        'Total Predicted Sales',
        'Total Current Stock',
        'Stock Coverage %',
        'Potential Lost Profit',
        'Weekly Holding Cost',
        'Total Weekly Impact'
    ],
    'Value': [
        len(recommendations),
        len(low_stock),
        len(normal),
        len(overstock),
        f'${total_predicted_sales:,.0f}',
        f'{total_current_stock:,.0f}',
        f'{stock_coverage:.2f}%',
        f'${potential_lost_profit:,.0f}',
        f'${holding_cost:,.0f}',
        f'${(potential_lost_profit + holding_cost):,.0f}'
    ]
})

summary_stats.to_csv('outputs/summary_stats.csv', index=False)
print("✅ Summary statistics exported: outputs/summary_stats.csv")

print("\n" + "="*70)
print("✅ REPORT GENERATION COMPLETE!")
print("="*70)
print("\n📁 All outputs saved to outputs/:")
print("   • Charts: outputs/charts/ (4 visualizations)")
print("   • Reports: outputs/*.csv (detailed + summary)")
print("\n" + "="*70)