# Funnel Metrics & Definitions

## Core Funnel Metrics

### 1. Users at Stage

**Definition**: The number of unique users who reached a specific funnel stage.

**Calculation**:
```
Users at Stage N = COUNT(DISTINCT user_id)
WHERE user_id has completed stages 1 through N
AND user_id has event_type matching stage N
```

**Example**:
- Stage 1 (Page View): 10,000 users
- Stage 2 (Add to Cart): 3,000 users
- Stage 3 (Purchase): 1,500 users

### 2. Conversion Rate

**Definition**: The percentage of users who reached a stage relative to the first stage.

**Formula**:
```
Conversion Rate (Stage N) = (Users at Stage N / Users at Stage 1) × 100
```

**Example**:
- Stage 1 to Stage 2: (3,000 / 10,000) × 100 = 30%
- Stage 1 to Stage 3: (1,500 / 10,000) × 100 = 15%
- Overall Conversion: 15% (first to last stage)

### 3. Drop-Off Rate

**Definition**: The percentage of users who left the funnel between two consecutive stages.

**Formula**:
```
Drop-Off Rate (Stage N to N+1) = ((Users at Stage N - Users at Stage N+1) / Users at Stage N) × 100
```

**Example**:
- Stage 1 to Stage 2: ((10,000 - 3,000) / 10,000) × 100 = 70%
- Stage 2 to Stage 3: ((3,000 - 1,500) / 3,000) × 100 = 50%

### 4. Completion Rate

**Definition**: The percentage of users who completed the entire funnel.

**Formula**:
```
Completion Rate = (Users at Final Stage / Users at First Stage) × 100
```

**Example**:
- 1,500 users completed purchase out of 10,000 who viewed page
- Completion Rate = (1,500 / 10,000) × 100 = 15%

## Advanced Metrics (Post-MVP)

### 5. Time to Convert

**Definition**: Average time taken for users to progress from first to last stage.

**Calculation**:
```
Time to Convert = AVG(completed_at - started_at)
WHERE user completed entire funnel
```

**Use Case**: Identify bottlenecks where users take too long to convert.

### 6. Stage Duration

**Definition**: Average time users spend at each stage before moving to next.

**Calculation**:
```
Stage Duration (N to N+1) = AVG(event_time_stage_N+1 - event_time_stage_N)
WHERE user completed both stages
```

**Use Case**: Identify stages where users hesitate or drop off.

### 7. Funnel Velocity

**Definition**: Rate at which users progress through funnel stages.

**Formula**:
```
Funnel Velocity = Total Conversions / Total Time Period
```

**Use Case**: Measure overall funnel performance over time.

### 8. Abandonment Rate

**Definition**: Percentage of users who started but did not complete the funnel.

**Formula**:
```
Abandonment Rate = ((Users at First Stage - Users at Final Stage) / Users at First Stage) × 100
```

**Example**:
- 10,000 users started, 1,500 completed
- Abandonment Rate = ((10,000 - 1,500) / 10,000) × 100 = 85%

## Funnel Stage Requirements

### Sequential Funnel Logic

**Definition**: Users must complete stages in order (1 → 2 → 3 → ...)

**Calculation**:
```python
def calculate_stage_users(stage_order, events_df):
    """
    Calculate users who reached a specific stage.
    Users must have completed all previous stages.
    """
    required_stages = stages[:stage_order]  # All stages up to current
    stage_event = stages[stage_order]['event_type']
    
    # Get users who completed all previous stages
    users_completed_prev = set()
    for prev_stage in required_stages[:-1]:
        prev_users = events_df[events_df['event_type'] == prev_stage['event_type']]['user_id'].unique()
        if not users_completed_prev:
            users_completed_prev = set(prev_users)
        else:
            users_completed_prev = users_completed_prev.intersection(set(prev_users))
    
    # Get users who completed current stage
    current_users = events_df[events_df['event_type'] == stage_event]['user_id'].unique()
    
    # Users who completed all previous stages AND current stage
    stage_users = users_completed_prev.intersection(set(current_users))
    
    return len(stage_users)
```

### Non-Sequential Funnel (Future)

**Definition**: Users can complete stages in any order (flexible funnel)

**Use Case**: Track users who completed any combination of actions

## Metric Calculations in DuckDB

### Example Query: Funnel Metrics

