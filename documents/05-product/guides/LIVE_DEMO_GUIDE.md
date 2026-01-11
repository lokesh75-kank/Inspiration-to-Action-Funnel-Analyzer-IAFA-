# 🎬 IAFA Live Demo Guide - Step-by-Step Example

**Perfect for Pinterest DS Interview Demonstration**

This guide walks through a complete, realistic example from project creation to decision-making.

---

## 🎯 Demo Scenario: "Home Feed Ranking Experiment"

**Story**: A Pinterest DS is evaluating a Home Feed ranking algorithm change. The new algorithm increases click-through rates but might hurt save rates (inspiration quality). Using IAFA, the DS analyzes segment-level effects and makes a data-driven decision.

**Time**: ~10-15 minutes

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

---

## Step 2: Create Project - "Home Feed Ranking Refresh" (2 min)

**What to Say:**
> "I'm evaluating a Home Feed ranking algorithm change. This is a product initiative, so I'll create a project for it."

**Actions:**
1. Click **"Projects"** in the navbar
2. Click **"Create Project"** button
3. Fill in:
   - **Project Name**: `Home Feed Ranking Refresh`
   - **Product Surface / Environment**: `Home Feed`
4. Click **"Create Project"**

**Expected Result:**
- ✅ Project created: "Home Feed Ranking Refresh"
- ✅ Product Surface: "Home Feed"
- ✅ API Key generated
- ✅ Tracking Code displayed

**Why This Matters:**
- Shows you understand projects as product initiatives, not just infrastructure
- Demonstrates Pinterest DS framing (surface-aware analysis)

---

## Step 3: Create Journey - "Pin Discovery to Save" (2 min)

**What to Say:**
> "The key question is: does this ranking change help or hurt the inspiration journey? I'll track users from Pin View to Save - this captures intent formation, not just clicks."

**Actions:**
1. Click **"Journeys"** in the navbar
2. Click **"Create Journey"** button
3. Fill in:
   - **Journey Name**: `Pin Discovery to Save`
   - **Description**: `Track users from Pin View through planning to Save - measures inspiration quality`
   - **Project**: Select "Home Feed Ranking Refresh"
   - **Stages** (Add 3 stages):
     - Stage 1: Name: `Pin View`, Event Type: `pin_view`, Order: `1`
     - Stage 2: Name: `Save`, Event Type: `save`, Order: `2`
     - Stage 3: Name: `Click`, Event Type: `click`, Order: `3` (optional - for comparison)
4. Click **"Create Journey"**

**Expected Result:**
- ✅ Journey created: "Pin Discovery to Save"
- ✅ 3 stages defined: Pin View → Save → Click
- ✅ Associated with "Home Feed Ranking Refresh" project

**Why This Matters:**
- Shows journey thinking (inspiration → planning → action)
- Measures saves (inspiration quality), not just clicks
- Aligns with Pinterest DS metrics

---

## Step 4: Track Events with Segments (3 min)

**What to Say:**
> "Now I'll simulate tracking events. In real life, these would come from the product. I'm tracking with user intent segments because Pinterest users behave differently - Planners save more, Actors click more."

**Option A: Via Browser Console (Quick Demo)**

Open browser DevTools (F12) → Console tab, run:

