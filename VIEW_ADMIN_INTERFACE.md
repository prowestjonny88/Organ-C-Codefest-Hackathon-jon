# 🎯 How to View the Admin Interface

## Quick Steps

### 1️⃣ Start Backend (Terminal 1)

```powershell
cd backend
uvicorn main:app --reload
```

Wait for: `INFO:     Uvicorn running on http://127.0.0.1:8000`

---

### 2️⃣ Start Frontend (Terminal 2 - NEW WINDOW)

```powershell
cd frontend
npm run dev
```

Wait for: `Local: http://localhost:5173/`

---

### 3️⃣ Open Browser

Go to: **http://localhost:5173/login**

---

### 4️⃣ Login

**Credentials:**
- Username: `admin`
- Password: `admin123`

Click **Login** → You'll be redirected to `/dashboard`

---

## ✅ What You'll See

### Login Page
- Clean login form
- Username/password fields
- Default credentials shown

### After Login
- **Dashboard** with analytics
- **Navigation bar** showing your username
- **Logout button** in navigation

---

## 🔍 Verify It Works

1. **Backend API Docs**: http://localhost:8000/docs
2. **Health Check**: http://localhost:8000/health
3. **Try logging out** and accessing `/dashboard` directly (should redirect to login)

---

## 🐛 Troubleshooting

### Backend won't start?
```powershell
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend won't start?
```powershell
cd frontend
npm install
npm run dev
```

### Login fails?
- Check backend is running: http://localhost:8000/health
- Check browser console (F12) for errors
- Verify credentials: `admin` / `admin123`

---

## 📝 Notes

- Keep **both terminals open** (backend + frontend)
- Backend runs on port **8000**
- Frontend runs on port **5173**
- Token expires after 24 hours (just login again)

---

**That's it! You should now see the admin interface! 🎉**