```sql
-- Step 1: Get user-stage progression
WITH user_progression AS (
    SELECT 
        user_id,
        event_type,
        MIN(created_at) as first_occurrence,
        CASE 
            WHEN event_type = 'page_view' THEN 1
            WHEN event_type = 'add_to_cart' THEN 2
            WHEN event_type = 'purchase' THEN 3
            ELSE 0
        END as stage_order
    FROM read_parquet(['events_2024-01-15.parquet'])
    WHERE created_at >= '2024-01-15'
      AND created_at < '2024-01-16'
      AND event_type IN ('page_view', 'add_to_cart', 'purchase')
    GROUP BY user_id, event_type, stage_order
),

-- Step 2: Filter users who completed stages sequentially
sequential_users AS (
    SELECT 
        user_id,
        MAX(CASE WHEN stage_order = 1 THEN 1 ELSE 0 END) as completed_stage_1,
        MAX(CASE WHEN stage_order = 2 THEN 1 ELSE 0 END) as completed_stage_2,
        MAX(CASE WHEN stage_order = 3 THEN 1 ELSE 0 END) as completed_stage_3
    FROM user_progression
    GROUP BY user_id
    HAVING completed_stage_1 = 1  -- Must complete first stage
)

-- Step 3: Calculate stage counts
SELECT 
    COUNT(DISTINCT CASE WHEN completed_stage_1 = 1 THEN user_id END) as stage_1_users,
    COUNT(DISTINCT CASE WHEN completed_stage_2 = 1 THEN user_id END) as stage_2_users,
    COUNT(DISTINCT CASE WHEN completed_stage_3 = 1 THEN user_id END) as stage_3_users
FROM sequential_users;
```

## Metric Visualization

### Funnel Chart

**Visual Representation**:
```
┌─────────────────────────────┐
│   Stage 1: Page View        │  10,000 users (100%)
│   ████████████████████████  │
│                             │
│   Stage 2: Add to Cart      │  3,000 users (30%)
│   ███████                   │  ↓ 70% drop-off
│                             │
│   Stage 3: Purchase         │  1,500 users (15%)
│   ███                       │  ↓ 50% drop-off
└─────────────────────────────┘
```

**Chart Properties**:
- Width proportional to user count
- Height: Fixed (consistent stage height)
- Color: Gradient (green to red based on conversion rate)
- Labels: User count, conversion rate, drop-off rate

### Metrics Cards

**Display Format**:
```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Total Users     │  │ Conversion Rate │  │ Drop-Off Rate   │
│ 10,000          │  │ 15.0%           │  │ 85.0%           │
│ Entered Funnel  │  │ First → Last    │  │ Total Drop-Off  │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

## Performance Targets

### Query Performance

- **Small Date Range** (1-7 days): < 500ms
- **Medium Date Range** (7-30 days): < 1 second
- **Large Date Range** (30-90 days): < 2 seconds
- **Very Large** (> 90 days): Use aggregation (future feature)

### Accuracy Targets

- **Funnel Tracking Accuracy**: > 95%
- **User Counting Accuracy**: > 99%
- **Conversion Rate Calculation**: Exact (no approximation)
- **Drop-Off Rate Calculation**: Exact

## Common Funnel Patterns

### E-Commerce Funnel

1. **Page View** → Product discovery
2. **Product View** → Product detail page
3. **Add to Cart** → Cart addition
4. **Checkout Started** → Checkout initiation
5. **Purchase Completed** → Conversion

**Expected Metrics**:
- Overall Conversion: 1-5% (industry average)
- Cart to Purchase: 30-70%

### SaaS Signup Funnel

1. **Landing Page View** → Marketing page
2. **Signup Form Viewed** → Form display
3. **Signup Form Submitted** → Form submission
4. **Email Verified** → Email confirmation
5. **First Action** → Product usage

**Expected Metrics**:
- Overall Conversion: 5-20% (industry average)
- Form Submit to Email Verified: 70-90%

### Content Funnel

1. **Content View** → Article/blog view
2. **Content Engagement** → Scroll, time on page
3. **CTA Click** → Call-to-action click
4. **Form Submit** → Lead form submission
5. **Conversion** → Desired action

**Expected Metrics**:
- Overall Conversion: 0.5-3% (content marketing)
- Engagement to CTA Click: 5-15%

---

**Document Owner**: Data Science Team  
**Last Updated**: Current Date  
**Status**: ✅ Complete
