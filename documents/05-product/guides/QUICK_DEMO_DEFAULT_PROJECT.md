# 🎬 Quick Demo Guide - Using Default Pinterest Project

**Perfect for Fast Demo - No Project Setup Needed**

This guide uses the default "Pinterest" project that's already created. Perfect for a quick 5-10 minute demo.

---

## 🎯 Demo Scenario: "Pin Discovery to Save Journey"

**Story**: Analyzing the inspiration journey from Pin View to Save using the default Pinterest project. Shows segment-level analysis (Planners vs Actors) to understand heterogeneous user behavior.

**Time**: ~5-10 minutes

---

## Step 0: Pre-populate Data (Before Demo - Run Once)

**Important**: Run this **before** your demo to pre-populate sample data.

**Terminal - Backend Directory:**
```bash
cd backend
source venv/bin/activate
python populate_sample_data.py
```

**Expected**: 420 events created (pin_view, save, click, purchase)

**See `PREPARE_DEMO.md` for detailed instructions.**

---

## Step 1: Start the Application (1 min)

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

**Expected Result:**
- ✅ Backend running on port 8000
- ✅ Frontend running on port 5173
- ✅ Default "Pinterest" project already exists

---

## Step 2: Get API Key from Default Project (30 sec)

**What to Say:**
> "I'll use the default Pinterest project that's already set up. Let me get the API key for tracking events."

