# 🚀 Quick Start: View Admin Interface

## Step-by-Step Guide

### Step 1: Start the Backend Server

Open a terminal and run:

```bash
cd backend
uvicorn main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

✅ Backend is now running at `http://localhost:8000`

---

### Step 2: Start the Frontend Server

Open a **NEW terminal** (keep backend running) and run:

```bash
cd frontend
npm install  # Only needed first time
npm run dev
```

**Expected output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

✅ Frontend is now running at `http://localhost:5173`

---

### Step 3: Access the Login Page

Open your browser and go to:

```
http://localhost:5173/login
```

You should see the **Admin Login** page with:
- Username field
- Password field
- Login button
- Default credentials displayed

---

### Step 4: Login

Enter the default credentials:

- **Username:** `admin`
- **Password:** `admin123`

Click the **Login** button.

✅ You should be redirected to `/dashboard`

---

### Step 5: View the Dashboard

After successful login, you'll see:
- **Navigation bar** with your username and "Logout" button
- **Dashboard** with analytics and data
- **Protected content** that requires authentication

---

## 🔍 Verify It's Working

### Check Backend API
Visit: `http://localhost:8000/docs`

You should see:
- Swagger UI with all endpoints
- `/api/v1/auth/login/json` endpoint listed
- Try the login endpoint in Swagger UI

### Check Frontend
1. Open browser DevTools (F12)
2. Go to **Network** tab
3. Login and check for:
   - `POST /api/v1/auth/login/json` - Should return 200 with token
   - `GET /api/v1/auth/me` - Should return user info

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Make sure you're in the backend directory
cd backend

# Install dependencies if needed
pip install -r requirements.txt

# Try starting again
uvicorn main:app --reload
```

### Frontend won't start
```bash
# Make sure you're in the frontend directory
cd frontend

# Install dependencies
npm install

# Try starting again
npm run dev
```

### Login fails
1. **Check backend is running** - Visit `http://localhost:8000/health`
2. **Check browser console** - Look for errors (F12)
3. **Check Network tab** - See if API calls are failing
4. **Verify credentials** - Username: `admin`, Password: `admin123`

### Can't access dashboard
- Make sure you're logged in (check Navigation bar shows username)
- Try logging out and logging back in
- Clear browser localStorage: `localStorage.clear()` in console

---

## 📝 Default Credentials

```
Username: admin
Password: admin123
```

**To change these**, set environment variables:
```bash
export ADMIN_USERNAME=your_username
export ADMIN_PASSWORD=your_password
```

---

## 🎯 What You Should See

### Login Page (`/login`)
- Clean, modern login form
- Username and password fields
- Login button
- Default credentials displayed

### Dashboard (`/dashboard`)
- Analytics dashboard
- Charts and metrics
- Navigation with logout button
- Your username displayed

### Navigation Bar
- **When logged out:** "Admin Login" button
- **When logged in:** Username + "Logout" button

---

## ✅ Success Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] Can access `/login` page
- [ ] Can login with default credentials
- [ ] Redirected to `/dashboard` after login
- [ ] Username shown in navigation
- [ ] Can logout successfully
- [ ] Dashboard requires login (try accessing directly when logged out)

---

## 🎉 You're Done!

Your admin interface is now working! You can:
- Login and logout
- Access protected routes
- View the dashboard
- Manage authentication

**Next Steps:**
- Customize the dashboard
- Add more protected routes
- Change default credentials
- Deploy to production




