# 🌐 API Configuration Guide

## How It Works

The frontend automatically detects whether to use **localhost** (development) or **production API** (deployment) based on where it's running.

---

## 🔧 Current Configuration

### **Local Development** (Automatic)
- **When:** Running on `localhost` or `127.0.0.1`
- **Uses:** `http://localhost:8000` (your local backend)
- **No changes needed!** ✅

### **Production Deployment** (Automatic)
- **When:** Deployed to any other domain (e.g., Netlify, Vercel, etc.)
- **Uses:** `https://organ-c-codefest-hackathon.onrender.com` (Render backend)
- **No changes needed!** ✅

---

## 📋 How It Detects Environment

The code checks `window.location.hostname`:

```typescript
// If hostname is localhost or 127.0.0.1 → Development mode
// Otherwise → Production mode
const isLocalDev = window.location.hostname === "localhost" || 
                   window.location.hostname === "127.0.0.1";
```

---

## 🎯 Summary

| Environment | Hostname | API URL | Action Required |
|------------|----------|---------|-----------------|
| **Local Dev** | `localhost` or `127.0.0.1` | `http://localhost:8000` | ✅ None - Automatic |
| **Production** | Any other domain | `https://organ-c-codefest-hackathon.onrender.com` | ✅ None - Automatic |

---

## 🔄 Manual Override (Advanced)

If you need to force production API while testing locally:

1. Open `frontend/client/lib/api.ts`
2. Change line 11:
   ```typescript
   const FORCE_PRODUCTION = true;  // Force production API
   ```
3. Restart your dev server

**Use case:** Testing production API from your local machine.

---

## ✅ Verification

Check the browser console to see which API is being used:

```javascript
🌐 API Configuration: {
  isDevelopment: true/false,
  FORCE_PRODUCTION: false,
  API_BASE_URL: "http://localhost:8000" or "https://organ-c-codefest-hackathon.onrender.com",
  hostname: "localhost" or your-domain.com
}
```

---

## 🚀 For Deployment

**No changes needed!** When you deploy:

1. Build your frontend: `npm run build`
2. Deploy to Netlify/Vercel/etc.
3. The frontend will automatically use the production API endpoint

The configuration automatically switches based on the hostname! 🎉