**Actions:**
1. Click **"Projects"** in the navbar
2. Click on the **"Pinterest"** project (it should expand)
3. **Copy the API Key** (you'll need it for tracking events)
4. Note: Product Surface is "Home Feed"

**Expected Result:**
- ✅ See "Pinterest" project with API Key visible
- ✅ Product Surface: "Home Feed"
- ✅ API Key copied (save it for Step 4)

**What to Say:**
> "The default project is already set up with Home Feed as the Product Surface. This represents our main product initiative."

---

## Step 3: Create a Journey (2 min)

**What to Say:**
> "Now I'll create a journey to track the inspiration-to-action flow. This measures how users move from Pin View to Save - capturing intent formation, not just clicks."

**Actions:**
1. Click **"Journeys"** in the navbar
2. Verify the **Project** shown at the top is "Pinterest" (it should be selected by default)
   - If not, go to **Projects** page first and click on "Pinterest" project to select it
3. Click **"Create Journey"** button
4. Fill in:
   - **Journey Name**: `Pin Discovery to Save`
   - **Description**: `Track users from Pin View through planning to Save - measures inspiration quality`
   - **Stages** (Add 2 stages):
     - Stage 1: 
       - Name: `Pin View`
       - Event Type: **Select from dropdown** → `pin_view`
       - Order: `1`
     - Stage 2:
       - Name: `Save`
       - Event Type: **Select from dropdown** → `save`
       - Order: `2`
5. Click **"Create Journey"**

**Note**: 
- Event Type fields show as **dropdown menus** (not text input) because data is pre-populated
- Available event types from pre-populated data: `pin_view`, `save`, `click`, `purchase`
- You can only select event types that exist in your data (ensures journeys have data to analyze)
- The journey is automatically associated with the current project shown at the top ("Pinterest")

**What to Say:**
> "The UI automatically shows only event types that exist in our data. This ensures we create journeys using events that have actual data to analyze. This is important for a DS demo - we want to focus on analysis, not data collection."

**Expected Result:**
- ✅ Journey created: "Pin Discovery to Save"
- ✅ 2 stages defined: Pin View → Save
- ✅ Associated with "Pinterest" project

**What to Say:**
> "This journey measures inspiration quality - saves, not just clicks. This aligns with Pinterest's focus on intent formation over immediate action."

---

## Step 4: Verify Pre-populated Data (30 sec)

**What to Say:**
> "The data has already been collected from our experiment. Let me create a journey to analyze it. Notice that the event type dropdown shows only the events that exist in our data - pin_view, save, click, and purchase."

**Actions:**
1. Go to **"Journeys"** page
2. Click **"Create Journey"**
3. Notice: **Event Type** fields show as **dropdown menus** (not text input)
4. Available event types: `pin_view`, `save`, `click`, `purchase`
5. These are the events that exist in the pre-populated data

**Expected Result:**
- ✅ Event Type dropdown shows: pin_view, save, click, purchase
- ✅ Can only select from available event types
- ✅ Ensures journeys use events that have data

**What to Say:**
> "The UI automatically shows only event types that exist in our data. This ensures we create journeys using events that have actual data to analyze. This is important for a DS demo - we want to focus on analysis, not data collection."

**Note**: If you need to populate data, see `PREPARE_DEMO.md` for instructions.

---

## Step 5: View Overall Analytics (1 min)

**What to Say:**
> "Let me check the overall journey metrics first. This gives me the aggregate view before I segment."

**Actions:**
1. Click **"Dashboard"** (Journey Overview)
2. Select **Journey**: "Pin Discovery to Save"
3. Select **Date Range**: Today (or Last 7 days)
4. Leave segment filters empty (aggregate view)
5. View analytics

**Expected Result:**
- ✅ **Users Exposed**: 200 (100 Planners + 100 Actors)
- ✅ **Advanced Users**: 100 (60 Planners + 40 Actors)
- ✅ **Progression Rate**: 50% (100/200)
- ✅ Journey visualization shows 2 stages

**What to Say:**
> "Overall, we have a 50% progression rate from Pin View to Save. But this aggregate hides important differences between user segments. Let me break it down by user intent."

---

## Step 6: Segment Analysis - Break Down by User Intent (2 min)

**What to Say:**
> "Pinterest users have different intent - Planners save for later, Actors act quickly. I need to see how each segment behaves differently. This is critical for Pinterest because we can't optimize for clicks at the expense of saves."

**Actions:**
1. On **Journey Overview** page
2. Select **Journey**: "Pin Discovery to Save"
3. **Break Down By**: Select "User Intent"
4. View segment comparison

**Expected Result:**
- ✅ **Segment Comparison Table** shows:
  - **Planner**: 100 users exposed, 60 advanced, **60% progression rate**
  - **Actor**: 100 users exposed, 40 advanced, **40% progression rate**
- ✅ **Per-Segment Visualization**:
  - Planner segment: Higher progression (60%)
  - Actor segment: Lower progression (40%)
- ✅ **Total Summary**: Aggregate across segments

**What to Say:**
> "Here's the key insight: **Planners show 60% progression** from Pin View to Save, while **Actors show 40%**. This makes sense - Planners are saving content for planning, Actors are ready to act immediately.

> **For Pinterest DS**, this segment-level analysis is critical. If we optimize for clicks and hurt saves, we need to understand which segment is affected. If Planners are harmed, we risk degrading inspiration quality - Pinterest's core value proposition."

---

## Step 7: Additional Segment Analysis (Optional - 1 min)

**What to Say:**
> "Let me also break this down by other dimensions to show the full analytical capabilities."

**Actions:**
1. **Break Down By**: Try "Surface" or "User Tenure"
2. Or use **Segment Filters**:
   - **User Intent**: Select "Planner" only
   - **Surface**: Select "Home"
   - View filtered analytics

**Expected Result:**
- ✅ See segment-specific metrics
- ✅ Compare different dimensions
- ✅ Understand heterogeneous effects

**What to Say:**
> "This tool supports multi-dimensional segmentation - user intent, surface, content category, and user tenure. This enables Pinterest DS to understand heterogeneous effects and make segment-specific decisions."

---

## Step 8: Decision & Insights (1 min)

**What to Say:**
> "Based on this analysis, here are the key insights for Pinterest DS:"

### Key Insights:

1. **Heterogeneous User Behavior**:
   - Planners show 60% progression (high save rate)
   - Actors show 40% progression (lower save rate)
   - Both segments are valuable, but for different reasons

2. **Metrics That Matter**:
   - **Progression Rate** (not conversion rate) - captures intent formation
   - **Users Exposed** (not total users) - Pinterest framing
   - **Advanced Users** (not completed users) - inspiration quality

3. **Decision Framework**:
   - **Planners**: Protect their experience (preserve save rates)
   - **Actors**: Can optimize for clicks (they're ready to act)
   - **Guardrails**: Check save-to-impression ratio, content diversity

**What to Say:**
> "This demonstrates Pinterest DS thinking:
> - We measure inspiration quality (saves), not just clicks
> - We evaluate heterogeneous segment effects
> - We understand that different segments have different needs
> - We make segment-specific recommendations, not one-size-fits-all

> This is exactly how Pinterest DS prevents harmful over-optimization and protects long-term user value."

---

## 🎯 Demo Summary

**What You Demonstrated:**
1. ✅ **Used Default Project** - "Pinterest" with Product Surface "Home Feed"
2. ✅ **Created Journey** - "Pin Discovery to Save" (inspiration quality metric)
3. ✅ **Tracked Events** - With user intent segments (Planner vs Actor)
4. ✅ **Segment Analysis** - Break down by User Intent (heterogeneous effects)
5. ✅ **Pinterest DS Framing** - Inspiration quality, intent formation

**Key Metrics Shown:**
- Progression Rate: 50% overall, 60% Planners, 40% Actors
- Users Exposed: 200
- Advanced Users: 100
- Segment Comparison: Planner vs Actor

**Key Insights:**
- Heterogeneous user behavior (Planners save more)
- Segment-level analysis is critical
- Protect inspiration quality (saves)

---

## 💡 Talking Points for Interview

**Throughout the demo, emphasize:**

1. **"This measures inspiration quality"** - Saves, not just clicks
2. **"Segments matter"** - Planners and Actors behave differently
3. **"Pinterest framing"** - Journey, progression rate, users exposed
4. **"Segment-specific decisions"** - Not one-size-fits-all
5. **"Guardrails"** - Check save ratios, content diversity

**This demonstrates:**
- ✅ Understanding of Pinterest business model
- ✅ Advanced analytics (segmentation, heterogeneous effects)
- ✅ Product thinking (inspiration quality, intent formation)
- ✅ Technical skills (tool usage, data analysis)
- ✅ Communication (clear insights, recommendations)

---

## ⚡ Ultra-Quick Demo (3 Minutes)

If very short on time:

1. **Pre-populate Data** (30 sec): Run `python populate_sample_data.py` (do this before demo)
2. **Create Journey** (1 min): "Pin Discovery to Save" with 2 stages (select event types from dropdown)
3. **View Analytics** (30 sec): Journey Overview → Select journey → View overall metrics
4. **Segment Analysis** (1 min): Break down by User Intent, show Planner 60% vs Actor 40%

**Key Message**: "This tool helps Pinterest DS analyze inspiration journeys by segment, understand heterogeneous user behavior, and make data-driven decisions that preserve inspiration quality."

---

## 🎓 Preparation Tips

1. **Pre-populate data** - Run `python populate_sample_data.py` **before** the demo (see Step 0)
2. **Practice the script** - Know what to say at each step
3. **Explain the "why"** - Don't just click buttons, explain Pinterest DS reasoning
4. **Emphasize segments** - Show you understand heterogeneous effects
5. **Connect to product** - Link metrics to Pinterest's core value (inspiration)
6. **Focus on analysis** - Data is pre-populated, so focus on analytics and decision-making

---

## 📝 Notes for Smooth Demo

**Common Questions & Answers:**

**Q: "Why use the default project?"**
A: "The default Pinterest project is already set up, which makes for a quick demo. In production, you'd create project-specific initiatives (e.g., 'Home Feed Ranking Refresh', 'Search Relevance Update')."

**Q: "What if I want to create a new project?"**
A: "You can! Click 'Create Project' and follow the full demo guide. For this quick demo, using the default project saves time."

**Q: "Why pre-populate data?"**
A: "For a DS demo, we want to focus on analysis and decision-making, not data collection. Pre-populating data allows us to quickly create journeys, analyze metrics, and demonstrate segment-level insights without spending time on event generation."

**Q: "Can I use this for real data?"**
A: "Yes! The pre-population script is just for demo purposes. In production, you'd track real events via the API or JavaScript tracking code. The tool works the same way with real user interactions."

---

**Status**: Ready to demo with default project! 🎬

This demo showcases:
- Quick setup (no project creation needed)
- Pinterest DS thinking
- Segment-aware analytics
- Technical skills

**Perfect for Pinterest DS interview!** 🎯
