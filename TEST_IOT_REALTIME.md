# 🧪 Testing Real-Time IoT Data Feature

## Step-by-Step Testing Guide

### Prerequisites
- ✅ Backend server running
- ✅ Frontend server running
- ✅ IoT simulator ready
- ✅ Browser open

---

## Step 1: Start Backend Server

**Open Terminal 1 (Command Prompt):**

```cmd
cd C:\Users\JON\OneDrive\Documents\CODEFEST\Organ-C-Codefest-Hackathon-jon\backend
uvicorn main:app --reload
```

**Wait for:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

✅ **Keep this terminal open!**

---

## Step 2: Start Frontend Server

**Open Terminal 2 (NEW Command Prompt window):**

```cmd
cd C:\Users\JON\OneDrive\Documents\CODEFEST\Organ-C-Codefest-Hackathon-jon\frontend
npm run dev
```

**Wait for:**
```
Local:   http://localhost:5173/
```

✅ **Keep this terminal open!**

---

## Step 3: Start IoT Simulator

**Open Terminal 3 (NEW Command Prompt window):**

```cmd
cd C:\Users\JON\OneDrive\Documents\CODEFEST\Organ-C-Codefest-Hackathon-jon
python iot_simulator.py --local --interval 3
```

**You should see:**
```
🚀 IoT Simulator running...
📍 Target: LOCAL (http://localhost:8000)
⏱️  Interval: 3 seconds
📡 Sending data to: http://localhost:8000/api/v1/iot
...
✅ Response: 200 OK
```

✅ **Keep this terminal open!** It will send data every 3 seconds.

---

## Step 4: Access Dashboard

1. **Open your browser** (Chrome, Edge, Firefox)

2. **Go to login page:**
   ```
   http://localhost:5173/login
   ```

3. **Login with admin credentials:**
   - Username: `admin`
   - Password: `admin123`

4. **You'll be redirected to `/dashboard`**

---

## Step 5: Choose Backend Data (Skip CSV Upload)

**When you see the CSV upload panel:**

1. **Click "Skip" or close the upload panel**
   - This tells the dashboard to use backend data
   - WebSocket will automatically connect

2. **You should immediately see:**
   - ✅ Green dot with "Real-time IoT data connected"
   - 📊 KPI Overview section
   - 📈 Charts and metrics

---

## Step 6: Verify Real-Time Updates

### ✅ Check Connection Status

**Look at the top of KPI Overview section:**
- Should show: **Green dot** + "Real-time IoT data connected"
- If gray dot: Wait a few seconds, it should connect

### ✅ Watch KPI Metrics Update

**In the KPI Overview cards, watch for:**
- **Avg Weekly Sales** - Should change as new data arrives
- **Max Sales** - Should increase if higher values come in
- **Min Sales** - Should decrease if lower values come in
- **Volatility** - Should recalculate based on data variance

**Expected:** Numbers update every 3 seconds (matching IoT simulator interval)

### ✅ Check Real-Time Alerts Section

**Scroll down to "Real-Time Alerts" section:**

1. **If HIGH risk detected:**
   - Red alert box appears
   - Shows: Store, Dept, Risk Score, Timestamp
   - Updates automatically

2. **Latest IoT Data Points:**
   - Blue box showing last 4 data points
   - Displays: Store, Sales, Risk Level
   - Updates as new data arrives

### ✅ Check Browser Console (Optional)

**Press F12 → Go to Console tab:**

**You should see:**
```
✅ WebSocket connected for real-time IoT data
```

**When data arrives:**
- No errors
- Messages about data updates (if logging enabled)

---

## Step 7: Verify Data Flow

### Check Backend Terminal (Terminal 1)

**You should see:**
```
INFO:     POST /api/v1/iot HTTP/1.1 200 OK
INFO:     📡 Broadcasted IoT update to 1 clients
```

**Every 3 seconds:**
- New POST request to `/api/v1/iot`
- WebSocket broadcast message
- Client count shows connected clients

### Check IoT Simulator Terminal (Terminal 3)

**You should see:**
```
📤 Sending IoT data...
✅ Response: 200 OK
   Anomaly: 1, Score: 0.05, Cluster: 3, Risk: LOW (0)
```

