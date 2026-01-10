# 🎯 IAFA User Guide - How to Use the Tool

**Inspiration-to-Action Funnel Analyzer (IAFA)** - Complete User Guide

---

## 🧠 Why IAFA Exists (Pinterest Context)

Pinterest is an inspiration-first platform where users move from discovery to planning to action over time. Traditional conversion metrics alone fail to capture this journey and can lead to over-optimization that harms long-term user trust, content diversity, and creator health.

IAFA is designed to help Product Data Scientists:
- **Measure inspiration quality beyond clicks** - Track saves, planning behavior, and long-term engagement
- **Understand how intent forms across user segments** - See how Browser, Planner, Actor, and Curator segments behave differently
- **Evaluate tradeoffs between discovery, diversity, and downstream actions** - Balance short-term clicks with long-term value
- **Design experiments that improve long-term value without degrading user experience** - Prevent harmful over-optimization

**📌 Why this matters:** This tool understands that Pinterest's success comes from helping users form intent over time, not forcing immediate conversions.

---

## 🚀 Quick Start

### 1. Start the Backend

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
✅ Default project already exists: Pinterest
INFO:     Application startup complete.
```

### 2. Start the Frontend

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### 3. Open in Browser

Visit: **http://localhost:5173**

You'll be automatically redirected to the Journey Overview (Dashboard).

---

## 📋 Main Features

### 1. **Projects** - Manage Product Initiatives & Experiment Scope

**What is a "Project" in Pinterest DS terms:**
- **A product initiative** (e.g., "Home Feed Ranking Refresh", "Search Relevance Update")
- **A surface-specific analysis** (e.g., "Shopping Surface Experiment", "Boards Engagement Analysis")
- **An experiment scope** (e.g., "Creator Tools A/B Test", "Recommendation System Update")

**View Projects:**
- Navigate to **Projects** page (click "Projects" in navbar)
- You'll see the default "Pinterest" project (created automatically with Product Surface: "Home Feed")
- Click on a project to see details (API Key, Tracking Code)

**Create New Project:**
1. Click "Create Project" button
2. Enter:
   - **Project Name** (required): Name your product initiative, experiment scope, or surface-specific analysis
     - Examples: `Home Feed Ranking Refresh`, `Search Relevance Update`, `Shopping Surface Experiment`, `Creator Tools A/B Test`, `Boards Engagement Analysis`
     - Think of this as: "What product work am I analyzing?"
   - **Product Surface / Environment** (optional): Identifies the product surface or environment generating events
     - Examples: `Home Feed`, `Search`, `Boards`, `Ads Manager`, `Shopping`, `Profile`
     - This helps organize analysis by where events occur in your product
     - Think of this as: "Which surface/environment is this for?"
3. Click "Create Project"
4. Your new project is created with an API Key

**Example Projects (Pinterest DS Style):**
- **Product Initiative**: "Home Feed Ranking Refresh" → Surface: "Home Feed"
- **Experiment Scope**: "Search Relevance Update" → Surface: "Search"
- **Surface Analysis**: "Shopping Surface Experiment" → Surface: "Shopping"
- **Feature Analysis**: "Boards Engagement Analysis" → Surface: "Boards"

**View Project Details:**
- Click on a project to expand it
- See the **API Key** (used for tracking events)
- See the **Product Surface** (where events occur)
- See the **Tracking Code** (JavaScript snippet to embed)

---

### 2. **Journeys** - Define Your Inspiration-to-Action Journeys

**Create a Journey:**
1. Navigate to **Journeys** page (formerly "Funnels")
2. Click "Create Journey"
3. Fill in:
   - **Journey Name**: e.g., "Pin Discovery to Action", "Save-to-Click Journey", "Shopping Inspiration Flow"
   - **Description** (optional): e.g., "Track users from Pin View through planning to action"
   - **Project**: Select your project (e.g., "Home Feed Ranking Refresh", "Search Relevance Update", "Shopping Surface Experiment")
     - Projects represent product initiatives or experiment scope
   - **Stages**: Define up to 5 stages representing the inspiration-to-action journey
     - For each stage:
       - **Stage Name**: e.g., "Pin View", "Save", "Click", "Purchase"
       - **Event Type**: e.g., "pin_view", "save", "click", "purchase"
       - **Order**: 1, 2, 3, 4, 5 (represents progression: discovery → planning → action)
4. Click "Create Journey"

**Example Journey:**
```
Stage 1: Pin View (event_type: "pin_view", order: 1) - Discovery/Inspiration
Stage 2: Save (event_type: "save", order: 2) - Planning/Intent Formation
Stage 3: Click (event_type: "click", order: 3) - Action Initiation
Stage 4: Add to Cart (event_type: "add_to_cart", order: 4) - Purchase Intent
Stage 5: Purchase (event_type: "purchase", order: 5) - Action Completion
```

**View Journeys:**
- All your journeys are listed on the Journeys page
- Click on a journey to see details
- Edit or delete journeys as needed

---

### 3. **Journey Overview** (Dashboard) - View Analytics

**View Journey Analytics:**
1. Navigate to **Journey Overview** (Dashboard)
2. **Select Journey**: Choose a journey from the dropdown
3. **Select Date Range**: Choose start and end dates
4. View analytics:
   - **Summary Cards**: Users Exposed, Advanced Users, Progression Rate
   - **Journey Visualization**: Visual journey with stages and progression rates
   - **Stage Details Table**: Detailed metrics for each stage showing natural attrition patterns

**Segment Filters (Phase 2 - Pinterest DS Features):**
1. **User Intent**: Filter by user intent segment
   - Browser (exploring, discovering)
   - Planner (saving for later)
   - Actor (ready to act, converting)
   - Curator (sharing, creating)
2. **Surface**: Filter by surface
   - Home (Home feed)
   - Search (Search results)
   - Boards (User boards)
   - Profile (User profile)
3. **User Tenure**: Filter by user tenure
   - New (New users)
   - Retained (Existing users)
4. **Content Category**: Filter by content category (e.g., home_decor, recipes, travel)
5. **Break Down By**: Compare segments side-by-side
   - Select dimension: User Intent, Surface, User Tenure, or Content Category
   - See segment comparison table

**Example Use Case:**
- **Question**: "Which user intent segments progress best from Pin View to Save?"
- **Steps**:
  1. Select journey: "Pin Discovery to Save"
  2. Select date range: Last 30 days
  3. Break down by: "User Intent"
  4. **Result**: See progression rates for Browser, Planner, Actor, Curator
  5. **Decision Enabled**: 
     - If Planners show high progression, prioritize save-oriented content for this segment
     - If Actors show low progression but high downstream actions, preserve click-optimized experience
     - Avoid global changes that might improve one segment at the expense of another

---

## 🧪 Experiment Lifecycle Supported by IAFA

IAFA supports the complete experiment lifecycle for Product Data Scientists:

1. **Define Hypothesis and Success Metrics**
   - Create journeys that capture the full inspiration-to-action path
   - Define segment-specific success metrics (e.g., progression rate by user intent)

2. **Validate Instrumentation and Guardrails**
   - Ensure event tracking covers all journey stages
   - Set up guardrails to monitor content diversity, session depth, and segment balance

3. **Measure Heterogeneous Segment Effects**
   - Break down results by user intent, surface, tenure, and category
   - Identify which segments benefit or are harmed by changes

4. **Evaluate Tradeoffs Across Inspiration and Action**
   - Compare saves vs clicks across segments
   - Identify if short-term gains come at the cost of long-term user trust

5. **Recommend Ship / Segment / Rollback Decisions**
   - Use segment comparison to recommend targeted rollouts
   - Flag experiments that show harmful tradeoffs

---

## 🛡️ Guardrails & Long-Term Health Metrics

IAFA tracks not only progression metrics, but also **guardrails to prevent over-optimization**:

- **Content Diversity**: Monitor creator & category concentration to ensure we don't over-optimize for narrow content
- **Save-to-Impression Ratio**: Track inspiration health (are users finding valuable content to save, or just clicking?)
- **Session Depth**: Ensure changes don't reduce exploration and discovery behavior
- **Segment Imbalance**: Identify when one intent group (e.g., Actors) benefits at the expense of others (e.g., Planners)

These guardrails help identify experiments that improve short-term clicks but risk long-term user trust and ecosystem health.

**Example Guardrail Alert:**
- Experiment increases clicks by 12% but reduces saves by 20%
- Save decline is concentrated in Planner segment
- Content diversity decreases in Home feed
- **Decision**: Reject global rollout; propose segment-specific ranking

---

## 📊 Appendix: Event Tracking & Instrumentation

### 4. **Track Events** - Collect User Data

**Track Events via API:**

**Single Event:**
```bash
curl -X POST http://localhost:8000/api/v1/track \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "event_type": "pin_view",
    "user_id": "user123",
    "session_id": "sess456",
    "user_intent": "Planner",
    "surface": "Home",
    "user_tenure": "Retained",
    "content_category": "home_decor",
    "properties": {
      "pin_id": "pin789",
      "category": "home_decor"
    }
  }'
