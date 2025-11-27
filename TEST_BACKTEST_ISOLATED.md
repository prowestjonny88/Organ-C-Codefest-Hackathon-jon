# 🧪 Isolated Backtest Test

## Purpose
Test the backtest feature independently without the API complexity to identify and fix issues.

## How to Run

```bash
cd backend
python test_backtest_isolated.py
```

## What It Tests

1. ✅ Data loading
2. ✅ Store selection
3. ✅ Date aggregation (multiple departments per date)
4. ✅ Data splitting (training vs test)
5. ✅ Data validation (NaN, infinite values, constant regressors)
6. ✅ Simple Prophet model (NO regressors) - **Primary test**
7. ✅ Prophet model with regressors (optional)

## Expected Output

### If Successful:
```
✅ SUCCESS! Simple model works!
📊 Metrics (Simple Model):
   MAE: [value]
   RMSE: [value]
   MAPE: [value]%
```

### If Failed:
```
❌ Simple model failed:
Error Type: [error type]
Error Message: [error message]
```

## What to Do Based on Results

### ✅ If Simple Model Works:
- The backtest feature CAN work
- Use simple model (no regressors) for hackathon demo
- Update `backend/routes/backtest.py` to use simple model by default

### ❌ If Simple Model Fails:
- Check the error message
- Likely issues:
  - Data quality problems
  - Prophet installation issues
  - Date format issues
- Share the error output for further debugging

## Next Steps After Test

1. **If test passes**: Update the API endpoint to match the working test
2. **If test fails**: Fix the issue in the test script first, then apply to API
3. **Once working**: Integrate back into the main API endpoint


