"""GenAI service for generating insights and recommendations."""

import json
import hashlib
from typing import Dict, List, Optional, Any
from datetime import datetime
from openai import OpenAI
from app.core.config import settings


class GenAIService:
    """Service for GenAI-powered insights and recommendations."""

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
        self.cache: Dict[str, Dict] = {}  # Simple in-memory cache
        self.cache_ttl = 24 * 60 * 60  # 24 hours in seconds
        self.model = "gpt-4"  # Can be configured to use gpt-3.5-turbo for cost savings

    def _get_cache_key(self, funnel_id: str, start_date: str, end_date: str, filters: Dict) -> str:
        """Generate cache key from parameters."""
        cache_data = {
            "funnel_id": funnel_id,
            "start_date": start_date,
            "end_date": end_date,
            "filters": json.dumps(filters, sort_keys=True)
        }
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_string.encode()).hexdigest()

    def _get_from_cache(self, cache_key: str) -> Optional[Dict]:
        """Get cached response if available and not expired."""
        if cache_key in self.cache:
            cached_item = self.cache[cache_key]
            age = (datetime.now() - cached_item["timestamp"]).total_seconds()
            if age < self.cache_ttl:
                return cached_item["data"]
            else:
                # Remove expired cache
                del self.cache[cache_key]
        return None

    def _save_to_cache(self, cache_key: str, data: Dict):
        """Save response to cache."""
        self.cache[cache_key] = {
            "data": data,
            "timestamp": datetime.now()
        }

    def _format_funnel_data(self, analytics_data: Dict) -> str:
        """Format funnel analytics data for prompt."""
        lines = []
        
        # Basic info
        lines.append(f"Funnel: {analytics_data.get('funnel_name', 'Unknown')}")
        lines.append(f"Date Range: {analytics_data.get('date_range', {}).get('start', '')} to {analytics_data.get('date_range', {}).get('end', '')}")
        lines.append("")
        
        # Stages
        if analytics_data.get('stages'):
            lines.append("Stage Metrics:")
            for stage in analytics_data['stages']:
                lines.append(f"  - {stage.get('stage_name', 'Unknown')}: {stage.get('users', 0)} users, {stage.get('conversion_rate', 0):.1f}% conversion, {stage.get('drop_off_rate', 0):.1f}% drop-off")
            lines.append("")
        
        # Overall metrics
        if analytics_data.get('total_users'):
            lines.append(f"Total Users: {analytics_data.get('total_users', 0):,}")
            lines.append(f"Completed Users: {analytics_data.get('completed_users', 0):,}")
            lines.append(f"Overall Conversion Rate: {analytics_data.get('overall_conversion_rate', 0):.2f}%")
            lines.append("")
        
        # Segment breakdown
        if analytics_data.get('segments'):
            lines.append("Segment Breakdown:")
            for segment_value, segment_data in analytics_data['segments'].items():
                lines.append(f"  {segment_value}:")
                lines.append(f"    - Total Users: {segment_data.get('total_users', 0):,}")
                lines.append(f"    - Completed Users: {segment_data.get('completed_users', 0):,}")
                lines.append(f"    - Conversion Rate: {segment_data.get('overall_conversion_rate', 0):.2f}%")
                if segment_data.get('stages'):
                    lines.append(f"    - Stages: {len(segment_data['stages'])} stages")
            lines.append("")
        
        return "\n".join(lines)

    async def generate_recommendations(
        self,
        funnel_id: str,
        analytics_data: Dict,
        start_date: str,
        end_date: str,
        filters: Dict,
        audience: str = "data_scientist"
    ) -> Dict:
        """Generate AI-powered insights and recommendations."""
        
        if not self.client:
            return {
                "error": "OpenAI API key not configured",
                "insights": [],
                "recommendations": [],
                "guardrails": []
            }
        
        # Check cache
        cache_key = self._get_cache_key(funnel_id, start_date, end_date, filters)
        cached_response = self._get_from_cache(cache_key)
        if cached_response:
            cached_response["cache_hit"] = True
            return cached_response
        
        # Format data for prompt
        formatted_data = self._format_funnel_data(analytics_data)
        
        # Build concise, actionable prompt
        prompt = f"""Analyze this Pinterest funnel data. Be CONCISE and ACTIONABLE.

DATA:
{formatted_data}

Return JSON with this EXACT structure:

{{
  "insights": [
    "Max 4 insights. Each = 1 sentence with a NUMBER. Example: 'Save stage has 49% drop-off, highest in funnel'"
  ],
  "recommendations": [
    {{
      "priority": "High",
      "title": "5 words max - verb first",
      "action": "One specific action to take",
      "impact": "+X% metric (be specific)",
      "effort": "Low/Med/High"
    }}
  ],
  "guardrails": [
    {{
      "metric": "What to protect",
      "threshold": "Alert if X drops below Y%",
      "why": "One sentence risk"
    }}
  ],
  "experiment": {{
    "hypothesis": "If [change] then [outcome] by [amount]",
    "test": "Control: X, Treatment: Y",
    "metric": "Primary success metric"
  }},
  "summary": "2 sentences max: biggest problem + top action"
}}

RULES:
- Max 4 insights (1 sentence each, must include numbers)
- Max 3 recommendations (verb-first titles)
- Max 2 guardrails
- 1 experiment suggestion
- Every claim needs data
- No filler words

JSON only:"""

        try:
            # Call OpenAI API with concise settings
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You generate ultra-concise analytics insights. Rules: max 4 insights, max 3 recommendations, every point has a number, no filler words. Return valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Low temp for focused, consistent output
                max_tokens=1000   # Reduced for conciseness
            )
            
            # Parse response
            content = response.choices[0].message.content.strip()
            
            # Try to extract JSON from response (handle markdown code blocks)
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            result = json.loads(content)
            
            # Add metadata
            result["generated_at"] = datetime.now().isoformat()
            result["model_used"] = self.model
            result["cache_hit"] = False
            
            # Save to cache
            self._save_to_cache(cache_key, result)
            
            return result
            
        except json.JSONDecodeError as e:
            # If JSON parsing fails, return error with raw response
            return {
                "error": f"Failed to parse AI response: {str(e)}",
                "raw_response": content if 'content' in locals() else None,
                "insights": [],
                "recommendations": [],
                "guardrails": []
            }
        except Exception as e:
            return {
                "error": f"OpenAI API error: {str(e)}",
                "insights": [],
                "recommendations": [],
                "guardrails": []
            }

    async def generate_report(
        self,
        funnel_id: str,
        analytics_data: Dict,
        start_date: str,
        end_date: str,
        filters: Dict,
        audience: str = "data_scientist",
        format: str = "html"
    ) -> Dict:
        """Generate AI-powered report in specified format."""
        
        if not self.client:
            return {
                "error": "OpenAI API key not configured",
                "report": "",
                "format": format
            }
        
        # Get AI recommendations first
        recommendations = await self.generate_recommendations(
            funnel_id=funnel_id,
            analytics_data=analytics_data,
            start_date=start_date,
            end_date=end_date,
            filters=filters,
            audience=audience
        )
        
        if "error" in recommendations:
            return recommendations
        
        # Format data for report prompt
        formatted_data = self._format_funnel_data(analytics_data)
        
        # Audience-specific context - all optimized for conciseness
        audience_contexts = {
            "executive": {
                "tone": "ultra-concise, strategic, bottom-line focused",
                "focus": "3-5 key metrics, business impact, 2-3 action items",
                "length": "1 page max - bullet points only",
                "sections": "Summary (3 bullets), Key Numbers, Recommendations (2-3)"
            },
            "product_manager": {
                "tone": "actionable, concise, decision-focused",
                "focus": "top insights, specific actions, next experiment",
                "length": "1-2 pages - bullet points preferred",
                "sections": "Summary, Key Insights (5 max), Actions (3 max), Next Experiment"
            },
            "data_scientist": {
                "tone": "precise, data-driven, concise",
                "focus": "key metrics with numbers, statistical findings, experiment design",
                "length": "2 pages max - tables and bullets",
                "sections": "Summary, Metrics Table, Key Findings (5 max), Experiment Suggestion, Guardrails"
            }
        }
        
        context = audience_contexts.get(audience, audience_contexts["data_scientist"])
        
        # Define HTML template (used if format is HTML) - Based on standard export styling
        html_template = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>IAFA Executive Report - __FUNNEL_NAME__</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      max-width: 1200px;
      margin: 0 auto;
      padding: 40px 20px;
      background-color: #f5f5f5;
    }
    .container {
      background: white;
      padding: 40px;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 {
      color: #E60023;
      border-bottom: 3px solid #E60023;
      padding-bottom: 10px;
      margin-bottom: 30px;
    }
    h2 {
      color: #111827;
      margin-top: 30px;
      margin-bottom: 15px;
      font-size: 1.5em;
    }
    h3 {
      color: #111827;
      margin-top: 20px;
      margin-bottom: 10px;
      font-size: 1.2em;
    }
    .summary {
      background: #f9fafb;
      padding: 20px;
      border-radius: 8px;
      margin: 20px 0;
      border-left: 4px solid #E60023;
    }
    .summary-item {
      display: flex;
      justify-content: space-between;
      padding: 10px 0;
      border-bottom: 1px solid #e5e7eb;
    }
    .summary-item:last-child {
      border-bottom: none;
    }
    .summary-label {
      font-weight: 600;
      color: #6b7280;
    }
    .summary-value {
      font-weight: 700;
      color: #111827;
      font-size: 1.1em;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
    }
    th {
      background: #f9fafb;
      padding: 12px;
      text-align: left;
      font-weight: 600;
      color: #374151;
      border-bottom: 2px solid #e5e7eb;
    }
    td {
      padding: 12px;
      border-bottom: 1px solid #e5e7eb;
    }
    tr:hover {
      background: #f9fafb;
    }
    .insights {
      background: #eff6ff;
      padding: 20px;
      border-radius: 8px;
      margin: 20px 0;
      border-left: 4px solid #3b82f6;
    }
    .insights ul {
      margin: 0;
      padding-left: 20px;
    }
    .insights li {
      margin: 8px 0;
    }
    .recommendations {
      background: #fef2f2;
      padding: 20px;
      border-radius: 8px;
      margin: 20px 0;
      border-left: 4px solid #E60023;
    }
    .recommendation-item {
      background: white;
      padding: 15px;
      margin: 10px 0;
      border-radius: 6px;
      border-left: 3px solid #E60023;
    }
    .experiments {
      background: #f3e8ff;
      padding: 20px;
      border-radius: 8px;
      margin: 20px 0;
      border-left: 4px solid #a78bfa;
    }
    .guardrails {
      background: #fef3c7;
      padding: 20px;
      border-radius: 8px;
      margin: 20px 0;
      border-left: 4px solid #f59e0b;
    }
    ul, ol {
      margin: 15px 0;
      padding-left: 20px;
    }
    li {
      margin: 8px 0;
    }
    p {
      margin: 15px 0;
      line-height: 1.8;
    }
    .footer {
      margin-top: 40px;
      padding-top: 20px;
      border-top: 1px solid #e5e7eb;
      color: #6b7280;
      font-size: 0.9em;
      text-align: center;
    }
    strong {
      color: #111827;
      font-weight: 600;
    }
    .highlight {
      background: #fef2f2;
      padding: 2px 6px;
      border-radius: 4px;
      color: #E60023;
      font-weight: 600;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Inspiration-to-Action Funnel Analyzer (IAFA)</h1>
    <h2>AI-Powered __REPORT_TYPE__ Report</h2>
    
    <div style="margin-bottom: 30px;">
      <p><strong>Journey:</strong> __FUNNEL_NAME__</p>
      <p><strong>Date Range:</strong> __START_DATE__ to __END_DATE__</p>
      <p><strong>Audience:</strong> __AUDIENCE_DISPLAY__</p>
    </div>
    
    <div class="content">
      __REPORT_CONTENT__
    </div>
    
    <div class="footer">
      <p>Report Generated: __GENERATED_AT__</p>
      <p>Inspiration-to-Action Funnel Analyzer (IAFA)</p>
    </div>
  </div>
</body>
</html>
"""
        
        # Build report prompt
        if format == "html":
            prompt = f"""You are a Product Data Scientist creating a CONCISE HTML report for {audience.replace('_', ' ').title()}.

DATA:
{formatted_data}

INSIGHTS:
{json.dumps(recommendations, indent=2)}

REQUIREMENTS:
- Tone: {context['tone']}
- Focus: {context['focus']}
- Length: {context['length']}
- Sections: {context['sections']}

CRITICAL RULES FOR CONCISENESS:
1. Use BULLET POINTS, not paragraphs
2. Each insight = 1 sentence max
3. Each recommendation = action + expected impact (1 line)
4. No filler words, no repetition
5. Numbers are mandatory - every claim needs data
6. Max 3-5 bullets per section
7. Total report should fit on 1-2 printed pages

Use these CSS classes for sections:

<div class="summary">
  <h2>Summary</h2>
  <ul>
    <li><strong>Key Finding:</strong> One sentence with number</li>
  </ul>
</div>

<div class="insights">
  <h2>Key Insights</h2>
  <ul>
    <li>Insight with specific number</li>
  </ul>
</div>

<div class="recommendations">
  <h2>Recommendations</h2>
  <ul>
    <li><strong>Action:</strong> What to do → Expected impact</li>
  </ul>
</div>

<div class="experiments">
  <h2>Next Experiment</h2>
  <p><strong>Hypothesis:</strong> If X then Y</p>
  <p><strong>Metric:</strong> What to measure</p>
</div>

<div class="guardrails">
  <h2>Guardrails</h2>
  <ul>
    <li>What NOT to break</li>
  </ul>
</div>

Generate ONLY the HTML content. Be extremely concise - every word must add value:"""
        else:
            # For markdown and text - concise formatting
            prompt = f"""Create a CONCISE {format.upper()} report for {audience.replace('_', ' ').title()}.

DATA:
{formatted_data}

INSIGHTS:
{json.dumps(recommendations, indent=2)}

REQUIREMENTS:
- {context['tone']}
- {context['length']}
- Sections: {context['sections']}

STRUCTURE (use bullet points, max 3-5 per section):

## Summary
- Key finding 1 with number
- Key finding 2 with number
- Top recommendation

## Key Metrics
| Metric | Value |
|--------|-------|
| Total Users | X |
| Progression Rate | X% |

## Insights (max 5)
- Insight with specific data point

## Recommendations (max 3)
1. **Action** → Expected impact

## Next Experiment
- Hypothesis: If X then Y
- Primary metric: Z

## Guardrails
- Metric to protect

RULES:
- Every bullet = 1 sentence max
- Every claim needs a number
- No filler words
- Total: 1-2 pages max

Generate now:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You create ultra-concise {format.upper()} reports. Rules: bullet points only, 1 sentence per bullet, every claim needs data, no filler words, max 1-2 pages. Be direct and actionable."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,  # Lower temperature for more focused output
                max_tokens=2000   # Reduced to encourage conciseness
            )
            
            # Initialize report_content
            report_content = ""
            if response.choices and len(response.choices) > 0 and response.choices[0].message:
                report_content = response.choices[0].message.content.strip()
            else:
                raise ValueError("Empty response from OpenAI API")
            
            # For HTML format, wrap content in template
            if format == "html":
                # Extract HTML content (remove any markdown code blocks if present)
                if "```html" in report_content:
                    report_content = report_content.split("```html")[1].split("```")[0].strip()
                elif "```" in report_content:
                    report_content = report_content.split("```")[1].split("```")[0].strip()
                
                # If AI generated plain text or markdown, convert it to HTML with proper CSS classes
                # Check if content already has styled HTML with our CSS classes
                has_styled_html = ("class=\"summary\"" in report_content or "class=\"insights\"" in report_content or 
                                  "class=\"recommendations\"" in report_content or "class=\"experiments\"" in report_content or
                                  "class=\"guardrails\"" in report_content)
                
                if not has_styled_html:
                    # Convert plain text/markdown to HTML with proper structure and CSS classes
                    lines = report_content.split('\n')
                    html_sections = []
                    current_section = None
                    current_list = None
                    in_paragraph = False
                    
                    for line in lines:
                        original_line = line
                        line = line.strip()
                        if not line:
                            if current_list:
                                html_sections.append('</ul>')
                                current_list = None
                            if in_paragraph:
                                html_sections.append('</p>')
                                in_paragraph = False
                            continue
                        
                        # Section headers (## Header)
                        if line.startswith('## '):
                            if current_list:
                                html_sections.append('</ul>')
                                current_list = None
                            if in_paragraph:
                                html_sections.append('</p>')
                                in_paragraph = False
                            if current_section:
                                html_sections.append('</div>')
                            
                            section_title = line[3:].strip()
                            # Determine section class based on title keywords
                            title_lower = section_title.lower()
                            if 'summary' in title_lower or 'executive' in title_lower:
                                current_section = 'summary'
                            elif 'insight' in title_lower:
                                current_section = 'insights'
                            elif 'recommendation' in title_lower:
                                current_section = 'recommendations'
                            elif 'experiment' in title_lower or 'suggestion' in title_lower:
                                current_section = 'experiments'
                            elif 'guardrail' in title_lower or 'risk' in title_lower:
                                current_section = 'guardrails'
                            else:
                                # Default - no special styling
                                current_section = None
                            
                            if current_section:
                                html_sections.append(f'<div class="{current_section}">')
                                html_sections.append(f'<h2>{section_title}</h2>')
                            else:
                                html_sections.append(f'<h2>{section_title}</h2>')
                                
                        # Subsection headers (### Subheader)
                        elif line.startswith('### '):
                            if current_list:
                                html_sections.append('</ul>')
                                current_list = None
                            if in_paragraph:
                                html_sections.append('</p>')
                                in_paragraph = False
                            html_sections.append(f'<h3>{line[4:]}</h3>')
                        # Bold text (might be markdown **text**)
                        elif line.startswith('**') and line.endswith('**'):
                            if current_list:
                                html_sections.append('</ul>')
                                current_list = None
                            text = line.replace('**', '').strip()
                            if not in_paragraph:
                                html_sections.append('<p>')
                                in_paragraph = True
                            html_sections[-1] = html_sections[-1] + f'<strong>{text}</strong>'
                        # Lists (- item or * item or numbered)
                        elif line.startswith('- ') or line.startswith('* ') or (len(line) > 2 and line[0].isdigit() and line[1] == '.'):
                            if in_paragraph:
                                html_sections.append('</p>')
                                in_paragraph = False
                            if not current_list:
                                # Determine if numbered or bulleted
                                if line[0].isdigit():
                                    html_sections.append('<ol>')
                                else:
                                    html_sections.append('<ul>')
                                current_list = True
                            
                            # Remove list markers
                            list_item = line
                            if line.startswith('- ') or line.startswith('* '):
                                list_item = line[2:].strip()
                            elif line[0].isdigit() and '. ' in line:
                                list_item = line.split('. ', 1)[1].strip()
                            
                            html_sections.append(f'<li>{list_item}</li>')
                        # Regular paragraphs
                        else:
                            if current_list:
                                # Check if we have <ol> or <ul>
                                if any('</ol>' in s for s in html_sections[-5:]):
                                    html_sections.append('</ol>')
                                else:
                                    html_sections.append('</ul>')
                                current_list = None
                            
                            # Check if this should start a new paragraph or continue existing
                            if not in_paragraph:
                                html_sections.append(f'<p>{line}')
                                in_paragraph = True
                            else:
                                # Continue existing paragraph with a space
                                html_sections[-1] = html_sections[-1] + ' ' + line
                    
                    # Close any open tags
                    if current_list:
                        html_sections.append('</ul>')
                    if in_paragraph:
                        html_sections.append('</p>')
                    if current_section:
                        html_sections.append('</div>')
                    
                    report_content = '\n'.join(html_sections)
                
                # Format the HTML template with actual values
                from datetime import datetime as dt
                generated_at = dt.now().strftime("%B %d, %Y at %I:%M %p")
                funnel_name = analytics_data.get('funnel_name', 'Unknown Journey')
                
                # Audience-specific report type labels
                report_type_map = {
                    "data_scientist": "Technical Analysis",
                    "executive": "Executive Summary",
                    "product_manager": "Product Insights"
                }
                audience_display_map = {
                    "data_scientist": "Data Scientist",
                    "executive": "Executive",
                    "product_manager": "Product Manager"
                }
                report_type = report_type_map.get(audience, "Analytics")
                audience_display = audience_display_map.get(audience, audience.replace('_', ' ').title())
                
                # Replace placeholders using __ delimiters to avoid conflicts with CSS braces
                full_html = html_template.replace('__FUNNEL_NAME__', funnel_name)
                full_html = full_html.replace('__START_DATE__', start_date)
                full_html = full_html.replace('__END_DATE__', end_date)
                full_html = full_html.replace('__REPORT_TYPE__', report_type)
                full_html = full_html.replace('__AUDIENCE_DISPLAY__', audience_display)
                full_html = full_html.replace('__REPORT_CONTENT__', report_content)
                full_html = full_html.replace('__GENERATED_AT__', generated_at)
                
                report_content = full_html
            
            return {
                "report": report_content,
                "format": format,
                "audience": audience,
                "generated_at": datetime.now().isoformat(),
                "model_used": self.model
            }
            
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"Error generating report: {error_trace}")
            return {
                "error": f"Failed to generate report: {str(e)}",
                "report": "",
                "format": format,
                "traceback": error_trace
            }
