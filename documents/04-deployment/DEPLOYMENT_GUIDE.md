# Deployment Guide for IAFA

**How to Deploy and Share the Inspiration-to-Action Funnel Analyzer**

---

## 🎯 Quick Start Options

### Option 1: **Local Development** (Best for Testing)
- Run on your computer
- Free, no account needed
- Full control
- Best for demos and interviews

### Option 2: **Free Cloud Deployment** (Best for Sharing)
- Accessible via URL
- Free hosting options available
- Share with others easily
- Professional for portfolio/demos

---

## 📦 Option 1: Local Setup (Recommended for Interviews/Demos)

### Prerequisites
- Python 3.11+ (check: `python3 --version`)
- Node.js 18+ (check: `node --version`)
- npm (comes with Node.js)

### Step-by-Step Setup

#### 1. Clone or Download the Repository
```bash
git clone https://github.com/lokesh75-kank/Inspiration-to-Action-Funnel-Analyzer-IAFA-.git
cd "Inspiration-to-Action-Funnel-Analyzer-IAFA-"
```

#### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Pre-populate sample data
python populate_sample_data.py
```

#### 3. Start Backend Server

```bash
# Make sure you're in the backend directory with venv activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend should be running at: `http://localhost:8000`

#### 4. Setup Frontend (New Terminal)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend should be running at: `http://localhost:5173` (or similar port)

#### 5. Access the Tool
- Open browser: `http://localhost:5173`
- The tool is ready to use!

---

## ☁️ Option 2: Free Cloud Deployment

### Recommended Free Platforms

#### **Option A: Render.com** (Easiest, Recommended)
- **Free tier**: 750 hours/month
- Supports both backend (Python) and frontend (static)
- Automatic HTTPS
- Custom domain support
- **Best for**: Full-stack deployment

#### **Option B: Railway.app**
- **Free tier**: $5 credit/month
- Easy deployment
- Good for Python backends
- **Best for**: Backend deployment

#### **Option C: Vercel + Railway/Render**
- **Vercel**: Frontend (excellent for React)
- **Railway/Render**: Backend
- Both have free tiers
- **Best for**: Production-ready setup

---

## 🚀 Deploy to Render.com (Recommended)

### Part 1: Deploy Backend to Render

