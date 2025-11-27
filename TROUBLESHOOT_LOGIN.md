# 🔧 Troubleshooting: Can't View Login Page

## Step-by-Step Diagnosis

### Step 1: Check Frontend is Running

**Open Command Prompt and check:**

```cmd
cd frontend
npm run dev
```

**Expected output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**If you see errors:**
- Run `npm install` first
- Check if port 5173 is already in use
- Try a different port: `npm run dev -- --port 5174`

---

### Step 2: Verify Correct URL

**❌ WRONG (Backend):**
```
http://localhost:8000/login  ← This won't work!
```

**✅ CORRECT (Frontend):**
```
http://localhost:5173/login  ← Use this!
```

**Make sure you're using:**
- Port **5173** (frontend), NOT port 8000 (backend)
- URL starts with `http://localhost:5173`

---

### Step 3: Check Browser Console

**Press F12 → Go to Console tab**

**Look for errors:**
- Red error messages?
- Failed imports?
- Network errors?

**Common errors:**
- `Failed to fetch` → Backend not running
- `Cannot find module` → Missing dependencies
- `404 Not Found` → Wrong URL/port

---

### Step 4: Check Network Tab

**Press F12 → Go to Network tab**

**Refresh the page and check:**
- Is `index.html` loading? (should be 200 OK)
- Are JavaScript files loading? (App.tsx, etc.)
- Any 404 errors?

---

### Step 5: Clear Browser Cache

**Try these:**

1. **Hard Refresh:**
   - Windows: `Ctrl + Shift + R` or `Ctrl + F5`
   - Mac: `Cmd + Shift + R`

2. **Clear Cache:**
   - Press `Ctrl + Shift + Delete`
   - Clear cached images and files
   - Refresh page

3. **Try Incognito/Private Mode:**
   - Open new incognito window
   - Go to `http://localhost:5173/login`

---

### Step 6: Check Terminal Output

**Look at the frontend terminal for:**

**Errors:**
```
✘ [ERROR] ...
✘ Failed to compile
```

**Warnings:**
```
⚠ Missing dependencies
⚠ Port already in use
```

**If you see errors:**
- Copy the error message
- Check if dependencies are installed: `npm install`
- Check if TypeScript errors exist

---

### Step 7: Verify Files Exist

**Check these files exist:**

```cmd
cd frontend\client\pages
dir Login.tsx
```

**Should show:**
```
Login.tsx
```

**If missing:**
- File was deleted or moved
- Need to recreate it

---

### Step 8: Test Basic Routes

**Try these URLs in order:**

1. **Home page:**
   ```
   http://localhost:5173/
   ```
   Should show the landing page

2. **Login page:**
   ```
   http://localhost:5173/login
   ```
   Should show login form

3. **Dashboard (should redirect to login):**
   ```
   http://localhost:5173/dashboard
   ```
   Should redirect to `/login` if not authenticated

---

### Step 9: Check Backend is Running

**Even though login is frontend, backend is needed for authentication:**

```cmd
cd backend
uvicorn main:app --reload
```

**Check:**
- Is it running on port 8000?
- Can you access `http://localhost:8000/docs`?
- Any errors in backend terminal?

---

### Step 10: Check for Port Conflicts

**Is port 5173 already in use?**

**Windows:**
```cmd
netstat -ano | findstr :5173
```

**If something is using it:**
- Kill the process
- Or use different port: `npm run dev -- --port 5174`

---

## 🐛 Common Issues & Fixes

### Issue 1: "Cannot GET /login"

**Problem:** Accessing backend instead of frontend

**Fix:** Use `http://localhost:5173/login` (port 5173, not 8000)

---

### Issue 2: Blank Page / White Screen

**Problem:** JavaScript error or build failure

**Fix:**
1. Check browser console (F12)
2. Check frontend terminal for errors
3. Try: `npm install` then `npm run dev`

---

### Issue 3: "Module not found" Error

**Problem:** Missing dependencies

**Fix:**
```cmd
cd frontend
npm install
npm run dev
```

---

### Issue 4: Page Loads but Login Form Missing

**Problem:** CSS not loading or component error

**Fix:**
1. Check browser console for errors
2. Check Network tab - are CSS files loading?
3. Hard refresh: `Ctrl + Shift + R`

---

### Issue 5: Redirect Loop

**Problem:** Auth context causing redirect

**Fix:**
1. Clear localStorage: `localStorage.clear()` in console
2. Refresh page
3. Check AuthContext for errors

---

### Issue 6: Port Already in Use

**Problem:** Another process using port 5173

**Fix:**
```cmd
# Find process
netstat -ano | findstr :5173

# Kill process (replace PID with actual number)
taskkill /PID <PID> /F

# Or use different port
npm run dev -- --port 5174
```

---

## ✅ Quick Checklist

Run through this checklist:

- [ ] Frontend running: `npm run dev` in `frontend` folder
- [ ] Using correct URL: `http://localhost:5173/login`
- [ ] No errors in browser console (F12)
- [ ] No errors in frontend terminal
- [ ] Backend running on port 8000 (for auth)
- [ ] Browser cache cleared (Ctrl + Shift + R)
- [ ] Files exist: `frontend/client/pages/Login.tsx`
- [ ] Dependencies installed: `npm install` in frontend

---

## 🔍 Detailed Diagnosis Commands

### Check Frontend Status:
```cmd
cd frontend
npm run dev
```

### Check if Port is Free:
```cmd
netstat -ano | findstr :5173
```

### Check Backend Status:
```cmd
cd backend
uvicorn main:app --reload
```

### Test Backend API:
```
http://localhost:8000/health
```
Should return: `{"status": "ok"}`

### Test Frontend:
```
http://localhost:5173/
```
Should show landing page

---

## 📞 What to Check Next

**If still not working, provide:**

1. **Browser console errors** (F12 → Console)
2. **Frontend terminal output** (any errors?)
3. **URL you're using** (exact URL)
4. **What you see** (blank page? error? redirect?)

---

## 🚀 Quick Fix Attempts

### Fix 1: Restart Everything
```cmd
# Stop all terminals
# Then restart in order:

# Terminal 1: Backend
cd backend
uvicorn main:app --reload

# Terminal 2: Frontend  
cd frontend
npm run dev
```

### Fix 2: Reinstall Dependencies
```cmd
cd frontend
rm -rf node_modules  # or del /s node_modules on Windows
npm install
npm run dev
```

### Fix 3: Clear Everything
```cmd
# Clear browser cache
# Clear localStorage: localStorage.clear() in console
# Restart frontend
```

---

**Try these steps and let me know what you find!** 🔍