```javascript
// Get API Key from Projects page first, then replace YOUR_API_KEY below
const API_KEY = 'YOUR_API_KEY'; // Get from Projects page
const API_URL = 'http://localhost:8000/api/v1/track';

// Helper function to track events
async function trackEvent(event) {
  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY
      },
      body: JSON.stringify(event)
    });
    return response.ok;
  } catch (error) {
    console.error('Error tracking event:', error);
    return false;
  }
}

// Simulate baseline data (Before experiment)
console.log('📊 Tracking baseline events (Before experiment)...');

// Planner users - Save-oriented behavior (high save rate)
for (let i = 1; i <= 100; i++) {
  // Pin View
  await trackEvent({
    event_type: 'pin_view',
    user_id: `planner_baseline_${i}`,
    user_intent: 'Planner',
    surface: 'Home',
    user_tenure: 'Retained',
    content_category: 'home_decor',
    timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString() // 2 days ago
  });
  
  // 60% of Planners save (high save rate - inspiration quality)
  if (i <= 60) {
    await trackEvent({
      event_type: 'save',
      user_id: `planner_baseline_${i}`,
      user_intent: 'Planner',
      surface: 'Home',
      timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString()
    });
  }
  
  // 30% of Planners click (they save for later, click less)
  if (i <= 30) {
    await trackEvent({
      event_type: 'click',
      user_id: `planner_baseline_${i}`,
      user_intent: 'Planner',
      surface: 'Home',
      timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString()
    });
  }
}

// Actor users - Click-oriented behavior (lower save rate, higher click rate)
for (let i = 1; i <= 100; i++) {
  // Pin View
  await trackEvent({
    event_type: 'pin_view',
    user_id: `actor_baseline_${i}`,
    user_intent: 'Actor',
    surface: 'Home',
    user_tenure: 'Retained',
    content_category: 'shopping',
    timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString() // 2 days ago
  });
  
  // 40% of Actors save (lower save rate - they act quickly)
  if (i <= 40) {
    await trackEvent({
      event_type: 'save',
      user_id: `actor_baseline_${i}`,
      user_intent: 'Actor',
      surface: 'Home',
      timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString()
    });
  }
  
  // 50% of Actors click (higher click rate - ready to act)
  if (i <= 50) {
    await trackEvent({
      event_type: 'click',
      user_id: `actor_baseline_${i}`,
      user_intent: 'Actor',
      surface: 'Home',
      timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString()
    });
  }
}

console.log('✅ Baseline events tracked (200 users, 100 saves)');
console.log('📊 Expected: Planner 60% progression, Actor 40% progression');
```

**Option B: Use QUICK_DEMO_SCRIPT.js (Recommended)**

1. Get API Key from Projects page
2. Open `QUICK_DEMO_SCRIPT.js` file
3. Replace `YOUR_API_KEY` with your actual API key
4. Copy the entire script
5. Paste into browser console (F12)
6. Press Enter to run

**Expected Result:**
- ✅ 200 Planner users tracked (100 views, 60 saves, 30 clicks)
- ✅ 100 Actor users tracked (100 views, 40 saves, 50 clicks)
- ✅ Events stored in Parquet files with segment dimensions

**Why This Matters:**
- Shows segmentation at data collection (user_intent)
- Demonstrates heterogeneous user behavior (Planners vs Actors)
- Real Pinterest DS pattern

---

## Step 5: View Journey Analytics - Overall View (2 min)

**What to Say:**
> "Let me check the overall journey metrics first. This gives me the aggregate view before I segment."

**Actions:**
1. Click **"Dashboard"** (Journey Overview)
2. Select **Journey**: "Pin Discovery to Save"
3. Select **Date Range**: Today to Today (or last 7 days if events span multiple days)
4. Leave segment filters empty (aggregate view)
5. Click to refresh/view analytics

**Expected Result:**
- ✅ **Users Exposed**: 200 (100 Planners + 100 Actors who viewed pins)
- ✅ **Advanced Users**: 100 (60 Planners + 40 Actors who saved)
- ✅ **Progression Rate**: 50% (100/200)
- ✅ Journey visualization shows stages
- ✅ Stage details table shows metrics

**What to Say:**
> "Overall, we have a 50% progression rate from Pin View to Save. But this aggregate hides important differences - let me break it down by user intent to see heterogeneous effects."

**Why This Matters:**
- Shows you don't just look at aggregate metrics
- Demonstrates thinking about segment-level differences
- Classic Pinterest DS approach

---

## Step 6: Segment Analysis - Break Down by User Intent (3 min)

**What to Say:**
> "Pinterest users have different intent - Planners save for later, Actors act quickly. I need to see how this ranking change affects each segment differently. This is critical for Pinterest because we can't optimize for clicks at the expense of saves."

**Actions:**
1. On **Journey Overview** page
2. Select **Journey**: "Pin Discovery to Save"
3. **Break Down By**: Select "User Intent"
4. View segment comparison

**Expected Result:**
- ✅ **Segment Comparison Table** shows:
  - **Planner**: 100 users exposed, 60 advanced, 60% progression rate
  - **Actor**: 100 users exposed, 40 advanced, 40% progression rate
- ✅ **Per-Segment Journey Visualization**:
  - Planner segment: Higher progression (60% save rate)
  - Actor segment: Lower progression (40% save rate)
