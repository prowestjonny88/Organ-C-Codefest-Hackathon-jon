# 📊 Backtest Comparison - Predicted vs Actual Walmart Data

## Overview

The **Model Accuracy & Performance** section now shows a comparison graph between:
- **Predicted Sales** (purple dashed line) - from our trained model
- **Actual Sales** (green solid line) - from Walmart historical data

This serves as a **testimonial** to demonstrate model accuracy to customers.

---

## ✅ What's Implemented

### **Backend Endpoint**
- `GET /api/v1/backtest/comparison` - Generates 12-week backtest comparison
- Uses Walmart sales data (`backend/data/Walmart_Sales.csv`)
- Trains Prophet model on historical data
- Forecasts last 12 weeks
- Compares predictions to actual Walmart sales

### **Frontend Visualization**
- Integrated into "Model Accuracy & Performance" section
- Interactive graph showing:
  - **Green line** = Actual Walmart sales
  - **Purple line** = Predicted sales (our model)
  - **Light blue area** = Forecast confidence intervals
- Metrics displayed: MAE, RMSE, MAPE

---

## 🔧 How It Works

### **Backtest Process** (Same as Colab Notebook)

1. **Load Walmart Data**: Reads `Walmart_Sales.csv`
2. **Split Data**: 
   - Training: All data except last 12 weeks
   - Testing: Last 12 weeks (actual Walmart sales)
3. **Train Model**: Fits Prophet model with features:
   - CPI, Temperature, IsHoliday, Fuel_Price, Unemployment
4. **Forecast**: Predicts last 12 weeks
5. **Compare**: Actual vs Predicted values
6. **Calculate Metrics**: MAE, RMSE, MAPE

---

## 📍 Where to See It

1. **Start Backend**: `cd backend && uvicorn main:app --reload`
2. **Start Frontend**: `cd frontend && npm run dev`
3. **Login**: `http://localhost:8080/login`
4. **Go to Dashboard**
5. **Scroll to "Model Accuracy & Performance" section**
6. **See "Predicted vs Actual Sales Comparison" graph**

---

## 🎯 Graph Details

### **Visual Elements**
- **Green Solid Line** = Actual Walmart Sales (real historical data)
- **Purple Dashed Line** = Predicted Sales (our model's forecast)
- **Light Blue Shaded Area** = Forecast confidence intervals (95% prediction interval)

### **What It Shows**
- **Close Match** = Model is accurate (predicted ≈ actual)
- **Large Gap** = Model needs improvement
- **Trends** = How well model captures sales patterns

---

## 🔍 Understanding the Metrics

| Metric | Meaning | Good Value |
|--------|---------|------------|
| **MAE** | Average absolute difference | Lower is better |
| **RMSE** | Penalizes large errors more | Lower is better |
| **MAPE** | Percentage error | < 10% is good |

---

## 🐛 Troubleshooting

### **Graph Shows "Comparison graph will be displayed here once backtest data is available"**

**Possible causes:**
1. Backend not running
2. Walmart_Sales.csv not found
3. Backtest endpoint taking too long (model fitting is slow)
4. Insufficient data for 12-week backtest

**Solutions:**
1. Check backend logs for errors
2. Verify `backend/data/Walmart_Sales.csv` exists
3. Wait 30-60 seconds for model to fit (first time is slow)
4. Check browser console (F12) for API errors

### **All Metrics Show 0.0%**

**Possible causes:**
1. Backtest endpoint failed
2. Model accuracy endpoint failed
3. Data not loading properly

**Solutions:**
1. Check backend terminal for errors
2. Test endpoint directly: `curl http://localhost:8000/api/v1/backtest/comparison`
3. Check if Walmart_Sales.csv has data

---

## 🚀 Performance Notes

- **First Request**: May take 30-60 seconds (model fitting)
- **Subsequent Requests**: Cached for 5 minutes
- **Store Selection**: Currently uses first store for speed
- **To See Other Stores**: Use `?store_id=X` parameter

---

## 📝 Example API Call

```bash
# Get backtest comparison for store 1
curl http://localhost:8000/api/v1/backtest/comparison?store_id=1&weeks=12

# Response includes:
# {
#   "store_id": 1,
#   "comparison": [
#     {"date": "2012-10-05", "actual": 1643690.9, "forecast": 1654321.2, ...},
#     ...
#   ],
#   "metrics": {"mae": 12345.67, "rmse": 23456.78, "mape": 5.23},
#   "weeks_backtested": 12
# }
```

---

## ✨ Summary

✅ **Backend**: Generates backtest comparison using Walmart data  
✅ **Frontend**: Shows comparison graph in Model Accuracy section  
✅ **Purpose**: Testimonial showing model accuracy  
✅ **Data**: Uses actual Walmart sales data for validation  

**The comparison graph demonstrates how well your model predicts actual Walmart sales!** 🎯


