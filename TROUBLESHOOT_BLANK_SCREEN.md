# 🔧 Troubleshooting: Blank Screen on Dashboard

## ✅ **FIXED: Missing `accuracyQuery` Definition**

The issue was that `accuracyQuery` was being used in the JSX but was never defined, causing a runtime error.

### **What Was Fixed:**

1. ✅ Added missing `accuracyQuery` definition
2. ✅ Improved error handling for accuracy metrics
3. ✅ Added fallback UI when metrics are unavailable

---

## 🧪 **How to Test**

### **Step 1: Check Browser Console**

1. Open Dashboard: `http://localhost:8080/dashboard`
2. Press **F12** to open Developer Tools
3. Go to **Console** tab
4. Look for any red error messages

**Common errors:**
- `ReferenceError: accuracyQuery is not defined` ← This was the issue (now fixed)
- `TypeError: Cannot read property 'data' of undefined`
- Network errors (CORS, 404, etc.)

---

### **Step 2: Check Network Tab**

1. Press **F12** → **Network** tab
2. Refresh the page
3. Look for failed requests (red status codes)

**Check these endpoints:**
- `GET /api/v1/model-accuracy/overall` - Should return 200 or show error
- `GET /api/v1/kpi` - Should work
- `GET /api/v1/forecast` - Should work

---

### **Step 3: Verify Backend is Running**

```cmd
# Check if backend is running
curl http://localhost:8000/health
```

Should return: `{"status": "ok"}`

---

### **Step 4: Check Frontend Terminal**

Look for:
- ✅ `VITE v7.x.x ready` - Frontend is running
- ❌ `Error: Cannot find module` - Missing dependencies
- ❌ `Failed to compile` - Syntax errors

---

## 🐛 **Common Issues & Fixes**

### **Issue 1: Blank Screen with No Errors**

**Possible causes:**
- Component crashed silently
- Missing error boundary
- Infinite render loop

**Fix:**
1. Check browser console for errors
2. Check React DevTools (if installed)
3. Try hard refresh: `Ctrl + Shift + R`

---

### **Issue 2: "accuracyQuery is not defined" Error**

**Status:** ✅ **FIXED** - Query is now defined

**If you still see this:**
1. Make sure you've pulled the latest changes
2. Restart frontend: Stop and run `npm run dev` again
3. Clear browser cache: `Ctrl + Shift + Delete`

---

### **Issue 3: "Failed to load accuracy metrics"**

**This is normal if:**
- Backend model evaluation endpoint is slow
- Backend doesn't have enough data for cross-validation
- Backend is not running

**Fix:**
- The dashboard will still work, just without accuracy metrics
- Check backend logs for errors
- Ensure `backend/ml/forecast_model.pkl` exists

---

### **Issue 4: CORS Errors**

**Error:** `Access to fetch at 'http://localhost:8000/...' from origin 'http://localhost:8080' has been blocked by CORS policy`

**Fix:**
- Check `backend/main.py` has CORS middleware enabled
- Verify backend is running on port 8000
- Check frontend is using correct API URL

---

### **Issue 5: 404 Errors for API Endpoints**

**Error:** `GET http://localhost:8000/api/v1/model-accuracy/overall 404`

**Fix:**
1. Check `backend/main.py` includes the model_accuracy router:
   ```python
   from routes.model_accuracy import router as model_accuracy_router
   app.include_router(model_accuracy_router, prefix=f"{API_V1_PREFIX}/model-accuracy", ...)
   ```
2. Restart backend
3. Check backend logs for route registration

---

## 🔍 **Debugging Steps**

### **1. Check Component Renders**

Add console.log to see if component is rendering:

```typescript
export default function Dashboard() {
  console.log("Dashboard component rendering...");
  // ... rest of code
}
```

---

### **2. Check Queries**

Add console.log to see query status:

```typescript
console.log("accuracyQuery:", {
  isLoading: accuracyQuery.isLoading,
  error: accuracyQuery.error,
  data: accuracyQuery.data
});
```

---

### **3. Check API Function**

Test API function directly in browser console:

```javascript
// In browser console
fetch('http://localhost:8000/api/v1/model-accuracy/overall')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);
```

---

## ✅ **Verification Checklist**

Run through this checklist:

- [ ] Backend is running: `http://localhost:8000/health` returns OK
- [ ] Frontend is running: `http://localhost:8080` loads
- [ ] No console errors (F12 → Console)
- [ ] No network errors (F12 → Network)
- [ ] `accuracyQuery` is defined (check Dashboard.tsx line ~227)
- [ ] Browser cache cleared (`Ctrl + Shift + R`)
- [ ] Dependencies installed: `npm install` in frontend folder

---

## 🚀 **Quick Fix Attempts**

### **Fix 1: Restart Everything**

```cmd
# Stop all terminals
# Then restart:

# Terminal 1: Backend
cd backend
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

---

### **Fix 2: Clear Cache & Rebuild**

```cmd
cd frontend
rm -rf node_modules  # or del /s node_modules on Windows
npm install
npm run dev
```

---

### **Fix 3: Check for TypeScript Errors**

```cmd
cd frontend
npx tsc --noEmit
```

---

## 📞 **If Still Not Working**

**Provide:**
1. **Browser console errors** (F12 → Console, copy all red errors)
2. **Network tab errors** (F12 → Network, look for failed requests)
3. **Backend terminal output** (any errors?)
4. **Frontend terminal output** (any errors?)
5. **What you see** (completely blank? loading spinner? error message?)

---

## 🎯 **Summary**

✅ **Fixed:** Missing `accuracyQuery` definition  
✅ **Added:** Better error handling  
✅ **Improved:** Fallback UI when metrics unavailable  

**The dashboard should now load properly!** If you still see a blank screen, check the browser console for specific errors.

