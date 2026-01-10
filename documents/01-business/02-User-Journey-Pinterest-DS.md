# User Journey: Inspiration-to-Action Funnel Analyzer (IAFA)

## Primary User: Product Data Scientist (Pinterest DS)
**Secondary Consumers:** PMs, Engineers (via summaries)

---

## 🎯 High-Level Journey (TL;DR)

**A DS notices a product question → explores user behavior → evaluates a change → uncovers tradeoffs → recommends next action.**

That's the whole loop.

---

## Step-by-Step User Journey

### 1️⃣ Entry Point: A Product Question Appears

**Trigger:** The DS starts with a real product question, not data curiosity.

**Example Questions:**
- "Saves are up, but outbound clicks are flat — why?"
- "Does increasing feed diversity hurt intent?"
- "Which users actually convert inspiration into action?"

**DS Action:** Opens IAFA to investigate.

**Current State:** ✅ Can create projects and funnels
**Need:** Entry point that prompts for product question

---

### 2️⃣ Funnel Overview: "What's happening right now?"

**What the DS sees:**
- A funnel dashboard showing:
  - Impressions → Close-ups → Saves → Clicks → Action proxy
  - Overall conversion rates
  - Trend lines over time

**What this answers:**
- Where is the biggest drop-off?
- Is this a top-of-funnel or bottom-funnel issue?

**Key Insight:** 📌 This mirrors how Pinterest DS thinks: start broad, then zoom.

**Current State:** ✅ Basic funnel visualization exists
**Need:** 
- Better funnel visualization with drop-off rates
- Time-series trends
- Stage-by-stage breakdown

---

### 3️⃣ Segment Exploration: "Who is affected?"

**The DS slices the funnel by:**
- **User intent segment:**
  - Browser (exploring, discovering)
  - Planner (saving for later, organizing)
  - Actor (ready to act, converting)
  - Curator (sharing, creating)
- **Content category** (e.g., home decor, recipes, travel)
- **Surface** (Home Feed, Search, Boards, Profile)
- **User tenure** (New users vs Retained users)

**What the DS learns:**
- Browsers save more but rarely click
- Planners save a lot but act later
- Actors convert quickly but are sensitive to diversity changes

**Key Insight:** 📌 Pinterest DS work is all about heterogeneous effects.

**Current State:** ❌ No segmentation yet
**Need:**
- Add segment dimensions to events
- Segment filtering in analytics
- Segment comparison view

---

### 4️⃣ Instrumentation Check: "Are we measuring the right things?"

