# 🚀 Step-by-Step Guide: Run Admin Interface

## Prerequisites Check

Make sure you have:
- ✅ Python installed (for backend)
- ✅ Node.js installed (for frontend)
- ✅ Both terminals/command prompts ready

---

## Step 1: Start Backend Server

### Option A: Using Command Prompt (Recommended - No PowerShell issues)

1. **Open Command Prompt** (not PowerShell):
   - Press `Win + R`
   - Type `cmd` and press Enter

2. **Navigate to backend folder:**
   ```cmd
   cd C:\Users\JON\OneDrive\Documents\CODEFEST\Organ-C-Codefest-Hackathon-jon\backend
   ```

3. **Install dependencies (if not done):**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Start the backend server:**
   ```cmd
   uvicorn main:app --reload
   ```

5. **Wait for this message:**
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000
   ```

✅ **Keep this window open!** Backend is now running.

---

## Step 2: Start Frontend Server

### Open a NEW Command Prompt window

1. **Open another Command Prompt** (new window):
   - Press `Win + R`
   - Type `cmd` and press Enter

2. **Navigate to frontend folder:**
   ```cmd
   cd C:\Users\JON\OneDrive\Documents\CODEFEST\Organ-C-Codefest-Hackathon-jon\frontend
   ```

3. **Install dependencies (first time only):**
   ```cmd
   npm install
   ```
   ⏳ This may take 2-5 minutes the first time.

4. **Start the frontend server:**
   ```cmd
   npm run dev
   ```

5. **Wait for this message:**
   ```
   Local:   http://localhost:5173/
   ```

✅ **Keep this window open too!** Frontend is now running.

---

## Step 3: Open Login Page

1. **Open your web browser** (Chrome, Edge, Firefox, etc.)

2. **Go to:**
   ```
   http://localhost:5173/login
   ```

3. **You should see the Admin Login page!**

---

## Step 4: Login

1. **Enter credentials:**
   - **Username:** `admin`
   - **Password:** `admin123`

2. **Click the "Login" button**

3. **You'll be redirected to the dashboard!** 🎉

---

## ✅ What You Should See

### Login Page (`/login`)
- Clean login form
- Username and password fields
- Login button
- Default credentials displayed at bottom

### After Login (`/dashboard`)
- Analytics dashboard
- Charts and metrics
- Navigation bar with:
  - Your username displayed
  - "Logout" button

---

## 🔍 Verify Everything Works

### Test Backend:
Open browser and go to: **http://localhost:8000/docs**
- Should show Swagger API documentation
- Try the `/api/v1/auth/login/json` endpoint

### Test Frontend:
1. Open browser DevTools (Press `F12`)
2. Go to **Network** tab
3. Login and check:
   - `POST /api/v1/auth/login/json` → Should return 200 with token
   - `GET /api/v1/auth/me` → Should return user info

---

## 🐛 Troubleshooting

### Backend won't start?

**Error: "uvicorn not found"**
```cmd
pip install uvicorn fastapi
```

**Error: "Module not found"**
```cmd
pip install -r requirements.txt
```

**Error: "Port 8000 already in use"**
- Close other programs using port 8000
- Or use a different port: `uvicorn main:app --reload --port 8001`

---

### Frontend won't start?

**Error: "npm not recognized"**
- Make sure Node.js is installed
- Restart Command Prompt after installing Node.js

**Error: "vite not found"**
```cmd
npm install
```

**Error: "Port 5173 already in use"**
- Close other programs using port 5173
- Vite will automatically use the next available port

**PowerShell execution policy error?**
- **Solution:** Use Command Prompt (cmd.exe) instead of PowerShell
- Or run: `powershell -ExecutionPolicy Bypass -Command "npm run dev"`

---

### Login fails?

1. **Check backend is running:**
   - Visit: http://localhost:8000/health
   - Should return: `{"status": "ok"}`

2. **Check browser console:**
   - Press `F12` → Go to **Console** tab
   - Look for red error messages

3. **Check Network tab:**
   - Press `F12` → Go to **Network** tab
   - Try logging in
   - Check if `/api/v1/auth/login/json` request fails

4. **Verify credentials:**
   - Username: `admin` (exact, case-sensitive)
   - Password: `admin123` (exact)

---

## 📋 Quick Checklist

Before starting:
- [ ] Python installed
- [ ] Node.js installed
- [ ] Two terminal windows ready (one for backend, one for frontend)

Starting:
- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] Can access http://localhost:5173/login

After login:
- [ ] Redirected to /dashboard
- [ ] Username shown in navigation
- [ ] Can logout successfully

---

## 🎯 Summary

**Two terminals needed:**
1. **Terminal 1 (Backend):** `cd backend` → `uvicorn main:app --reload`
2. **Terminal 2 (Frontend):** `cd frontend` → `npm install` → `npm run dev`

**Then:**
- Open browser → http://localhost:5173/login
- Login with: `admin` / `admin123`
- Enjoy your admin interface! 🎉

---

## 💡 Pro Tips

- **Use Command Prompt (cmd)** instead of PowerShell to avoid execution policy issues
- **Keep both terminals open** while testing
- **Check backend first** if frontend has issues (visit http://localhost:8000/health)
- **Clear browser cache** if you see old errors (Ctrl+Shift+Delete)

---

**That's it! You're ready to test the admin interface!** 🚀




