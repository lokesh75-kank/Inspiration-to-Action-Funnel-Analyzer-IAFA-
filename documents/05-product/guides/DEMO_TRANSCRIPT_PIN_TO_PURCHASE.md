# Demo Transcript: Pin to Purchase Journey

**Duration:** 2-3 minutes  
**Audience:** Product Data Scientists, Hiring Managers, Product Teams

---

## Opening (15 seconds)

"Hi, I'm going to show you IAFA — a tool I built to analyze inspiration-to-action journeys, inspired by how Pinterest thinks about user behavior.

Today I'll walk through a **Pin to Purchase** journey — tracking how users move from discovering a pin, to saving it, clicking through, and ultimately making a purchase."

---

## Step 1: Journey Overview (30 seconds)

*[Navigate to Dashboard, select "Pin to Purchase" journey]*

"Here's our Pin to Purchase journey with four stages:
- **Pin View** — users discover content
- **Save** — they save it for later
- **Click** — they click through to the website
- **Purchase** — they complete a purchase

Right away, I can see our overall progression rate is about **X%** — meaning X% of users who view a pin eventually purchase. But that's not the full story."

---

## Step 2: Segment Analysis (45 seconds)

*[Click on Segment Breakdown, select "User Intent"]*

"Let me break this down by user intent. This is where it gets interesting.

**Planners** — users who save pins — have a progression rate of **X%**. They're browsing, planning, not ready to buy yet.

**Actors** — users who click immediately — have a progression rate of **Y%**. They're ready to act now.

This tells me: if I optimize only for clicks, I might hurt the Planner segment. That's a tradeoff I need to understand."

*[Switch to "User Tenure" breakdown]*

"Now look at user tenure. **New users** convert at **X%**, while **Retained users** convert at **Y%**.

This suggests our onboarding might need work, or new users need more time to build trust before purchasing."

---

## Step 3: Identifying Bottlenecks (30 seconds)

*[Point to funnel visualization]*

"Looking at the funnel, I see the biggest drop-off is at the **Save stage** — about **49%** of users drop off here.

But here's the key question: Is that bad? For Planners, saving IS the goal. For Actors, it's a friction point.

This is why segment analysis matters. A global optimization might hurt one group to help another."

---

## Step 4: AI-Powered Insights (45 seconds)

*[Scroll to AI Insights panel]*

"Now let's see what AI recommends. The system analyzed our data and suggests:

**Key Insight:** 'Save stage has 49% drop-off, but Planners have 3x higher progression rate than Actors.'

**Recommendation:** 'Test save button placement → Expected impact: +15% save rate for Planners'

**Guardrail:** 'Monitor click rate — don't let save optimization hurt click-through for Actors'

**Experiment:** 'A/B test: Control uses current save placement, Treatment uses optimized placement. Primary metric: Save rate. Secondary: Click rate.'

This gives me a clear hypothesis to test, with guardrails to prevent negative impacts."

---

## Step 5: Decision & Next Steps (30 seconds)

*[Click Export Report, select "Executive" audience]*

"Based on this analysis, here's what I'd recommend:

1. **Don't optimize globally** — segment by user intent
2. **Test save optimization** — but monitor click rates as a guardrail
3. **Focus on new user onboarding** — they're converting lower than retained users

I can export this as a report for leadership, with audience-specific formatting — executive summary, technical deep-dive, or product manager action items."

---

## Closing (15 seconds)

"This tool helps me answer the question: **Are we optimizing for short-term clicks at the cost of long-term user trust?**

By measuring progression, not just conversion, and understanding segment differences, I can make recommendations that balance immediate metrics with long-term retention.

That's IAFA — measuring what matters, not just what's easy to track."

---

## Key Talking Points to Emphasize

✅ **Progression vs Conversion** — measuring the full journey, not just final step  
✅ **Segment Analysis** — understanding tradeoffs between user groups  
✅ **Guardrails** — preventing negative impacts  
✅ **Actionable Insights** — clear recommendations with expected impact  
✅ **Decision Support** — enabling product teams to make informed choices  

---

## Tips for Delivery

- **Pause at insights** — let the data speak, don't rush
- **Ask rhetorical questions** — "Is 49% drop-off bad? It depends..."
- **Show tradeoffs** — "If I optimize for X, what happens to Y?"
- **Connect to business** — "This helps us balance short-term metrics with retention"
- **Be humble** — "I'm exploring this problem, curious to hear your thoughts"

---

## If Asked Technical Questions

**"What's the tech stack?"**
"I used React for the frontend, FastAPI for the backend, and DuckDB for analytics. But honestly, the interesting part isn't the tech — it's how we think about measuring user journeys."

**"How do you handle data?"**
"For this demo, I'm using pre-populated Pinterest event data stored in Parquet files. Events are queried on-demand when you select a date range — it's not real-time streaming, but it's efficient for analytics queries."

**"Is this real-time?"**
"No, it's not real-time. The tool queries stored event data from Parquet files based on your selected date range. This is intentional — for analytics and decision-making, you typically want to analyze historical data over time periods, not stream individual events. Real-time streaming would be better for monitoring dashboards, but for funnel analysis, batch queries are more appropriate."

---

## If Asked About Limitations

**"What can't it do?"**
"It's focused on observational analytics — understanding what's happening. For causal inference, you'd still need A/B tests. But it helps you design better experiments."

**"How do you handle attribution?"**
"Right now, it's session-based. For multi-touch attribution, you'd need additional logic, but the framework supports it."

---

**Total Demo Time:** ~3 minutes (can be shortened to 2 minutes by skipping some segment breakdowns)
