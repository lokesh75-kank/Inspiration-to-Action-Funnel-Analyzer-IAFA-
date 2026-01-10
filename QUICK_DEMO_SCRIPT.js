/**
 * Quick Demo Script for IAFA Live Demo
 * Copy-paste into browser console (F12) after getting API Key from Projects page
 * 
 * Step 1: Get API Key from Projects page
 * Step 2: Replace YOUR_API_KEY below
 * Step 3: Run in browser console
 */

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

// Simulate experiment data (After - Treatment)
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
