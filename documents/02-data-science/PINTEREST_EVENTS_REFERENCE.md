# Pinterest Events Reference

**Common Pinterest events for inspiration-to-action journey analysis**

---

## 🎯 Core Pinterest Events

### 1. **pin_view**
- **Description**: User views a pin in their feed, search results, or board
- **When it fires**: Every time a pin is displayed to the user
- **Use case**: First touchpoint in the inspiration journey
- **Common properties**: `pin_id`, `board_id`, `surface` (Home, Search, Board)

### 2. **save**
- **Description**: User saves a pin to a board
- **When it fires**: User clicks the "Save" button
- **Use case**: Strong intent signal - user wants to reference later
- **Common properties**: `pin_id`, `board_id`, `board_name`

### 3. **click**
- **Description**: User clicks on a pin to view details or visit the source
- **When it fires**: User clicks the pin image or title
- **Use case**: Engagement signal - user wants more information
- **Common properties**: `pin_id`, `destination_url`, `click_type` (pin, title, etc.)

### 4. **purchase**
- **Description**: User completes a purchase from a pin
- **When it fires**: Transaction completed (via Pinterest Shopping or outbound)
- **Use case**: Final conversion action
- **Common properties**: `order_id`, `value`, `currency`, `product_ids`

---

## 📊 Additional Pinterest Events (Recommended)