- ✅ **Total Summary**: Shows aggregate across segments

**What to Say:**
> "Here's the key insight: Planners show 60% progression from Pin View to Save, while Actors show 40%. This makes sense - Planners are saving content for planning, Actors are ready to act immediately. 

> **The critical question**: If our ranking change improves clicks but hurts saves, which segment is affected? If Planners are harmed, we risk degrading inspiration quality - Pinterest's core value."

**Why This Matters:**
- Shows heterogeneous effect analysis (core Pinterest DS skill)
- Demonstrates understanding of segment behavior differences
- Connects metrics to product value (inspiration quality)

---

## Step 7: Simulate Experiment - Before vs After (2 min)

**What to Say:**
> "Now let's simulate an experiment. The new ranking algorithm increases clicks by 12% but reduces saves by 20%. Let me track this scenario."

**Track "After" Scenario Events:**

```javascript
// Simulate NEW ranking (click-optimized, save-reduced)
// Run this in browser console after baseline events

console.log('🧪 Tracking experiment events (After - Treatment)...');

// Planner users - HARMED by click-optimized ranking (save rate drops)
for (let i = 1; i <= 100; i++) {
  await trackEvent({
    event_type: 'pin_view',
    user_id: `planner_exp_${i}`,
    user_intent: 'Planner',
    surface: 'Home',
    user_tenure: 'Retained',
    content_category: 'home_decor',
    experiment_id: 'ranking_exp_001',
    variant: 'treatment',
    timestamp: new Date().toISOString() // Today
  });
  
  // Only 40% save now (DOWN from 60% - HARMED by click optimization)
  if (i <= 40) {
    await trackEvent({
      event_type: 'save',
      user_id: `planner_exp_${i}`,
      user_intent: 'Planner',
      experiment_id: 'ranking_exp_001',
      variant: 'treatment',
      timestamp: new Date().toISOString()
    });
  }
  
  // Click rate increases (but saves decrease - tradeoff)
  if (i <= 45) {
    await trackEvent({
      event_type: 'click',
      user_id: `planner_exp_${i}`,
      user_intent: 'Planner',
      experiment_id: 'ranking_exp_001',
      variant: 'treatment',
      timestamp: new Date().toISOString()
    });
  }
}

// Actor users - BENEFITED by click-optimized ranking (click rate increases)
for (let i = 1; i <= 100; i++) {
  await trackEvent({
    event_type: 'pin_view',
    user_id: `actor_exp_${i}`,
    user_intent: 'Actor',
    surface: 'Home',
    user_tenure: 'Retained',
    content_category: 'shopping',
    experiment_id: 'ranking_exp_001',
    variant: 'treatment',
    timestamp: new Date().toISOString() // Today
  });
  
  // Save rate stays at 40% (stable)
  if (i <= 40) {
    await trackEvent({
      event_type: 'save',
      user_id: `actor_exp_${i}`,
      user_intent: 'Actor',
      experiment_id: 'ranking_exp_001',
      variant: 'treatment',
      timestamp: new Date().toISOString()
    });
  }
  
  // Click rate increases to 70% (UP from 50% - BENEFITED)
  if (i <= 70) {
    await trackEvent({
      event_type: 'click',
      user_id: `actor_exp_${i}`,
      user_intent: 'Actor',
      experiment_id: 'ranking_exp_001',
      variant: 'treatment',
      timestamp: new Date().toISOString()
    });
  }
}

console.log('✅ Experiment events tracked (200 users, 80 saves)');
console.log('📊 Expected: Planner 40% progression (↓20%), Actor 40% progression (stable)');
console.log('🚨 Key Insight: Planners HARMED, Actors BENEFITED - Segment imbalance detected!');
```

**Expected Result:**
- ✅ New events tracked with `experiment_id: 'ranking_exp_001'` and `variant: 'treatment'`
- ✅ Planner save rate: 40% (down from 60%) - **HARMED**
- ✅ Actor click rate: 70% (up from 50%) - **BENEFITED**

**Why This Matters:**
- Simulates realistic experiment scenario
- Shows heterogeneous effects (different segments affected differently)
- Demonstrates tradeoff (clicks up, saves down)

---

## Step 8: Analyze Tradeoffs - Segment Comparison (3 min)

