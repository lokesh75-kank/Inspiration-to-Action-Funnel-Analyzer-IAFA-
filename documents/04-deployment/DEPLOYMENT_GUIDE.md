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
- **Free tier**: 750 hours/month (resets every month - enough for one service running 24/7)
- **Important**: Free tier services automatically "spin down" after 15 minutes of inactivity
  - When someone visits, it "spins up" in ~30 seconds (cold start)
  - You only use hours when the service is actually running
  - This means 750 hours can last much longer than one month!
- Supports both backend (Python) and frontend (static)
- Automatic HTTPS
- Custom domain support
- **Best for**: Full-stack deployment, demos, portfolios
- **What happens after 750 hours?**: The limit resets every month. Plus, with auto spin-down, you rarely hit the limit!

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

### Prerequisites
- GitHub repository with your code (already done if you cloned/pushed)
- GitHub account connected to Render.com

### Step 0: Connect GitHub to Render (First Time Only)

1. **Sign up/Login**: Go to [render.com](https://render.com)
   - Click "Get Started for Free" or "Log In"
   - Sign up with email or GitHub (recommended: use GitHub)

2. **Connect GitHub Account** (if not already connected):
   - Go to Dashboard
   - Click "New +" → Select any service type
   - Click "Connect GitHub" or "Connect Repository"
   - Authorize Render to access your GitHub repositories
   - You only need to do this once!

### Part 1: Deploy Backend to Render (GitHub Integration)

1. **Create Web Service**:
   - Click "New +" → "Web Service"
   - Select "Connect a repository"
   - Find and select your repository: `Inspiration-to-Action-Funnel-Analyzer-IAFA-`
   - Click "Connect"

2. **Configure Backend Settings**:
   ```
   Name: iafa-backend
   Region: Oregon (or closest to you)
   Branch: main (or your default branch)
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt && python populate_sample_data.py
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

3. **Environment Variables** (optional, will use defaults):
   - Click "Advanced" → "Add Environment Variable"
   - You can skip this for now (backend uses defaults)
   - Render automatically sets `PORT` variable

4. **Deploy**:
   - Click "Create Web Service"
   - Render will:
     1. Clone your GitHub repository
     2. Run the build command
     3. Start the service
   - First deploy takes ~5-10 minutes

5. **Note the URL**: 
   - Once deployed, you'll see something like: `https://iafa-backend.onrender.com`
   - Copy this URL - you'll need it for the frontend!

6. **Test Backend**:
   - Visit: `https://iafa-backend.onrender.com/docs`
   - You should see the FastAPI Swagger documentation
   - ✅ Backend is deployed!

### Part 2: Deploy Frontend to Render (Static Site with GitHub)

1. **Create Static Site**:
   - Click "New +" → "Static Site"
   - Select "Connect a repository"
   - Find and select the same repository: `Inspiration-to-Action-Funnel-Analyzer-IAFA-`
   - Click "Connect"

2. **Configure Frontend Settings**:
   ```
   Name: iafa-frontend
   Branch: main (or your default branch)
   Root Directory: frontend
   Build Command: npm install && npm run build
   Publish Directory: dist
   ```

3. **Environment Variables** (IMPORTANT):
   - Click "Add Environment Variable"
   - Add this variable:
     ```
     Key: VITE_API_URL
     Value: https://iafa-backend.onrender.com/api/v1
     ```
   - Replace `iafa-backend.onrender.com` with YOUR backend URL from Part 1
   - ⚠️ **Important**: This must match your backend URL exactly!

4. **Deploy**:
   - Click "Create Static Site"
   - Render will:
     1. Clone your GitHub repository
     2. Install npm dependencies
     3. Build the frontend
     4. Deploy static files
   - First deploy takes ~3-5 minutes

5. **Note the URL**: 
   - Once deployed, you'll see something like: `https://iafa-frontend.onrender.com`
   - This is your live application URL! 🎉

### Part 3: Auto-Deploy from GitHub (Bonus!)

**Automatic Deployments** (already enabled by default):
- ✅ Every push to `main` branch automatically triggers a new deployment
- ✅ Render watches your GitHub repository
- ✅ No need to manually redeploy after code changes
- ✅ Just push to GitHub: `git push` → Auto-deploys! 🚀

**To update your app:**
```bash
# Make changes to your code
git add .
git commit -m "Your changes"
git push

# Render automatically detects the push and redeploys!
# Check Render dashboard to see deployment progress
```

### Part 4: Test Your Deployment

1. **Visit Frontend URL**: 
   - Go to: `https://iafa-frontend.onrender.com`
   - The app should load! ✨

2. **First Visit (Cold Start)**:
   - Free tier services "spin down" after 15 minutes
   - First visit after spin-down takes ~30 seconds (cold start)
   - Subsequent visits are instant!

3. **Test Features**:
   - Select a journey
   - View analytics
   - Create a new journey
   - Export reports
   - Everything should work! 🎯

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

## 🌐 Update CORS Settings (Optional for Render)

### For Render.com Deployment

**Good News**: The current code already uses `allow_origins=["*"]` for POC/demo, so it works out of the box! ✅

However, if you want to restrict CORS for security, update `backend/app/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local development
        "https://iafa-frontend.onrender.com",  # Your Render frontend URL
        # Add more origins as needed
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**For POC/Demo (current setup)**: 
- Already configured with `allow_origins=["*"]`
- Works immediately - no changes needed!
- Perfect for demos and portfolios

**After updating CORS**:
- Commit changes: `git add . && git commit -m "Update CORS"`
- Push to GitHub: `git push`
- Render auto-deploys the changes!

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
- **Python version errors (Rust compilation)**: 
  - Set Python version to 3.11.0 or 3.12.0 in Render settings
  - Or create `runtime.txt` file with `python-3.11.0` in backend directory
  - Python 3.13 may have issues with package wheels requiring Rust compilation

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

**Quick deployment command (after initial setup):**
```bash
# Just push to GitHub, Render auto-deploys!
git add .
git commit -m "Your changes"
git push

# Render automatically detects the push and redeploys!
# Check Render dashboard to see deployment status
```

**Initial Setup Time**: ~15-20 minutes (one-time setup)
**Future Updates**: ~30 seconds (just push to GitHub!)

---

## ❓ FAQ: Render.com Free Tier

### Q: What does "750 hours/month" actually mean?
**A**: 
- You get 750 hours of service runtime per month
- This resets every month (not a one-time limit!)
- In a 31-day month, there are 744 hours (31 × 24)
- So 750 hours = enough for one service to run 24/7 for the entire month

### Q: What happens after 750 hours are used?
**A**: 
- The limit **resets every month** - you get 750 hours again!
- Most users never hit the limit because:
  - Free tier services automatically "spin down" after 15 minutes of inactivity
  - They only use hours when actually running (when someone visits)
  - For a demo/portfolio site with occasional traffic, 750 hours can last months!

### Q: What happens when a free service "spins down"?
**A**: 
- After 15 minutes of no traffic, the service stops running
- When someone visits, it automatically "spins up" in ~30 seconds (cold start)
- This saves hours - you only pay for active runtime!

### Q: Is the free tier good for demos/portfolios?
**A**: 
- **Yes, absolutely!** 
- Perfect for demo sites, portfolios, and interview projects
- The auto spin-down means low-traffic sites use very few hours
- 750 hours/month is more than enough for occasional access

### Q: What if I need guaranteed uptime (always on)?
**A**: 
- Free tier is not for production apps that need 100% uptime
- For production, consider Render's paid tier ($7/month for always-on)
- For demos/interviews/portfolios, free tier is perfect!

---

Good luck with your deployment! 🚀