### 5. **board_view**
- **Description**: User views a board (their own or someone else's)
- **When it fires**: User navigates to a board page
- **Use case**: Understanding board-level engagement
- **Common properties**: `board_id`, `board_name`, `is_own_board`

### 6. **board_create**
- **Description**: User creates a new board
- **When it fires**: User creates a new board
- **Use case**: Organizing behavior - strong planning signal
- **Common properties**: `board_id`, `board_name`, `board_type`

### 7. **pin_edit**
- **Description**: User edits a saved pin (moves to different board, adds note)
- **When it fires**: User modifies a saved pin
- **Use case**: Refinement behavior - user organizing their saves
- **Common properties**: `pin_id`, `old_board_id`, `new_board_id`

### 8. **search**
- **Description**: User performs a search query
- **When it fires**: User submits a search
- **Use case**: Intent discovery - what users are looking for
- **Common properties**: `query`, `results_count`, `surface`

### 9. **idea_pin_view**
- **Description**: User views an Idea Pin (multi-page story format)
- **When it fires**: User opens an Idea Pin
- **Use case**: Rich content engagement
- **Common properties**: `idea_pin_id`, `page_number`, `duration`

### 10. **idea_pin_complete**
- **Description**: User views all pages of an Idea Pin
- **When it fires**: User reaches the last page
- **Use case**: Deep engagement signal
- **Common properties**: `idea_pin_id`, `total_pages`, `view_duration`

### 11. **shop_click**
- **Description**: User clicks on a shopping pin or product
- **When it fires**: User clicks on a buyable pin
- **Use case**: Shopping intent
- **Common properties**: `product_id`, `price`, `merchant_id`

### 12. **video_play**
- **Description**: User plays a video pin
- **When it fires**: Video starts playing
- **Use case**: Video content engagement
- **Common properties**: `pin_id`, `video_duration`, `video_type`

### 13. **video_complete**
- **Description**: User watches a video pin to completion
- **When it fires**: Video reaches 100% completion
- **Use case**: High engagement signal
- **Common properties**: `pin_id`, `video_duration`, `watch_time`

### 14. **follow**
- **Description**: User follows a creator or board
- **When it fires**: User clicks "Follow"
- **Use case**: Long-term engagement signal
- **Common properties**: `followed_user_id`, `followed_board_id`, `follow_type`

### 15. **comment**
- **Description**: User comments on a pin
- **When it fires**: User submits a comment
- **Use case**: Community engagement
- **Common properties**: `pin_id`, `comment_length`, `is_reply`

### 16. **share**
- **Description**: User shares a pin (via link, message, etc.)
- **When it fires**: User shares a pin
- **Use case**: Viral/word-of-mouth signal
- **Common properties**: `pin_id`, `share_method`, `share_destination`

### 17. **closeup_view**
- **Description**: User views pin in closeup/detail view
- **When it fires**: User opens pin detail page
- **Use case**: Deep engagement - user wants full details
- **Common properties**: `pin_id`, `view_duration`, `source` (feed, search, board)

### 18. **related_pin_click**
- **Description**: User clicks on a related pin suggestion
- **When it fires**: User clicks a recommended pin
- **Use case**: Discovery and recommendation effectiveness
- **Common properties**: `source_pin_id`, `related_pin_id`, `recommendation_type`

### 19. **filter_apply**
- **Description**: User applies a filter (e.g., price, color, style)
- **When it fires**: User selects a filter option
- **Use case**: Intent refinement
- **Common properties**: `filter_type`, `filter_value`, `surface`

### 20. **collection_view**
- **Description**: User views a collection (curated pin sets)
- **When it fires**: User opens a collection
- **Use case**: Curated content engagement
- **Common properties**: `collection_id`, `collection_type`, `pin_count`

---

## 🎯 Recommended Journey Combinations

### Journey 1: Discovery to Save (Most Common)
```
pin_view → save
```
- **Use case**: Measure inspiration quality
- **Metrics**: Save rate, time to save

### Journey 2: Discovery to Action
```
pin_view → save → click → purchase
```
- **Use case**: Full inspiration-to-action funnel
- **Metrics**: Multi-stage progression rates

### Journey 3: Planning Journey
```
pin_view → save → board_create → pin_edit
```
- **Use case**: Planning and organization behavior
- **Metrics**: Planning depth, organization rate

### Journey 4: Shopping Journey
```
pin_view → shop_click → purchase
```
- **Use case**: Shopping-specific conversion
- **Metrics**: Shopping conversion rate

### Journey 5: Video Engagement
```
pin_view → video_play → video_complete → click
```
- **Use case**: Video content effectiveness
- **Metrics**: Video completion rate, click-through

### Journey 6: Discovery Journey
```
search → pin_view → save → click
```
- **Use case**: Search-driven discovery
- **Metrics**: Search-to-action rate

---

## 📈 Event Priority for IAFA

### **Tier 1: Essential Events** (Already Implemented)
- ✅ `pin_view` - Core discovery event
- ✅ `save` - Intent signal
- ✅ `click` - Engagement signal
- ✅ `purchase` - Conversion event

### **Tier 2: High-Value Events** (Recommended Next)
- 🔄 `board_view` - Board engagement
- 🔄 `search` - Intent discovery
- 🔄 `closeup_view` - Deep engagement
- 🔄 `shop_click` - Shopping intent

### **Tier 3: Advanced Events** (Future)
- 📋 `idea_pin_view` - Rich content
- 📋 `video_play` - Video engagement
- 📋 `follow` - Long-term engagement
- 📋 `comment` - Community engagement

---

## 💡 Event Properties to Track

### Universal Properties (All Events)
- `user_id` - User identifier
- `session_id` - Session identifier
- `timestamp` - Event timestamp
- `surface` - Where event occurred (Home, Search, Board, Profile)
- `user_intent` - User segment (Planner, Actor, Browser, Curator)
- `user_tenure` - User tenure (New, Retained)
- `content_category` - Content category

### Event-Specific Properties
- **pin_view**: `pin_id`, `position_in_feed`, `impression_type`
- **save**: `pin_id`, `board_id`, `board_name`, `save_method`
- **click**: `pin_id`, `destination_url`, `click_type`, `link_type`
- **purchase**: `order_id`, `value`, `currency`, `product_ids`, `merchant_id`

---

## 🔧 Implementation Notes

### Current Implementation
- ✅ Pre-populated with: `pin_view`, `save`, `click`, `purchase`
- ✅ Supports all event types dynamically
- ✅ UI allows selecting from available event types

### Adding New Events
1. Update `populate_sample_data.py` to generate new event types
2. Events automatically appear in journey creation UI
3. No code changes needed - fully dynamic!

### Event Naming Convention
- Use lowercase with underscores: `pin_view`, `board_create`
- Be descriptive: `idea_pin_view` not `ipv`
- Match Pinterest's event naming when possible

---

## 📚 References

- Pinterest Developer Documentation
- Pinterest Analytics Events
- Pinterest Shopping Events

---

**Last Updated**: Event reference for IAFA journey analysis
