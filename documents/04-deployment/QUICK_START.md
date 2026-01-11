# Quick Start Guide - IAFA

**Get started in 5 minutes!**

---

## 🚀 For Users (Local Setup)

### Step 1: Prerequisites
- Python 3.11+ installed
- Node.js 18+ installed
- Terminal/Command Prompt

### Step 2: Clone Repository
```bash
git clone https://github.com/lokesh75-kank/Inspiration-to-Action-Funnel-Analyzer-IAFA-.git
cd "Inspiration-to-Action-Funnel-Analyzer-IAFA-"
```

### Step 3: Start Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python populate_sample_data.py
uvicorn app.main:app --reload --port 8000
```

**Keep this terminal open!** Backend is running.

### Step 4: Start Frontend (New Terminal)
```bash
cd frontend
npm install
npm run dev
```

### Step 5: Open Browser
- Go to: `http://localhost:5173`
- **You're ready to use IAFA!**

---

## 📱 What Can Users Do?

### 1. **View Journey Analytics**
- Select a journey from the dropdown
- View stage-by-stage progression
- See conversion rates and drop-offs
- Analyze segment breakdowns

### 2. **Create Custom Journeys**
- Go to "Journeys" tab
- Click "Create Journey"
- Add stages (pin_view → save → click)
- Analyze your custom journey

### 3. **Segment Analysis**
- Filter by user intent, tenure, surface
- Break down by segments
- Compare segment performance
- Identify opportunities

### Step 4: **Export Reports**
- Click "Export Report" button
- Choose format: HTML, CSV, or Text
- Share with team/leadership
- Use in presentations

---

## ☁️ For Cloud Deployment (Free)

### Option 1: Render.com (Easiest)
1. Sign up at [render.com](https://render.com)
2. Deploy backend as "Web Service"
3. Deploy frontend as "Static Site"
4. Set environment variables
5. Get shareable URL!

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for detailed instructions.

### Option 2: Railway.app
1. Sign up at [railway.app](https://railway.app)
2. Deploy backend service
3. Deploy frontend service
4. Get shareable URL!

---

## 🎯 Quick Demo Flow

1. **Open Journey Overview**
   - Select "Pin Discovery to Save" journey
   - View the analytics dashboard

2. **Explore Segments**
   - Select "Break Down By: User Intent"
   - See Planner vs Actor performance
   - Compare conversion rates

3. **Export Report**
   - Click "Export Report"
   - Choose HTML format
   - Download and open

4. **Create Custom Journey**
   - Go to "Journeys" tab
   - Create new journey
   - Analyze it in dashboard

---

## ❓ Need Help?

- **Full Documentation**: See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
- **User Guide**: See [documents/05-product/USER_GUIDE.md](./documents/05-product/USER_GUIDE.md)
- **Demo Guide**: See [LIVE_DEMO_GUIDE.md](./LIVE_DEMO_GUIDE.md)

---

## 🔗 Links

- **GitHub**: https://github.com/lokesh75-kank/Inspiration-to-Action-Funnel-Analyzer-IAFA-
- **Demo URL**: (Deploy to get your URL!)

---

**Ready to analyze inspiration-to-action journeys!** 🚀
