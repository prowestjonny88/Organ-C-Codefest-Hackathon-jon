# 📊 Real-Time Graph Updates - How It Works

## ✅ **YES - Graphs Update Simultaneously When IoT Data Arrives!**

The dashboard now updates **automatically** when new IoT data is received via WebSocket.

---

## 🔄 How Real-Time Updates Work

### 1. **Data Flow**

```
IoT Simulator → Backend API → WebSocket → Frontend Dashboard → Graphs Update
```

1. **IoT Simulator** sends data to `POST /api/v1/iot/`
2. **Backend** processes data (ML models, risk calculation)
3. **Backend** broadcasts via WebSocket to all connected clients
4. **Frontend** receives WebSocket message
5. **Frontend** updates state and invalidates React Query
6. **Graphs** automatically re-render with new data

---

### 2. **What Updates in Real-Time**

#### ✅ **KPI Cards** (Top 5 metrics)
- **Updates:** Immediately via state (`setKpiMetrics`)
- **Data Source:** Calculated from accumulated IoT data points
- **Metrics:**
  - Avg Weekly Sales
  - Max Sales
  - Min Sales
  - Volatility
  - Holiday Sales Avg

#### ✅ **Forecast Graph**
- **Updates:** Via React Query refetch (every 10 seconds OR when WebSocket message arrives)
- **Data Source:** Backend API (`/api/v1/forecast`)
- **Trigger:** WebSocket invalidates query → Forces immediate refetch

#### ✅ **Anomaly Detection Graph**
- **Updates:** Via React Query refetch
- **Data Source:** Backend API (`/api/v1/anomaly`)
- **Trigger:** WebSocket invalidates query → Forces immediate refetch

#### ✅ **Risk Analysis Table**
- **Updates:** Via React Query refetch
- **Data Source:** Backend API (`/api/v1/risk`)
- **Trigger:** WebSocket invalidates query → Forces immediate refetch

#### ✅ **Real-Time Alerts Section**
- **Updates:** Immediately via state (`setRealtimeAlerts`)
- **Data Source:** WebSocket `alert` messages
- **Shows:** High-risk alerts as they occur

---

### 3. **Technical Implementation**

#### **WebSocket Connection**
```typescript
// Connects when user chooses backend data (not CSV upload)
useEffect(() => {
  if (dataLoaded) return; // Skip if CSV uploaded
  
  const ws = new WebSocket(WS_ALERTS_URL);
  
  ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    
    if (message.type === "iot_update") {
      // 1. Update IoT data points state
      setIotDataPoints(prev => [...prev, message].slice(-100));
      
      // 2. Calculate and update KPI metrics
      setKpiMetrics(calculatedMetrics);
      
      // 3. Invalidate all queries (triggers refetch)
      queryClient.invalidateQueries({ queryKey: ["kpi"] });
      queryClient.invalidateQueries({ queryKey: ["forecast"] });
      queryClient.invalidateQueries({ queryKey: ["anomalies"] });
      queryClient.invalidateQueries({ queryKey: ["risk"] });
      
      // 4. Force immediate refetch (bypasses staleTime)
      queryClient.refetchQueries({ queryKey: ["kpi"] });
      queryClient.refetchQueries({ queryKey: ["forecast"] });
      // ... etc
    }
  };
}, [dataLoaded]);
```

#### **React Query Configuration**
```typescript
// Reduced staleTime for real-time mode
const staleTimeForRealtime = dataLoaded ? 60_000 : 5_000; // 5s for backend, 60s for CSV

// Auto-refetch every 10 seconds when using backend data
const forecastQuery = useQuery({ 
  queryKey: ["forecast", ...],
  queryFn: fetchForecast,
  staleTime: staleTimeForRealtime,
  refetchInterval: dataLoaded ? false : 10_000 // Auto-refetch every 10s
});
```

---

### 4. **Visual Indicators**

#### **Real-Time Status Banner**
- **Green dot + "Connected"**: WebSocket is active
- **Red dot + "Connecting..."**: WebSocket disconnected (auto-reconnects)
- **Data point count**: Shows how many IoT updates received
- **Message**: "Graphs update automatically as new data arrives"

---

### 5. **Update Frequency**

| Component | Update Method | Frequency |
|-----------|--------------|-----------|
| **KPI Cards** | State update | **Immediate** (on WebSocket message) |
| **Forecast Graph** | Query refetch | **Immediate** (on WebSocket) + **Every 10s** (auto) |
| **Anomaly Graph** | Query refetch | **Immediate** (on WebSocket) + **Every 10s** (auto) |
| **Risk Table** | Query refetch | **Immediate** (on WebSocket) + **Every 10s** (auto) |
| **Alerts** | State update | **Immediate** (on WebSocket message) |

---

### 6. **Testing Real-Time Updates**

#### **Step 1: Start Backend**
```cmd
cd backend
uvicorn main:app --reload
```

#### **Step 2: Start Frontend**
```cmd
cd frontend
npm run dev
```

#### **Step 3: Login & Access Dashboard**
1. Go to `http://localhost:8080/login`
2. Login with `admin` / `admin123`
3. **Skip CSV upload** (click "Skip" or close upload panel)
4. Dashboard should show "Real-Time Mode: Connected"

#### **Step 4: Start IoT Simulator**
```cmd
python iot_simulator.py --local --interval 5
```

#### **Step 5: Watch Dashboard**
- **KPI Cards**: Should update immediately as data arrives
- **Forecast Graph**: Should refresh every 10 seconds OR when new data arrives
- **Anomaly Graph**: Should refresh every 10 seconds OR when new data arrives
- **Status Banner**: Should show increasing data point count

---

### 7. **Troubleshooting**

#### **Graphs Not Updating?**

1. **Check WebSocket Connection**
   - Look for green status indicator at top of dashboard
   - Check browser console for WebSocket errors

2. **Check Backend Logs**
   - Should see: `📡 Broadcasted IoT update to X clients`
   - If 0 clients, frontend isn't connected

3. **Check Browser Console**
   - Look for: `✅ WebSocket connected for real-time IoT data`
   - Look for: `Error parsing WebSocket message` (if any)

4. **Verify IoT Simulator**
   - Check if it's sending data: `python iot_simulator.py --local --interval 5`
   - Check backend logs for `POST /api/v1/iot/` requests

5. **Force Refresh**
   - Hard refresh: `Ctrl + Shift + R`
   - Check Network tab → WebSocket connection

---

### 8. **Performance Optimizations**

- **Data Point Limit**: Only keeps last 100 IoT data points (prevents memory issues)
- **Alert Limit**: Only keeps last 20 alerts
- **StaleTime**: 5 seconds for real-time mode (vs 60s for CSV mode)
- **Auto-Refetch**: Every 10 seconds (fallback if WebSocket fails)
- **Query Invalidation**: Forces immediate refetch when WebSocket message arrives

---

## 🎯 Summary

**YES, graphs update simultaneously when IoT data is fetched!**

- ✅ **KPI Cards**: Update immediately via state
- ✅ **Forecast Graph**: Updates immediately + every 10s
- ✅ **Anomaly Graph**: Updates immediately + every 10s
- ✅ **Risk Table**: Updates immediately + every 10s
- ✅ **Alerts**: Update immediately via state

**All updates happen automatically - no manual refresh needed!** 🚀


