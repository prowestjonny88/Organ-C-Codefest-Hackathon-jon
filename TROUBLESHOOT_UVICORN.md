# 🔧 Troubleshooting: Uvicorn "Could not import module 'main'" Error

## ❌ Error Message
```
ERROR:    Error loading ASGI app. Could not import module "main".
INFO:     Will watch for changes in these directories: ['C:\\Users\\JON\\OneDrive\\Documents\\CODEFEST\\Organ-C-Codefest-Hackathon-jon']
```

## 🔍 Root Cause Analysis

### Problem
Uvicorn is being run from the **root directory** (`Organ-C-Codefest-Hackathon-jon`), but `main.py` is located in the **`backend`** subdirectory.

When you run `uvicorn main:app`, Python looks for `main.py` in the **current working directory**. Since you're in the root directory, it can't find `backend/main.py`.

### Why This Happens
1. **Current Directory**: You're running uvicorn from the root project folder
2. **Module Location**: `main.py` is in `backend/main.py`
3. **Import Path**: All imports in `main.py` are relative (e.g., `from routes.iot import router`), which means Python needs to be run from the `backend` directory so it can find the `routes` subdirectory

### Evidence
The error log shows:
```
Will watch for changes in these directories: ['C:\\Users\\JON\\OneDrive\\Documents\\CODEFEST\\Organ-C-Codefest-Hackathon-jon']
```
This confirms uvicorn is watching the **root directory**, not `backend`.

---

## ✅ Solution

### Option 1: Run from Backend Directory (Recommended)

**Step 1:** Navigate to the backend directory:
```cmd
cd backend
```

**Step 2:** Run uvicorn:
```cmd
uvicorn main:app --reload
```

**Expected Output:**
```
INFO:     Will watch for changes in these directories: ['C:\\Users\\JON\\OneDrive\\Documents\\CODEFEST\\Organ-C-Codefest-Hackathon-jon\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

✅ Notice the directory path now includes `\backend` at the end!

---

### Option 2: One-Line Command (From Root)

If you're in the root directory, you can run:
```cmd
cd backend && uvicorn main:app --reload
```

---

### Option 3: Use Python Module Syntax (Alternative)

From the root directory, you can also try:
```cmd
python -m uvicorn backend.main:app --reload
```

However, this might have import issues because the relative imports in `main.py` expect to be run from the `backend` directory.

---

## 🧪 Verification Steps

### 1. Check Current Directory
```cmd
cd
```
Should show: `C:\Users\JON\OneDrive\Documents\CODEFEST\Organ-C-Codefest-Hackathon-jon\backend`

### 2. Verify main.py Exists
```cmd
dir main.py
```
Should show: `main.py` file exists

### 3. Test Import
```cmd
python -c "import main; print('✅ Import successful')"
```
Should print: `✅ Import successful`

### 4. Start Server
```cmd
uvicorn main:app --reload
```
Should start without errors.

---

## 🐛 Common Mistakes

### ❌ Wrong: Running from Root
```cmd
C:\Users\JON\OneDrive\Documents\CODEFEST\Organ-C-Codefest-Hackathon-jon> uvicorn main:app --reload
```
**Error:** `Could not import module "main"`

### ✅ Correct: Running from Backend
```cmd
C:\Users\JON\OneDrive\Documents\CODEFEST\Organ-C-Codefest-Hackathon-jon\backend> uvicorn main:app --reload
```
**Success:** Server starts correctly

---

## 📝 Quick Reference

| Location | Command | Result |
|----------|---------|--------|
| Root directory | `uvicorn main:app --reload` | ❌ Error |
| Backend directory | `uvicorn main:app --reload` | ✅ Works |
| Root directory | `cd backend && uvicorn main:app --reload` | ✅ Works |
| Root directory | `python -m uvicorn backend.main:app --reload` | ⚠️ May have import issues |

---

## 🚀 Pro Tip: Create a Startup Script

To avoid this issue in the future, you can create a batch file:

**Create `start-backend.bat` in the root directory:**
```batch
@echo off
cd backend
uvicorn main:app --reload
```

Then just run:
```cmd
start-backend.bat
```

---

## ✅ Success Indicators

When uvicorn starts correctly, you should see:
1. ✅ Directory path includes `\backend`
2. ✅ `INFO:     Uvicorn running on http://127.0.0.1:8000`
3. ✅ `INFO:     Application startup complete.`
4. ✅ No import errors
5. ✅ API docs accessible at `http://localhost:8000/docs`

---

**That's it! The fix is simple: just make sure you're in the `backend` directory when running uvicorn.** 🎉