```

**Batch Events:**
```bash
curl -X POST http://localhost:8000/api/v1/track/batch \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "events": [
      {
        "event_type": "pin_view",
        "user_id": "user123",
        "user_intent": "Planner",
        "surface": "Home"
      },
      {
        "event_type": "save",
        "user_id": "user123",
        "user_intent": "Planner",
        "surface": "Home"
      }
    ]
  }'
```

**Track Events via JavaScript (Embed Tracking Code):**

1. Go to **Projects** page
2. Click on your project
3. Copy the **Tracking Code** snippet
4. Embed it in your website/application

Example tracking code:
```javascript
<script>
  // Replace YOUR_API_KEY with your actual API key
  const API_KEY = 'YOUR_API_KEY';
  const API_URL = 'http://localhost:8000/api/v1/track';
  
  function trackEvent(eventType, userId, properties = {}) {
    fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY
      },
      body: JSON.stringify({
        event_type: eventType,
        user_id: userId,
        session_id: getSessionId(),
        properties: properties,
        // Segment dimensions (Phase 2)
        user_intent: getUserIntent(), // e.g., "Planner"
        surface: getSurface(), // e.g., "Home"
        user_tenure: getUserTenure(), // e.g., "Retained"
        content_category: getContentCategory(), // e.g., "home_decor"
        timestamp: new Date().toISOString()
      })
    });
  }
  
  // Track a Pin View
  trackEvent('pin_view', 'user123', {
    pin_id: 'pin789',
    category: 'home_decor'
  });