**What to Say:**
> "Now let me compare the experiment results. I'll filter to the experiment period and break down by user intent to see who wins and who loses."

**Actions:**
1. On **Journey Overview**
2. Select **Journey**: "Pin Discovery to Save"
3. **Date Range**: Select date range that includes experiment events
4. **Break Down By**: "User Intent"
5. View segment comparison

**Expected Results:**

**Baseline (Before Experiment):**
- Planner: 60% progression rate
- Actor: 40% progression rate

**Experiment (After - Treatment):**
- Planner: 40% progression rate (**↓ 20% - HARMED**)
- Actor: 40% progression rate (stable)

**What to Say:**
> "Here's the critical finding: The ranking change **reduces Planner progression by 20%** (from 60% to 40%), while Actor progression stays the same. 

> **This is a red flag for Pinterest**. Planners represent users who are forming intent over time - they're saving content for planning. If we optimize for clicks and hurt saves, we're degrading inspiration quality - Pinterest's core value proposition.

> Let me check the guardrails to see the full picture."

**Why This Matters:**
- Shows tradeoff analysis (core Pinterest DS skill)
- Demonstrates segment-level impact understanding
- Connects to product value (inspiration quality)

---

## Step 9: Guardrail Check (2 min)

**What to Say:**
> "Before making a decision, I need to check guardrails. Pinterest doesn't just optimize for clicks - we need to ensure we're not harming long-term value."

**Actions (Explain Guardrails):**

1. **Content Diversity** (Manual check):
   - "I would check if the new ranking narrows content shown"
   - "Are we showing fewer creators/categories?"

2. **Save-to-Impression Ratio** (Calculate):
   - "Baseline: 50 saves / 100 impressions = 50%"
   - "Experiment: 40 saves / 100 impressions = 40%"
   - "**↓ 10 percentage points - inspiration quality declining**"

3. **Session Depth** (Explain):
   - "Are users exploring less? (Would need additional tracking)"
   - "Less exploration = less discovery = harm to Pinterest model"

4. **Segment Imbalance** (Already visible):
   - "Planners harmed, Actors stable - **segment imbalance detected**"

**What to Say:**
> "The guardrails tell a clear story:
> - Save-to-impression ratio declined (inspiration quality down)
> - Segment imbalance (Planners harmed, Actors unaffected)
> - This suggests we're optimizing for clicks at the expense of saves

> **This is exactly the kind of tradeoff Pinterest DS needs to catch before shipping.**"

**Why This Matters:**
- Shows guardrail thinking (preventing harmful optimization)
- Demonstrates multi-metric evaluation
- Shows senior judgment

---

## Step 10: Decision & Recommendation (2 min)

**What to Say:**
> "Based on this analysis, here's my recommendation."

**Decision Framework:**

### ❌ **Reject Global Rollout**

**Reasoning:**
1. **Planner segment harmed**: 20% reduction in save progression
2. **Inspiration quality declining**: Save-to-impression ratio down 10%
3. **Segment imbalance**: One segment benefits, another is harmed
4. **Long-term risk**: Optimizing for clicks may harm Pinterest's core value (inspiration)

### ✅ **Recommended Next Steps**

1. **Ship Segment-Specific Ranking**:
   - Use click-optimized ranking for Actor segments (they benefit, less save impact)
   - Keep save-oriented ranking for Planner segments (preserve inspiration quality)
   - A/B test segment-specific ranking

2. **Monitor Guardrails**:
   - Track save rates for Planner segments (target: maintain >55%)
   - Monitor content diversity (target: no reduction)
   - Track session depth (target: no reduction)

3. **Iterate**:
   - If segment-specific ranking works, consider expanding
   - If Planner segments still harmed, rollback entirely
   - Test alternative ranking strategies that preserve saves

**What to Say:**
> "This decision demonstrates Pinterest DS thinking:
> - We measure beyond clicks (saves, inspiration quality)
> - We evaluate heterogeneous segment effects
> - We check guardrails before shipping
> - We recommend segment-specific solutions, not one-size-fits-all

> This is exactly how Pinterest DS prevents harmful over-optimization and protects long-term user value."

**Why This Matters:**
- Shows decision-making with guardrails
- Demonstrates segment-specific recommendations
- Shows long-term thinking
- Perfect Pinterest DS demonstration

---

