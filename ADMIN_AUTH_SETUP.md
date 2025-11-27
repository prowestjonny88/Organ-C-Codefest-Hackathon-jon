# 🔐 Admin Authentication Setup Guide

## Overview

A complete JWT-based admin authentication system has been implemented for your hackathon project. This includes:

- **Backend**: JWT token generation, admin login/logout endpoints
- **Frontend**: Login page, protected routes, auth context
- **Security**: Token-based authentication with 24-hour expiration

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

New dependencies added:
- `python-jose[cryptography]` - JWT token handling
- `passlib[bcrypt]` - Password hashing (for future use)

### 2. Set Environment Variables

**For Local Development** (optional - defaults provided):
```bash
# Admin credentials
export ADMIN_USERNAME=admin
export ADMIN_PASSWORD=admin123

# JWT secret (change in production!)
export JWT_SECRET_KEY=your-secret-key-change-in-production-min-32-chars
```

**For Production (Render)**:
Add these environment variables in your Render dashboard:
- `ADMIN_USERNAME` - Admin username (default: "admin")
- `ADMIN_PASSWORD` - Admin password (default: "admin123")
- `JWT_SECRET_KEY` - Secret key for JWT signing (use a strong random string)

---

## 📡 API Endpoints

### `POST /api/v1/auth/login/json`
**Login endpoint (JSON format - recommended for frontend)**

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1440,
  "username": "admin"
}
```

### `POST /api/v1/auth/login`
**Login endpoint (OAuth2 form format - for Swagger UI)**

Uses standard OAuth2 form data format. Hidden from schema but available for testing.

### `GET /api/v1/auth/me`
**Get current authenticated user**

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "username": "admin",
  "is_admin": true
}
```

### `POST /api/v1/auth/logout`
**Logout endpoint**

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Logged out successfully"
}
```

---

## 🎨 Frontend Usage

### Login Page
Navigate to `/login` to access the admin login page.

**Default Credentials:**
- Username: `admin`
- Password: `admin123`

### Protected Routes
The `/dashboard` route is now protected. Users must be logged in to access it.

### Navigation
- **When logged out**: Shows "Admin Login" button
- **When logged in**: Shows username and "Logout" button

### Using Auth in Components

```tsx
import { useAuth } from "@/contexts/AuthContext";

function MyComponent() {
  const { user, isAuthenticated, login, logout } = useAuth();

  if (!isAuthenticated) {
    return <div>Please log in</div>;
  }

  return (
    <div>
      <p>Welcome, {user?.username}!</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

---

## 🔒 Protecting Backend Endpoints

To protect a backend endpoint, use the `get_current_admin` dependency:

```python
from jwt_auth import get_current_admin

@router.get("/protected")
async def protected_endpoint(admin: str = Depends(get_current_admin)):
    return {"message": f"Hello, {admin}!"}
```

---

## 📁 Files Created/Modified

### Backend
- ✅ `backend/jwt_auth.py` - JWT utilities and auth functions
- ✅ `backend/routes/auth.py` - Authentication endpoints
- ✅ `backend/main.py` - Registered auth router
- ✅ `backend/requirements.txt` - Added JWT dependencies

### Frontend
- ✅ `frontend/client/pages/Login.tsx` - Login page component
- ✅ `frontend/client/contexts/AuthContext.tsx` - Auth context provider
- ✅ `frontend/client/components/ProtectedRoute.tsx` - Route protection component
- ✅ `frontend/client/components/Navigation.tsx` - Updated with auth UI
- ✅ `frontend/client/App.tsx` - Added AuthProvider and protected routes
- ✅ `frontend/client/lib/api.ts` - Added auth functions

---

## 🧪 Testing

### 1. Test Login via API

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/json \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### 2. Test Protected Endpoint

```bash
# First, get token from login response
TOKEN="your-token-here"

curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

### 3. Test Frontend

1. Start backend: `cd backend && uvicorn main:app --reload`
2. Start frontend: `cd frontend/client && npm run dev`
3. Navigate to `http://localhost:5173/login`
4. Login with default credentials
5. Access `/dashboard` (should work)
6. Logout and try accessing `/dashboard` (should redirect to login)

---

## 🔐 Security Notes

### Current Implementation (Hackathon)
- ✅ JWT tokens with 24-hour expiration
- ✅ Token stored in localStorage
- ✅ Protected routes on frontend
- ✅ Admin credentials via environment variables

### Production Recommendations
1. **Change default credentials** - Set strong `ADMIN_USERNAME` and `ADMIN_PASSWORD`
2. **Use strong JWT secret** - Generate a random 32+ character string
3. **Implement token refresh** - Add refresh token mechanism
4. **Add token blacklist** - For logout functionality
5. **Use HTTP-only cookies** - Instead of localStorage (more secure)
6. **Add rate limiting** - On login endpoint
7. **Add password hashing** - If storing passwords in database
8. **Add 2FA** - For enhanced security

---

## 🐛 Troubleshooting

### "Could not validate credentials"
- Token expired (24 hours) - Login again
- Invalid token - Clear localStorage and login again
- Token not sent - Check Authorization header

### Login fails
- Check `ADMIN_USERNAME` and `ADMIN_PASSWORD` environment variables
- Verify backend is running
- Check browser console for errors

### Frontend redirects to login
- Token expired - Login again
- Token missing - Check localStorage
- Backend not running - Start backend server

---

## ✅ Status

**All features implemented and tested!**

- ✅ Backend JWT authentication
- ✅ Login/logout endpoints
- ✅ Frontend login page
- ✅ Protected routes
- ✅ Auth context
- ✅ Navigation updates
- ✅ Token management

Ready for deployment! 🚀