</script>
```

**Event Schema:**
```typescript
{
  event_type: string;        // Required: e.g., "pin_view", "save", "click"
  user_id: string;           // Required: Unique user identifier
  session_id?: string;       // Optional: Session identifier
  properties?: object;       // Optional: Custom properties
  url?: string;              // Optional: Page URL
  referrer?: string;         // Optional: Referrer URL
  user_agent?: string;       // Optional: User agent string
  timestamp?: string;        // Optional: ISO timestamp (auto-generated if omitted)
  
  // Segment dimensions (Phase 2)
  user_intent?: string;      // Optional: "Browser", "Planner", "Actor", "Curator"
  content_category?: string; // Optional: e.g., "home_decor", "recipes"
  surface?: string;          // Optional: "Home", "Search", "Boards", "Profile"
  user_tenure?: string;      // Optional: "New", "Retained"
  
  // Experiment tracking (Phase 3 - future)
  experiment_id?: string;    // Optional: Experiment identifier
  variant?: string;          // Optional: "control", "treatment"
}
```

---

## 🎯 Common Use Cases

### Use Case 1: Track Pinterest-Style Inspiration Journey

**Scenario**: Track users from Pin View → Save → Click → Purchase for a Home Feed ranking experiment

**Steps:**
1. **Create Project** (if not exists):
   - Name: "Home Feed Ranking Refresh"
   - Product Surface: "Home Feed"

2. **Create Journey**:
   - Name: "Pin Discovery to Action"
   - Project: "Home Feed Ranking Refresh"
   - Stages:
     - Stage 1: Pin View (event_type: "pin_view") - Discovery/Inspiration
     - Stage 2: Save (event_type: "save") - Planning/Intent Formation
     - Stage 3: Click (event_type: "click") - Action Initiation
     - Stage 4: Purchase (event_type: "purchase") - Action Completion

3. **Track Events**:
   ```javascript
   // User views a pin
   trackEvent('pin_view', 'user123', {
     pin_id: 'pin789',
     user_intent: 'Planner',
     surface: 'Home'
   });
   
   // User saves the pin (planning behavior)
   trackEvent('save', 'user123', {
     pin_id: 'pin789',
     user_intent: 'Planner',
     surface: 'Home'
   });
   
   // User clicks through (action initiation)
   trackEvent('click', 'user123', {
     pin_id: 'pin789',
     user_intent: 'Planner'
   });
   
   // User makes purchase (action completion)
   trackEvent('purchase', 'user123', {
     order_id: 'order456',
     amount: 29.99,
     user_intent: 'Actor'
   });
   ```

4. **View Analytics**:
   - Go to Journey Overview
   - Select project: "Home Feed Ranking Refresh"
   - Select journey: "Pin Discovery to Action"
   - Select date range
   - See progression rates and natural attrition patterns

**Decision Enabled:**
- Understand which stages show high natural attrition (expected behavior)
- Identify stages with unexpectedly high drop-offs (opportunities for improvement)
- Segment analysis reveals if changes should be targeted by user intent
- Guardrails ensure we don't optimize for clicks at the expense of saves (inspiration quality)

---

### Use Case 2: Analyze by User Intent Segment

**Scenario**: "Which user intent segments progress best through the inspiration journey?"

**Steps:**
1. Go to **Journey Overview**
2. Select your journey
3. Select date range
4. **Break Down By**: Select "User Intent"
5. **Result**: See progression rates for:
   - Browser: 5% progression (exploring, not ready to act)
   - Planner: 45% progression (saving for later, forming intent)
   - Actor: 15% progression (acts quickly, lower save rate)
   - Curator: 25% progression (sharing content, moderate progression)

**Insight**: "Planners show 3x better progression than Actors because they save more content for planning."

**Decision Enabled:**
- **Ship**: Prioritize save-oriented ranking improvements for Planner segments (high progression, preserve their experience)
- **Segment**: Maintain click-optimized ranking for Actor segments (they act quickly, different behavior pattern)
- **Rollback**: Avoid global ranking changes that optimize for clicks and hurt Planner save rates
- **Guardrail Check**: Monitor that save-to-impression ratio doesn't decline for Planners (inspiration quality)

---

### Use Case 3: Compare Surfaces

**Scenario**: "Which surface enables better inspiration-to-action progression?"

**Steps:**
1. Go to **Journey Overview**
2. Select your journey
3. **Break Down By**: Select "Surface"
4. **Result**: See progression rates for:
   - Home: 20% progression (discovery-focused, lower immediate action)
   - Search: 35% progression (intent-driven, higher action)
   - Boards: 40% progression (saved content, high intent, highest action)
   - Profile: 10% progression (exploration-focused, low action)

**Insight**: "Boards surface shows 2x better progression than Home because users are revisiting saved content with formed intent."

**Decision Enabled:**
- **Ship**: Enhance Board experience features (high-intent users, preserve their planning workflow)
- **Segment**: Maintain Home feed's discovery focus (different use case, don't over-optimize for clicks)
- **Rollback**: Avoid making Home feed too action-oriented (would harm discovery and inspiration)
- **Guardrail Check**: Ensure Home feed maintains content diversity (don't narrow to high-click content only)

---

### Use Case 4: Filter by Multiple Segments

**Scenario**: "How do Retained Planners progress on Home vs Search?"

**Steps:**
1. Go to **Journey Overview**
2. Select your journey
3. **User Intent**: Select "Planner"
4. **User Tenure**: Select "Retained"
5. **Break Down By**: Select "Surface"
6. **Result**: See progression rates for Retained Planners:
   - Home: 50% progression (discovery with planning intent)
   - Search: 60% progression (search with formed intent, higher action)

**Insight**: "Retained Planners show better progression on Search because they're searching with formed intent from previous planning."

**Decision Enabled:**
- **Ship**: Optimize Search experience for Planner segments (they're ready to act)
- **Segment**: Maintain Home feed's inspiration focus for Planners (discovery phase, different journey stage)
- **Rollback**: Don't make Home feed too search-like (would lose discovery value)
- **Guardrail Check**: Monitor session depth (ensure changes don't reduce exploration time)

---

### Use Case 5: Preventing Harmful Over-Optimization (Critical for Pinterest DS)

**Scenario:**
An experiment increases outbound clicks by 12% but reduces saves by 20%. The team is considering a global rollout.

**IAFA Analysis:**
1. Go to **Journey Overview**
2. Select project: "Home Feed Ranking Refresh"
3. Select journey: "Pin Discovery to Action"
4. Compare experiment period vs baseline:
   - **Clicks**: ↑ 12% (looks positive)
   - **Saves**: ↓ 20% (concerning)
5. **Break Down By**: User Intent
   - **Gains driven by**: Actor segments (+18% clicks, -5% saves)
   - **Losses concentrated in**: Planner segments (-2% clicks, -30% saves)
6. **Break Down By**: Surface (Product Surface)
   - **Home Feed**: Significant save decline, reduced content diversity
   - **Search**: Minimal change (less affected)
7. **Guardrail Check**:
   - Content diversity: ↓ 15% (narrower content shown)
   - Save-to-impression ratio: ↓ 25% (inspiration quality declining)
   - Session depth: ↓ 8% (less exploration)

**Decision:**
- **Reject global rollout** - Short-term click gains don't justify long-term inspiration quality loss
- **Propose segmented ranking strategy**:
  - Ship click-optimized ranking for Actor segments (they benefit, less save impact)
  - Rollback for Planner segments (preserve their planning behavior)
  - A/B test segment-specific ranking
- **Monitor guardrails**: Track save rates, content diversity, session depth over 30 days

**Why This Matters:**
This decision prevents a global change that would improve short-term clicks at the expense of Pinterest's core value proposition (inspiration and planning). By segmenting the approach, we preserve the experience for high-value Planner users while still capturing gains for Actor segments.

---

## 📊 Understanding the Analytics

### Summary Cards
- **Users Exposed**: Number of users who entered the journey (Stage 1 - discovery/inspiration)
- **Advanced Users**: Number of users who progressed through the entire journey (last stage - action completion)
- **Overall Progression Rate**: Percentage of users who progressed through the journey (measures intent formation and action)

### Journey Visualization
- Visual representation of your inspiration-to-action journey
- Shows progression rates at each stage (how many users advance)
- Shows natural attrition rates between stages (expected vs concerning drop-offs)
- Width of bars represents progression rate

### Stage Details Table
- **Stage**: Stage name (e.g., Pin View, Save, Click)
- **Users**: Number of users at this stage
- **Progression Rate**: Percentage relative to Stage 1 (how many users reached this stage)
- **Natural Attrition**: Percentage who didn't progress from previous stage (helps identify expected vs concerning patterns)

### Segment Comparison (Phase 2)
- **Segment**: Segment value (e.g., "Planner", "Home", "Retained")
- **Users Exposed**: Users in this segment who entered the journey (Stage 1)
- **Advanced Users**: Users who progressed through the journey in this segment
- **Progression Rate**: Segment-specific progression rate (enables heterogeneous effect analysis)

---

## 🔧 Troubleshooting

### "Failed to fetch projects"
- **Check**: Is backend running on port 8000?
- **Fix**: Start backend: `uvicorn app.main:app --reload --port 8000`

### "Cannot connect to backend"
- **Check**: Are both servers running?
- **Fix**: 
  - Backend: `cd backend && source venv/bin/activate && uvicorn app.main:app --reload --port 8000`
  - Frontend: `cd frontend && npm run dev`

### "No analytics data"
- **Check**: Have you tracked any events?
- **Fix**: Track events using the API or JavaScript tracking code (see Appendix)

### "No journeys found"
- **Check**: Have you created any journeys?
- **Fix**: Go to Journeys page and create a journey

---

## 🎓 Best Practices

1. **Event Naming**: Use consistent, descriptive event names (e.g., `pin_view`, not `view`)
2. **User IDs**: Use persistent user IDs across sessions to track long-term intent formation
3. **Segment Dimensions**: Always include segment dimensions (user_intent, surface, tenure) for heterogeneous effect analysis
4. **Date Ranges**: Use appropriate date ranges (e.g., 7 days for experiments, 30 days for trend analysis)
5. **Journey Stages**: Keep journeys focused (3-5 stages is optimal) representing inspiration → planning → action
6. **Guardrails First**: Always set up guardrails (content diversity, save ratios, session depth) before running experiments
7. **Segment Analysis**: Always break down results by user intent and surface to identify heterogeneous effects
8. **Long-term Value**: Evaluate tradeoffs between short-term clicks and long-term inspiration quality

---

## 📚 Next Steps

1. **Create Your First Journey**: Define your inspiration-to-action journey (3-5 stages)
2. **Set Up Guardrails**: Configure guardrails to monitor content diversity, save ratios, and session depth
3. **Track Events**: Start tracking user events with segment dimensions (user_intent, surface, tenure)
4. **View Analytics**: Check your Journey Overview for insights on progression rates
5. **Segment Analysis**: Use segment filters to understand heterogeneous user behavior
6. **Evaluate Tradeoffs**: Compare short-term action metrics with long-term inspiration quality
7. **Make Decisions**: Use insights to recommend ship/segment/rollback decisions with guardrail context

---

**Status**: Ready to use!  
**Need Help?**: Check `TROUBLESHOOTING.md` for common issues.

---

**Happy Analyzing! 🎉**