## 🎯 Demo Summary

**What You Demonstrated:**
1. ✅ **Project as Product Initiative** - "Home Feed Ranking Refresh"
2. ✅ **Journey Thinking** - Inspiration-to-action (Pin View → Save)
3. ✅ **Segment Tracking** - User intent (Planner vs Actor)
4. ✅ **Heterogeneous Effect Analysis** - Different segments affected differently
5. ✅ **Tradeoff Evaluation** - Clicks up, saves down
6. ✅ **Guardrail Checking** - Save ratios, segment balance
7. ✅ **Decision-Making** - Ship/Segment/Rollback with reasoning
8. ✅ **Pinterest DS Framing** - Inspiration quality, long-term value

**Key Metrics Shown:**
- Progression Rate (not conversion rate)
- Users Exposed (not total users)
- Advanced Users (not completed users)
- Natural Attrition (not drop-off)
- Segment Comparison (heterogeneous effects)

**Key Decisions Enabled:**
- ❌ Reject global rollout (harmful tradeoff)
- ✅ Ship segment-specific solution (preserve inspiration quality)
- ✅ Monitor guardrails (prevent future harm)

---

## 💡 Talking Points for Interview

**Throughout the demo, emphasize:**

1. **"This is not just about clicks"** - Pinterest values inspiration quality (saves, planning)
2. **"Segments matter"** - Planners and Actors have different behaviors and needs
3. **"Guardrails prevent harm"** - We check save ratios, content diversity, session depth
4. **"Tradeoffs are explicit"** - We don't hide that clicks are up but saves are down
5. **"Decisions are data-driven"** - We recommend segment-specific solutions based on data

**This demonstrates:**
- ✅ Understanding of Pinterest business model
- ✅ Advanced analytical thinking (heterogeneous effects)
- ✅ Product judgment (guardrails, tradeoffs)
- ✅ Communication (clear recommendations)
- ✅ Technical skills (tool usage, data analysis)

---

## ⚡ Quick Demo Script (5-Minute Version)

If short on time, focus on:

1. **Create Project** (30 sec): "Home Feed Ranking Refresh" → Surface: "Home Feed"
2. **Create Journey** (30 sec): "Pin Discovery to Save" with 2 stages
3. **Track Events** (1 min): Use browser console script to track Planner/Actor events
4. **Segment Analysis** (2 min): Break down by User Intent, show Planner 60% vs Actor 40%
5. **Decision** (1 min): "Planners show higher progression - protect their experience. Recommend segment-specific ranking."

**Key Message**: "This tool helps Pinterest DS evaluate experiments by segment, check guardrails, and make data-driven decisions that preserve inspiration quality."

---

## 🎓 Preparation Tips

1. **Practice the script** - Know what to say at each step
2. **Prepare example data** - Have the tracking scripts ready
3. **Explain the "why"** - Don't just click buttons, explain Pinterest DS reasoning
4. **Emphasize tradeoffs** - Show you understand it's not just about optimizing clicks
5. **Connect to product** - Link metrics to Pinterest's core value (inspiration)

---

## 📝 Notes for Smooth Demo

**Common Questions & Answers:**

**Q: "Why Parquet files instead of a database?"**
A: "For this POC, Parquet provides efficient columnar storage for analytics workloads. DuckDB can query Parquet files directly with SQL, making it perfect for analytical queries without needing a traditional database setup."

**Q: "How would this scale in production?"**
A: "In production, we'd move to a proper data warehouse (BigQuery, Snowflake) or a distributed system. This POC demonstrates the analytics logic and segment-aware querying that would transfer to a production system."

**Q: "What about real-time analytics?"**
A: "The current implementation uses buffered writes for efficiency. For real-time, we'd add streaming (Kafka) and potentially use ClickHouse or similar for sub-second query performance."

**Q: "How do you handle experiment assignment?"**
A: "Currently, experiment_id and variant are tracked in events. In production, this would integrate with an experiment framework (Pinterest's internal system) for proper randomization and assignment tracking."

---

**Status**: Ready to demo! 🎬

This demo showcases:
- Pinterest DS thinking
- Advanced analytics (segmentation, tradeoffs)
- Product judgment (guardrails, decisions)
- Technical skills (tool usage)

**Perfect for Pinterest DS interview!** 🎯
