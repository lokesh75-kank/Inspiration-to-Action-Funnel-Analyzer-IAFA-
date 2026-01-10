# ✅ Live Demo Checklist - Pinterest DS Interview

## Before Demo

- [ ] Backend server running on port 8000
- [ ] Frontend server running on port 5173
- [ ] Browser open to http://localhost:5173
- [ ] Browser DevTools open (F12) for console
- [ ] API Key copied from Projects page
- [ ] Demo script ready (QUICK_DEMO_SCRIPT.js)

## Demo Flow (10-15 minutes)

### Setup (2 min)
- [ ] ✅ Start backend: `uvicorn app.main:app --reload --port 8000`
- [ ] ✅ Start frontend: `npm run dev`
- [ ] ✅ Open http://localhost:5173
- [ ] ✅ Verify default "Pinterest" project exists

### Step 1: Create Project (2 min)
- [ ] Click "Projects"
- [ ] Click "Create Project"
- [ ] Enter: Name: "Home Feed Ranking Refresh"
- [ ] Enter: Product Surface: "Home Feed"
- [ ] Click "Create Project"
- [ ] **Say**: "This represents a product initiative - a Home Feed ranking experiment"

### Step 2: Create Journey (2 min)
- [ ] Click "Journeys"
- [ ] Click "Create Journey"
- [ ] Enter: Name: "Pin Discovery to Save"
- [ ] Select Project: "Home Feed Ranking Refresh"
- [ ] Add Stage 1: Pin View (pin_view, order 1)
- [ ] Add Stage 2: Save (save, order 2)
- [ ] Add Stage 3: Click (click, order 3) - optional
- [ ] Click "Create Journey"
- [ ] **Say**: "This measures inspiration quality - saves, not just clicks"

### Step 3: Track Baseline Events (2 min)
- [ ] Open browser console (F12)
- [ ] Copy API Key from Projects page
- [ ] Update QUICK_DEMO_SCRIPT.js with API Key
- [ ] Run baseline tracking section
- [ ] **Say**: "Simulating baseline data - Planner users save more (60%), Actor users click more (50%)"

### Step 4: View Overall Analytics (1 min)
- [ ] Go to Dashboard (Journey Overview)
- [ ] Select Journey: "Pin Discovery to Save"
- [ ] Select Date Range: Last 7 days (or appropriate range)
- [ ] View aggregate metrics
- [ ] **Say**: "Overall 50% progression, but this hides segment differences"

### Step 5: Segment Analysis (2 min)
- [ ] **Break Down By**: Select "User Intent"
- [ ] View segment comparison
- [ ] **Say**: "Planners show 60% progression, Actors show 40% - heterogeneous effects"

### Step 6: Track Experiment Events (2 min)
- [ ] Run experiment tracking section in console
- [ ] **Say**: "Simulating experiment - click-optimized ranking reduces Planner saves"

### Step 7: Analyze Tradeoffs (2 min)
- [ ] Select date range that includes experiment events
- [ ] **Break Down By**: "User Intent" again
- [ ] Compare: Planner 40% (↓20%) vs Actor 40% (stable)
- [ ] **Say**: "Planners harmed, Actors stable - segment imbalance, need to check guardrails"

### Step 8: Guardrail Check (1 min)
- [ ] Calculate: Save-to-impression ratio (before vs after)
- [ ] **Say**: "Save ratio down 10% - inspiration quality declining, reject global rollout"

### Step 9: Decision (1 min)
- [ ] **Recommend**: Segment-specific ranking
- [ ] **Say**: "Ship for Actors, rollback for Planners - preserve inspiration quality"

## Key Talking Points

✅ **Always Mention:**
- "This measures inspiration quality, not just clicks"
- "Segments behave differently - we need segment-level analysis"
- "Guardrails prevent harmful optimization"
- "Tradeoffs must be explicit - clicks up, saves down"
- "Decision: Segment-specific solution, not global rollout"

✅ **Avoid Saying:**
- ❌ "Conversion rate" (say "progression rate")
- ❌ "Drop-off" (say "natural attrition")
- ❌ "Completed users" (say "advanced users")
- ❌ "Domain" (say "product surface")

## Quick 5-Minute Version

If short on time:
1. ✅ Create Project: "Home Feed Ranking Refresh"
2. ✅ Create Journey: "Pin Discovery to Save" (2 stages)
3. ✅ Track events (run script)
4. ✅ Segment analysis (Break down by User Intent)
5. ✅ Decision: "Planners harmed → recommend segment-specific ranking"

**Key Message**: "This tool helps Pinterest DS evaluate experiments by segment, check guardrails, and make decisions that preserve inspiration quality."

---

**Status**: Ready to demo! 🎬
