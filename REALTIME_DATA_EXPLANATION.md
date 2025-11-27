# 📊 Real-Time Data Fetching Explanation

## Current Implementation

### ✅ What's Currently Working

**Location:** `frontend/client/pages/Dashboard.tsx` (lines 79-86)

The dashboard uses **React Query** (`useQuery`) to fetch data:

```typescript
const kpiQuery = useQuery({ 
  queryKey: ["kpi"], 
  queryFn: () => fetchKPIMetrics(), 
  staleTime: 60_000  // 60 seconds (NOT 10 minutes!)
});
```

**How it works:**
1. ✅ Fetches data when Dashboard component **first loads**
2. ✅ Caches data for **60 seconds** (`staleTime: 60_000`)
3. ❌ **Does NOT automatically refetch every 10 minutes**
4. ❌ Only refetches when:
   - Component remounts
   - Window regains focus
   - Query is manually invalidated

---

## 🔍 Data Fetching Flow

### 1. Initial Load
```
Dashboard loads → React Query fetches → Data displayed
```

### 2. Current Update Behavior
```
Data cached for 60 seconds → Only refetches on window focus/remount
```

### 3. WebSocket (Available but NOT Connected)
```
Backend: ✅ WebSocket ready at /ws/alerts
Frontend: ❌ Dashboard does NOT connect to WebSocket
```

---

## ❌ What's NOT Currently Working

### 1. **No Automatic Updates**
- Figures do **NOT** update every 10 minutes
- They only update when you:
  - Refresh the page
  - Switch tabs and come back
  - Manually trigger a refetch

### 2. **WebSocket Not Connected**
- Backend has WebSocket support (`routes/websocket.py`)
- Backend broadcasts when IoT data arrives (`routes/iot.py`)
- **Frontend Dashboard does NOT listen to WebSocket**

---

## 🎯 How to Add Real-Time Updates

### Option 1: Add Automatic Polling (Every 10 Minutes)

**Modify `Dashboard.tsx`:**

```typescript
const kpiQuery = useQuery({ 
  queryKey: ["kpi"], 
  queryFn: () => fetchKPIMetrics(), 
  staleTime: 60_000,
  refetchInterval: 10 * 60 * 1000,  // Refetch every 10 minutes
  refetchIntervalInBackground: true  // Continue even when tab is inactive
});
```

### Option 2: Connect to WebSocket (True Real-Time)

**Add WebSocket connection in `Dashboard.tsx`:**

```typescript
useEffect(() => {
  const ws = new WebSocket(WS_ALERTS_URL);
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'iot_update') {
      // Update dashboard with new data
      queryClient.invalidateQueries(['kpi']);
      queryClient.invalidateQueries(['alerts']);
    }
  };
  
  return () => ws.close();
}, []);
```

### Option 3: Hybrid Approach
- Use WebSocket for **instant alerts** (when IoT data arrives)
- Use polling for **regular metrics** (every 10 minutes)

---

## 📍 Key Files

### Frontend Data Fetching
- **`frontend/client/pages/Dashboard.tsx`** (lines 79-86)
  - Uses React Query `useQuery`
  - `staleTime: 60_000` = 60 seconds cache
  - No `refetchInterval` = No automatic updates

### Backend WebSocket
- **`backend/routes/websocket.py`** - WebSocket endpoints
- **`backend/routes/iot.py`** (lines 147-180) - Broadcasts on IoT data
- **`backend/websocket_manager.py`** - Manages connections

### API Functions
- **`frontend/client/lib/api.ts`**
  - `fetchKPIMetrics()` - Fetches KPI data
  - `fetchForecast()` - Fetches forecast
  - `WS_ALERTS_URL` - WebSocket URL (defined but not used)

---

## 🔧 Current Behavior Summary

| Feature | Status | Details |
|---------|--------|---------|
| **Initial Data Load** | ✅ Works | Fetches on Dashboard mount |
| **Auto-Update (10 min)** | ❌ **NOT Working** | No `refetchInterval` configured |
| **WebSocket Connection** | ❌ **NOT Connected** | Backend ready, frontend not listening |
| **Cache Duration** | ✅ 60 seconds | Data cached for 1 minute |
| **Manual Refresh** | ✅ Works | Refreshes on window focus |

---

## 💡 Recommendation

**To get automatic updates every 10 minutes:**

1. Add `refetchInterval: 10 * 60 * 1000` to all `useQuery` calls
2. OR connect to WebSocket for true real-time updates
3. OR use both (WebSocket for alerts, polling for metrics)

**Would you like me to implement automatic updates?**




