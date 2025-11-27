# 📊 Model Accuracy Display - Implementation Guide

## Overview

This guide explains how model accuracy is calculated and displayed to users using your existing backtesting code.

---

## ✅ What Was Implemented

### 1. **Backend API Endpoints** (`backend/routes/model_accuracy.py`)

Three endpoints for model evaluation:

#### **`GET /api/v1/model-accuracy/forecast`**
- Uses **Prophet cross-validation** to calculate forecast accuracy
- Metrics returned:
  - **MAE** (Mean Absolute Error)
  - **RMSE** (Root Mean Squared Error)
  - **MAPE** (Mean Absolute Percentage Error)
  - **Coverage** (Prediction interval coverage)
- Supports evaluating individual stores or all stores (aggregate)

#### **`GET /api/v1/model-accuracy/anomaly`**
- Calculates anomaly detection performance metrics
- Returns:
  - Detection rates
  - Confidence scores
  - Sample statistics

#### **`GET /api/v1/model-accuracy/overall`**
- Combines forecast and anomaly metrics
- Calculates overall confidence score (0-100%)
- Provides comprehensive model performance view

---

### 2. **Frontend Dashboard Section**

Added a new **"Model Accuracy & Performance"** section to the Dashboard that displays:

#### **Overall Confidence Score**
- Large, prominent display (0-100%)
- Visual progress bar
- Breakdown by forecast vs. anomaly confidence

#### **Forecast Model Accuracy**
- **MAE**: Mean Absolute Error
- **RMSE**: Root Mean Squared Error  
- **MAPE**: Mean Absolute Percentage Error
- **Coverage**: Prediction interval coverage (if available)

#### **Anomaly Detection Performance**
- Detection rate (% of anomalies found)
- Normal detection rate
- Total samples evaluated
- Score standard deviation

---

## 🔧 How It Works

### **Prophet Cross-Validation**

The backend uses Prophet's built-in `cross_validation()` function:

```python
from prophet.diagnostics import cross_validation, performance_metrics

# Perform cross-validation
df_cv = cross_validation(
    model,
    horizon="6 weeks",      # Forecast 6 weeks ahead
    period="3 weeks",        # Re-evaluate every 3 weeks
    initial="18 weeks"       # Use 18 weeks of training data
)

# Calculate performance metrics
df_perf = performance_metrics(df_cv, rolling_window=1.0)
```

This simulates backtesting by:
1. Training on historical data up to a cutoff date
2. Making predictions for the next `horizon` period
3. Comparing predictions to actual values
4. Repeating at regular intervals (`period`)
5. Calculating aggregate metrics (MAE, RMSE, MAPE)

---

## 📍 Where It's Displayed

### **Dashboard Location**
The Model Accuracy section appears **before the Recommendations section** on the Dashboard.

### **Access**
1. Login to admin dashboard: `http://localhost:8080/login`
2. Navigate to Dashboard
3. Scroll down to see "Model Accuracy & Performance" card

---

## 🎯 Key Features

### **Real-Time Evaluation**
- Metrics are calculated on-demand when the Dashboard loads
- Cached for 5 minutes (accuracy doesn't change frequently)
- Can be refreshed by reloading the page

### **Store-Specific or Aggregate**
- Evaluate individual stores: `GET /api/v1/model-accuracy/forecast?store_id=1`
- Evaluate all stores (aggregate): `GET /api/v1/model-accuracy/forecast`

### **Comprehensive Metrics**
- **Forecast accuracy**: How well the model predicts future sales
- **Anomaly detection**: How well the model identifies outliers
- **Overall confidence**: Combined score showing model reliability

---

## 🔍 Understanding the Metrics

### **Forecast Metrics**

| Metric | Meaning | Good Value |
|--------|---------|------------|
| **MAE** | Average absolute difference between predicted and actual | Lower is better |
| **RMSE** | Square root of average squared errors (penalizes large errors) | Lower is better |
| **MAPE** | Average percentage error | Lower is better (< 10% is good) |
| **Coverage** | % of actual values within prediction intervals | Closer to 95% is better |

### **Anomaly Metrics**

| Metric | Meaning |
|--------|---------|
| **Detection Rate** | % of samples flagged as anomalies |
| **Normal Rate** | % of samples identified as normal |
| **Score Std Dev** | Spread of confidence scores (lower = more consistent) |

### **Overall Confidence**

- **0-50%**: Poor model performance
- **50-70%**: Moderate performance
- **70-85%**: Good performance
- **85-100%**: Excellent performance

---

## 🚀 Testing

### **1. Start Backend**
```cmd
cd backend
uvicorn main:app --reload
```

### **2. Test API Endpoint**
```bash
# Get overall accuracy
curl http://localhost:8000/api/v1/model-accuracy/overall

# Get forecast accuracy for store 1
curl http://localhost:8000/api/v1/model-accuracy/forecast?store_id=1

# Get anomaly accuracy
curl http://localhost:8000/api/v1/model-accuracy/anomaly
```

### **3. View in Dashboard**
1. Start frontend: `cd frontend && npm run dev`
2. Login: `http://localhost:8080/login`
3. Navigate to Dashboard
4. Scroll to "Model Accuracy & Performance" section

---

## 📝 Customization

### **Adjust Cross-Validation Parameters**

Edit `backend/routes/model_accuracy.py`:

```python
df_cv = cross_validation(
    temp_model,
    horizon="12 weeks",     # Forecast further ahead
    period="4 weeks",        # Evaluate less frequently
    initial="24 weeks"       # Use more training data
)
```

### **Change Cache Duration**

Edit `frontend/client/pages/Dashboard.tsx`:

```typescript
const accuracyQuery = useQuery({ 
  queryKey: ["model-accuracy"], 
  queryFn: () => fetchOverallAccuracy(), 
  staleTime: 600_000  // Cache for 10 minutes instead of 5
});
```

---

## 🐛 Troubleshooting

### **"Failed to load accuracy metrics"**

**Possible causes:**
1. Backend not running
2. Insufficient data for cross-validation
3. Model file not found

**Solutions:**
- Check backend logs for errors
- Ensure `backend/ml/forecast_model.pkl` exists
- Verify CSV data has enough historical data (need at least `initial` period)

### **Metrics Show 0 or NaN**

**Possible causes:**
1. Data format mismatch
2. Empty time series
3. Cross-validation failed

**Solutions:**
- Check `backend/data/Walmart_Sales.csv` exists and has data
- Verify date column is properly parsed
- Check backend logs for Prophet errors

---

## 📚 References

- **Prophet Cross-Validation**: https://facebook.github.io/prophet/docs/diagnostics.html
- **Prophet Performance Metrics**: https://facebook.github.io/prophet/docs/diagnostics.html#performance-metrics
- **MAE/RMSE/MAPE Explanation**: Standard time series forecasting metrics

---

## ✨ Summary

✅ **Backend**: 3 API endpoints for model evaluation  
✅ **Frontend**: Beautiful dashboard section with metrics  
✅ **Real-time**: Calculated on-demand using Prophet cross-validation  
✅ **Comprehensive**: Forecast + Anomaly + Overall confidence  

**Users can now see exactly how accurate your models are!** 🎯


