# Quick Fix: "Failed to fetch projects" Error

## The Problem

You're seeing "Failed to fetch projects" error on the frontend. This usually means:

1. **Backend server is not running** (most common)
2. **Backend server is running but on wrong port**
3. **CORS issue** (less likely if servers are both on localhost)

## Quick Solution

### Step 1: Start Backend Server

Open a terminal and run:

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
✅ Default project already exists: Pinterest
```

### Step 2: Start Frontend Server

Open **another terminal** and run:

```bash
cd frontend
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms
➜  Local:   http://localhost:5173/
```

### Step 3: Test the Connection

Open your browser and visit:
- **Frontend**: http://localhost:5173/projects
- **Backend API**: http://localhost:8000/api/v1/projects
- **API Docs**: http://localhost:8000/docs

### Step 4: Verify Pinterest Project

If the backend is running, you should see the Pinterest project when you:
1. Visit http://localhost:8000/api/v1/projects directly (should return JSON)
2. Visit http://localhost:5173/projects (should show the project)

## If Still Not Working

### Check Backend Logs

Look at the backend terminal - you should see logs when you visit the frontend:
```
INFO:     127.0.0.1:xxxxx - "GET /api/v1/projects HTTP/1.1" 200 OK
```

### Check Browser Console

Open DevTools (F12) → Console tab:
- Look for error messages
- Check Network tab → see if `/api/v1/projects` request is made
- Check if there's a CORS error

### Manual Test

Test the API directly:
```bash
curl http://localhost:8000/api/v1/projects
```

Expected response:
```json
[
  {
    "id": "poc-project-001",
    "name": "Pinterest",
    "api_key": "aO4s9yN2O3tScKFP***",
    "domain": "pinterest.com",
    "created_at": "2026-01-10T...",
    "updated_at": "2026-01-10T..."
  }
]
```

## Most Common Fix

**99% of the time, the issue is:**
- Backend server is not running
- Solution: Start it with `uvicorn app.main:app --reload --port 8000`

Once both servers are running, refresh the browser at http://localhost:5173/projects and you should see the Pinterest project!

---

**Status**: Ready to start servers  
**Next**: Start backend, then frontend, then visit Projects page