**The DS reviews:**
- Event coverage (what's logged vs missing)
- Metric definitions
- Data quality checks

**Outcome:**
- Identifies missing signals (e.g., time-to-save, repeated saves)
- Recommends instrumentation improvements

**Key Insight:** 📌 This aligns with "develop best practices for instrumentation."

**Current State:** ❌ No instrumentation check
**Need:**
- Event coverage dashboard
- Metric definition documentation
- Data quality indicators
- Missing event detection

---

### 5️⃣ Experiment View: "What changed?"

**The DS selects a product change or experiment:**
- Increased feed diversity
- Re-ranking by freshness
- UI tweak to save button

**The tool shows:**
- Pre/post metrics
- Control vs treatment (if applicable)
- CUPED / diff-in-diff adjusted effects

**Key Insight:** 📌 This is classic Pinterest DS experimentation work.

**Current State:** ❌ No experiment tracking
**Need:**
- Experiment tagging (experiment_id, variant)
- Pre/post comparison
- Control/treatment analysis
- Statistical significance testing

---

### 6️⃣ Tradeoff Analysis: "Who wins, who loses?"

**This is the most important step.**

**The DS sees:**
- Saves ↑ for planners
- Clicks ↓ for actors
- Diversity ↑ but session depth ↓ slightly

**The DS answers:**
- Is this an acceptable tradeoff?
- Should we segment the experience?
- Is this worth rolling out globally?

**Key Insight:** 📌 Pinterest explicitly values tradeoff-aware decisions.

**Current State:** ❌ No tradeoff analysis
**Need:**
- Segment-level impact comparison
- Win/loss visualization
- Tradeoff matrix
- Recommendation framework

---

### 7️⃣ Insight Synthesis: "So what?"

**The tool generates:**
- Key findings
- Segment-level impacts
- Confidence / uncertainty notes

**The DS adds context:**
- "This aligns with previous experiments…"
- "We should protect actors while improving planners…"

**Key Insight:** 📌 This is where judgment matters.

**Current State:** ❌ No insight synthesis
**Need:**
- Automated insights generation
- Key findings summary
- Context notes
- Confidence indicators

---

### 8️⃣ Recommendation Output: "What should we do next?"

**The DS produces a PM-ready summary:**
- Recommendation (e.g., segment-aware ranking)
- Next experiment proposal
- Metrics to watch
- Guardrails

**Output formats:**
- Markdown summary
- Slide-ready 1-pager
- Shared doc

**Key Insight:** 📌 The output is a decision, not a model.

**Current State:** ❌ No recommendation output
**Need:**
- Export functionality (Markdown, PDF)
- Recommendation template
- Metrics watchlist
- Guardrails definition

---

## End State: What changes because of this tool?

✅ PMs understand why a change worked or failed
✅ Experiments are better designed
✅ Metrics are clearer
✅ Tradeoffs are explicit
✅ DS work directly influences product direction

---

## Why This Journey is PERFECT for Pinterest DS

**Because it shows you can:**
1. ✅ Start from a product question
2. ✅ Reason about user behavior
3. ✅ Design metrics and experiments
4. ✅ Handle ambiguity
5. ✅ Communicate insights clearly
6. ✅ Influence decisions

**That's literally the job.**

---

## One-Sentence Journey Summary

> "The tool helps a product data scientist move from a product question, to funnel and segment analysis, to rigorous experiment evaluation, and finally to clear product recommendations that balance inspiration, intent, and action."

---

## Implementation Roadmap

### Phase 1: Foundation (Current) ✅
- Event tracking
- Funnel definition
- Basic analytics
- Parquet storage

### Phase 2: Segmentation (Next)
- User intent segments
- Segment filtering
- Segment comparison

### Phase 3: Experimentation
- Experiment tagging
- Pre/post analysis
- Control/treatment comparison

### Phase 4: Tradeoffs & Insights
- Tradeoff analysis
- Insight generation
- Recommendation output

---

## User Personas

### Primary: Product Data Scientist
- **Goal:** Answer product questions with data
- **Needs:** Fast iteration, segment insights, experiment evaluation
- **Pain Points:** Too many tools, slow queries, unclear tradeoffs

### Secondary: Product Manager
- **Goal:** Understand impact of changes
- **Needs:** Clear recommendations, tradeoff summaries
- **Pain Points:** Complex analysis, unclear implications

### Tertiary: Engineer
- **Goal:** Implement recommendations
- **Needs:** Clear guardrails, metric definitions
- **Pain Points:** Unclear requirements, missing instrumentation

---

## Success Metrics

**For the Tool:**
- Time from question to insight: < 30 minutes
- Ability to segment by user intent: Yes
- Experiment evaluation capability: Yes
- Tradeoff visibility: Yes

**For the DS:**
- Product questions answered: 10+/week
- Recommendations implemented: 50%+
- Experiments improved: Yes
- PM satisfaction: High

---

## Technical Requirements (From Journey)

1. **Fast Queries** → DuckDB on Parquet ✅
2. **Segment Filtering** → Multi-dimensional events
3. **Experiment Tracking** → Experiment metadata
4. **Time-Series Analysis** → Date partitioning
5. **Export Functionality** → Markdown/PDF generation

---

**Status:** Journey defined, ready for implementation
**Next:** Implement features to support each step
