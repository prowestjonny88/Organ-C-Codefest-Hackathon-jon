# 🔧 Troubleshooting Backtest Comparison Graph

## Current Issue
The backtest comparison graph is not showing, with error:
```
Failed to generate backtest for any stores. First store (1) has 10226 rows (need at least 32)
```

## ✅ Step-by-Step Troubleshooting

### Step 1: Restart Backend Server
**IMPORTANT**: The backend must be restarted to pick up code changes.

1. Stop your current backend server (Ctrl+C in the terminal)
2. Restart it:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

### Step 2: Check Backend Logs
After restarting, try accessing the dashboard again and **immediately check your backend terminal logs**. Look for:

- `Processing store 1: X rows`
- `Store 1 has multiple departments per date. Aggregating by date...`
- `After aggregation: X unique dates`
- `Fitting Prophet model for store 1...`
- **Any ERROR messages** (these will tell us what's actually failing)

### Step 3: Common Issues & Solutions

#### Issue A: "Multiple departments per date"
**Symptom**: Error shows many rows but few unique dates
**Solution**: The aggregation code should handle this automatically. Check logs to confirm aggregation is happening.

#### Issue B: Prophet Model Fitting Fails
**Symptom**: Logs show "Fitting Prophet model..." but then an error
**Possible causes**:
- NaN values in feature columns
- Date format issues
- Insufficient data after aggregation

**Check**: Look for error messages like:
- `ValueError: Regressor 'X' missing from dataframe`
- `ValueError: Input contains NaN`
- `TypeError: ...`

#### Issue C: Data Not Aggregating
**Symptom**: Still seeing 10,226 rows instead of ~143 unique dates
**Solution**: The aggregation code should run automatically. If not, check:
- Is `Dept` column present in the data?
- Are there actually multiple rows per date?

### Step 4: Manual Data Check
Run this in your backend directory to verify data structure:

```python
from data_loader import get_all_data
import pandas as pd

df = get_all_data()
store1 = df[df["Store"] == 1].sort_values("Date")

print(f"Total rows: {len(store1)}")
print(f"Unique dates: {store1['Date'].nunique()}")
print(f"Rows per date (sample):")
print(store1.groupby("Date").size().head(10))

# Check for NaN
features = ["CPI", "Temperature", "IsHoliday", "Fuel_Price", "Unemployment"]
for feat in features:
    if feat in store1.columns:
        nan_count = store1[feat].isna().sum()
        print(f"{feat}: {nan_count} NaN values")
```

### Step 5: Test Backtest Endpoint Directly
Test the endpoint directly to see the full error:

```bash
# In browser or using curl
http://localhost:8000/api/v1/backtest/comparison?weeks=12
```

Or using Python:
```python
import requests
response = requests.get("http://localhost:8000/api/v1/backtest/comparison?weeks=12")
print(response.status_code)
print(response.json())
```

## 🔍 What to Share for Help

If the issue persists, please share:

1. **Backend terminal logs** (especially ERROR messages)
2. **Output from Step 4** (data check)
3. **Response from Step 5** (direct endpoint test)
4. **Any Prophet-related errors** from the logs

## 📝 Expected Behavior

After fixes, you should see in logs:
```
INFO: Processing store 1: 10226 rows
INFO: Store 1 has multiple departments per date. Aggregating by date...
INFO: After aggregation: 143 unique dates
INFO: Store 1 using features: ['CPI', 'Temperature', 'IsHoliday', 'Fuel_Price', 'Unemployment']
INFO: Fitting Prophet model for store 1 with 131 training rows...
INFO: Model fitted successfully for store 1
INFO: Making predictions for 12 test periods...
INFO: Backtest completed: Store 1, 12 data points
```

Then the graph should appear in the dashboard!