**Every 3 seconds:**
- New data sent
- Response received
- Analysis results shown

---

## ✅ Success Indicators

### Dashboard Shows:
- ✅ Green connection dot
- ✅ KPI metrics updating every 3 seconds
- ✅ Latest IoT data points updating
- ✅ Alerts appearing when HIGH risk detected
- ✅ Numbers changing in real-time

### Backend Shows:
- ✅ POST requests every 3 seconds
- ✅ WebSocket broadcasts
- ✅ "Broadcasted IoT update to X clients"

### IoT Simulator Shows:
- ✅ Sending data every 3 seconds
- ✅ 200 OK responses
- ✅ Analysis results

---

## 🐛 Troubleshooting

### WebSocket Not Connecting?

**Check:**
1. Backend is running on port 8000
2. Frontend is running on port 5173
3. Browser console shows connection errors
4. Try refreshing the dashboard page

**Fix:**
- Check backend terminal for errors
- Verify `WS_ALERTS_URL` in browser console
- Check CORS settings in backend

### No Data Updates?

**Check:**
1. IoT simulator is running
2. Simulator shows "200 OK" responses
3. Backend shows POST requests
4. WebSocket shows broadcasts

**Fix:**
- Restart IoT simulator
- Check API endpoint: `http://localhost:8000/api/v1/iot`
- Verify authentication (if enabled)

### KPI Metrics Not Updating?

**Check:**
1. WebSocket is connected (green dot)
2. IoT data is arriving (check latest data points)
3. Browser console for errors

**Fix:**
- Wait for more data points (needs at least 1)
- Check if `setKpiMetrics` is being called
- Verify data format matches expected structure

### Alerts Not Showing?

**Check:**
1. IoT simulator is sending HIGH risk data
2. Backend is detecting HIGH risk
3. WebSocket is broadcasting alerts

**Fix:**
- Use `--mode anomaly` in IoT simulator to force anomalies
- Check backend logs for alert broadcasts
- Verify alert message format

---

## 🎯 Quick Test Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] IoT simulator sending data every 3 seconds
- [ ] Logged in as admin
- [ ] Skipped CSV upload (chose backend data)
- [ ] Green dot shows "connected"
- [ ] KPI metrics updating
- [ ] Latest IoT data points showing
- [ ] Alerts appearing (if HIGH risk)
- [ ] No errors in browser console

---

## 🚀 Advanced Testing

### Test with Anomaly Mode

**Start IoT simulator with anomaly mode:**
```cmd
python iot_simulator.py --local --interval 3 --mode anomaly
```

**Expected:**
- More HIGH risk alerts
- Anomaly flags in data
- Higher risk scores

### Test with Different Intervals

**Fast updates (1 second):**
```cmd
python iot_simulator.py --local --interval 1
```

**Slow updates (10 seconds):**
```cmd
python iot_simulator.py --local --interval 10
```

### Test Multiple Data Points

**Send 10 records then stop:**
```cmd
python iot_simulator.py --local --interval 2 --count 10
```

**Expected:**
- 10 data points received
- KPI metrics calculated from all 10
- Dashboard shows accumulated data

---

## 📊 Expected Behavior

### Normal Operation:
- ✅ Data arrives every 3 seconds
- ✅ Dashboard updates automatically
- ✅ No page refresh needed
- ✅ Smooth updates without flickering

### When HIGH Risk Detected:
- ✅ Red alert appears immediately
- ✅ Alert shows in Real-Time Alerts section
- ✅ Risk score displayed
- ✅ Timestamp shown

### Connection Issues:
- ✅ Auto-reconnects after 3 seconds
- ✅ Shows "Connecting..." status
- ✅ Resumes updates when reconnected

---

## 🎉 Success!

**If you see:**
- ✅ Green dot connected
- ✅ Metrics updating every 3 seconds
- ✅ Latest data points showing
- ✅ Alerts appearing when needed

**Then the real-time IoT feature is working perfectly!** 🚀

---

## 💡 Tips

1. **Keep all 3 terminals visible** to monitor all components
2. **Use browser DevTools** (F12) to see WebSocket messages
3. **Check backend logs** to verify data processing
4. **Watch the numbers** - they should change smoothly
5. **Test with different intervals** to see update frequency

---

**Happy Testing!** 🧪✨




