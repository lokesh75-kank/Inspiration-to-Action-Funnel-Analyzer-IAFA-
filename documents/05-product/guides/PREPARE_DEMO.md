# 🎯 Prepare Demo Data - Quick Setup Guide

**Before your demo, run this once to pre-populate sample data.**

This creates events with common Pinterest event types: `pin_view`, `save`, `click`, `purchase`

---

## Step 1: Pre-populate Sample Data

**Terminal - Backend Directory:**
```bash
cd backend
source venv/bin/activate
python populate_sample_data.py
```

**Expected Output:**
```
📊 Pre-populating sample data for IAFA Demo...
✅ Using project: Pinterest (ID: poc-project-001)
📝 Generating events...
👥 Generating Planner user events...
👥 Generating Actor user events...
✅ Generated 420 events

📊 Event Summary:
   - pin_view: 200 events (100 Planners + 100 Actors)
   - save: 100 events (60 Planners + 40 Actors)
   - click: 80 events (30 Planners + 50 Actors)
   - purchase: 40 events (15 Planners + 25 Actors)

🎯 Available Event Types:
   - pin_view
   - save
   - click
   - purchase

📋 Suggested Journeys:
   1. pin_view → save (most common)
   2. pin_view → save → click
   3. pin_view → click
   4. pin_view → save → click → purchase

✅ Sample data pre-populated successfully!
```

---

## Step 2: Verify Data (Optional)

**Check if data was created:**
```bash
# Check Parquet files
ls -lh backend/data/events/project_poc-project-001/
```

**Expected:** You should see `.parquet` files in the directory.

---

## Step 3: Start Servers

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Browser:** http://localhost:5173

---

## Step 4: Demo Flow

1. **Create Journey** - Use "Journeys" page
   - Event types will show as dropdown (pin_view, save, click, purchase)
   - Select from available event types only

2. **View Analytics** - Use "Dashboard" (Journey Overview)
   - Data is already available
   - Focus on analysis, not data generation

3. **Segment Analysis** - Break down by User Intent
   - Planners vs Actors comparison
   - Focus on insights and decision-making

---

## Available Journeys to Demo

With pre-populated data, you can create:

1. **pin_view → save** (most common)
   - 200 users exposed
   - 100 advanced (50% progression)
   - Planners: 60% progression
   - Actors: 40% progression

2. **pin_view → save → click**
   - Full journey
   - Shows progression through all stages

3. **pin_view → click**
   - Direct action path
   - Actors: 50% progression

4. **pin_view → save → click → purchase**
   - Complete journey
   - Shows end-to-end progression

---

## Key Benefits

✅ **Data Already Exists** - No need to generate events during demo  
✅ **UI Shows Available Events** - Dropdown with event types from data  
✅ **Focus on Analytics** - More time for insights and decision-making  
✅ **Predictable Results** - Consistent metrics for demo  
✅ **Multiple Journey Options** - Create different journeys with same data  

---

## Notes

- Data persists across server restarts
- If you want fresh data, delete Parquet files and re-run script
- Event types in UI dropdown are based on actual data (from Parquet files)
- If no data exists yet, UI shows text input (allows any event type)

---

**Status**: Ready to demo! 🎬