1. **Sign up**: Go to [render.com](https://render.com) and sign up (free)

2. **Create Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure Backend**:
   ```
   Name: iafa-backend
   Region: Oregon (or closest to you)
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt && python populate_sample_data.py
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Environment Variables** (optional, will use defaults):
   ```
   PORT=10000 (Render sets this automatically)
   ```

5. **Deploy**: Click "Create Web Service"

6. **Note the URL**: Something like `https://iafa-backend.onrender.com`

### Part 2: Deploy Frontend to Render (Static Site)

1. **Create Static Site**:
   - Click "New +" → "Static Site"
   - Connect your GitHub repository

2. **Configure Frontend**:
   ```
   Name: iafa-frontend
   Branch: main
   Root Directory: frontend
   Build Command: npm install && npm run build
   Publish Directory: dist
   ```

3. **Environment Variables**:
   ```
   VITE_API_URL=https://iafa-backend.onrender.com/api/v1
   ```

4. **Deploy**: Click "Create Static Site"

5. **Note the URL**: Something like `https://iafa-frontend.onrender.com`

### Part 3: Update Frontend API URL

1. **Edit `frontend/src/services/api.ts`**:
   ```typescript
   // For production, use environment variable
   const API_URL = import.meta.env.VITE_API_URL || '/api/v1'
   ```

2. **Update `.env` or Render environment variable**:
   Set `VITE_API_URL` to your backend URL (from Part 1)

3. **Rebuild frontend** (Render will auto-deploy)

---

## 🚂 Deploy to Railway.app

### Backend Deployment

1. **Sign up**: Go to [railway.app](https://railway.app) (free tier)

2. **New Project**:
   - Click "New Project"
   - "Deploy from GitHub repo"
   - Select your repository

3. **Configure Service**:
   - Select "backend" folder
   - Railway auto-detects Python
   - Add start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Add Script** (in `backend/railway.json` or via UI):
   ```json
   {
     "build": {
       "builder": "NIXPACKS",
       "buildCommand": "pip install -r requirements.txt && python populate_sample_data.py"
     }
   }
   ```

5. **Get URL**: Railway provides URL like `https://iafa-backend.up.railway.app`

### Frontend Deployment (Vercel)

1. **Sign up**: Go to [vercel.com](https://vercel.com) (free)

2. **Import Project**:
   - Click "Add New" → "Project"
   - Import from GitHub
   - Select repository

3. **Configure**:
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   ```

4. **Environment Variables**:
   ```
   VITE_API_URL=https://iafa-backend.up.railway.app/api/v1
   ```

5. **Deploy**: Click "Deploy"

---

## 🔧 Alternative: Deploy Both to Railway

Railway can host both:

1. **Backend Service**: Follow Railway backend steps above

2. **Frontend Service**:
   - Add new service in same project
   - Select "frontend" folder
   - Build command: `npm install && npm run build`
   - Start command: `npx serve -s dist -l $PORT`
   - Add environment variable: `VITE_API_URL=<backend-url>/api/v1`

---

## 🌐 Update CORS Settings

### For Cloud Deployment

Update `backend/app/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://your-frontend-url.vercel.app",  # Add your frontend URL
        "https://your-frontend-url.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Or for POC/demo purposes (less secure):

```python
allow_origins=["*"]  # Allows all origins (only for demos!)
```

---

## 📝 Deployment Checklist

### Before Deploying
- [ ] Test locally first
- [ ] Ensure `populate_sample_data.py` runs successfully
- [ ] Check all environment variables
- [ ] Update CORS settings for production URLs
- [ ] Test API endpoints work
- [ ] Test frontend connects to backend

### After Deploying
- [ ] Verify backend is accessible (check `/docs` endpoint)
- [ ] Verify frontend loads
- [ ] Test journey creation
- [ ] Test analytics dashboard
- [ ] Test report export
- [ ] Share URL with others!

---

## 🔗 Quick Links for Free Deployment

- **Render**: https://render.com
- **Railway**: https://railway.app
- **Vercel**: https://vercel.com
- **Netlify**: https://netlify.com (alternative for frontend)

---

## 💡 Tips for Interviews/Demos

### Option 1: Screen Share Local Setup
- Run locally during interview
- Screen share your browser
- Show the tool in action
- **Pros**: No deployment needed, full control
- **Cons**: Requires setup during interview

### Option 2: Pre-Deploy to Cloud
- Deploy before interview
- Share the URL
- Interviewer can explore independently
- **Pros**: Professional, accessible anytime
- **Cons**: Requires initial deployment setup

### Option 3: Hybrid Approach
- Have cloud URL ready as backup
- Run locally for live demo
- Share URL for later exploration
- **Pros**: Best of both worlds
- **Cons**: Requires both setups

---

## 🐛 Troubleshooting

### Backend Issues
- **Port already in use**: Change port in start command
- **Import errors**: Ensure virtual environment is activated
- **Database errors**: Run `populate_sample_data.py` again

### Frontend Issues
- **Can't connect to backend**: Check API URL in environment variables
- **CORS errors**: Update CORS settings in backend
- **Build errors**: Check Node.js version (18+)

### Deployment Issues
- **Build fails**: Check build logs in deployment platform
- **Environment variables**: Ensure they're set correctly
- **Static files not serving**: Check publish directory is `dist`

---

## 📚 Additional Resources

- **Render Docs**: https://render.com/docs
- **Railway Docs**: https://docs.railway.app
- **Vercel Docs**: https://vercel.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Vite Docs**: https://vitejs.dev

---

## 🎯 Recommended Setup for Interview

**For maximum impact:**
1. Deploy to Render or Railway (free, easy)
2. Have URL ready before interview
3. Also have local setup ready as backup
4. Test everything the day before
5. Share URL in portfolio/resume

**Quick deployment command (after setup):**
```bash
# Just push to GitHub, Render/Railway auto-deploys!
git push
```

---

Good luck with your deployment! 🚀
