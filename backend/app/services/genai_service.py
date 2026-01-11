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
        
        # Build enhanced prompt with guardrails and experiment suggestions
        prompt = f"""You are a Product Data Scientist analyzing funnel metrics for Pinterest, an inspiration-to-action platform.

Funnel Metrics:
{formatted_data}

Business Context:
- Project: Pinterest
- Domain: Home Feed
- Focus: Inspiration-to-action journey analysis

Provide a comprehensive analysis in JSON format with the following structure:

{{
  "insights": [
    "3-5 key findings about the funnel performance, patterns, anomalies, and trends. Include segment comparisons, drop-off analysis, and trend identification."
  ],
  "recommendations": [
    {{
      "priority": "High/Medium/Low",
      "title": "Clear, actionable title",
      "rationale": "Data-driven explanation with specific metrics",
      "expected_impact": "Quantified estimate (e.g., +15% click-through, +5% overall conversion)",
      "action_items": ["2-3 specific next steps"],
      "estimated_effort": "Low/Medium/High",
      "risk_level": "Low/Medium/High"
    }}
  ],
  "guardrails": [
    {{
      "type": "warning/trend",
      "severity": "Low/Medium/High",
      "message": "Warning message about potential negative impacts",
      "metric": "Relevant metric being monitored",
      "recommendation": "What to monitor or do to prevent negative impact"
    }}
  ],
  "experiment_suggestions": [
    {{
      "hypothesis": "Testable hypothesis statement",
      "test_design": "A/B test description: Control vs Treatment",
      "success_metrics": ["Primary metric", "Secondary metrics"],
      "expected_outcome": "Expected result (e.g., +15% click-through, +8% conversion)",
      "duration": "Recommended duration (e.g., 2 weeks)",
      "sample_size": "Recommended sample size (e.g., 10,000 users per variant)"
    }}
  ],
  "summary": {{
    "executive": "2-3 sentence executive summary for leadership",
    "technical": "Detailed technical summary for data scientists with specific metrics and patterns"
  }}
}}

Focus Areas:
1. **Segment Analysis**: Compare segments (Planner vs Actor, New vs Retained) and identify optimization opportunities
2. **Bottleneck Identification**: Identify stages with highest drop-off rates and suggest interventions
3. **Guardrail Monitoring**: Identify potential negative impacts (e.g., one segment benefiting at another's expense, content diversity decline)
4. **Experiment Design**: Suggest testable hypotheses with clear experiment designs
5. **Risk Assessment**: Evaluate trade-offs and long-term health concerns
6. **Pinterest Context**: Consider inspiration quality, intent formation, and long-term user value

Guardrail Checks:
- Monitor if optimizations hurt other segments
- Watch for content diversity decline
- Check for save rate degradation
- Ensure no negative impact on user trust

Be data-driven, specific, and actionable. Format as valid JSON only."""

        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a Product Data Scientist specializing in funnel analysis and optimization for Pinterest."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
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
        
        # Audience-specific context
        audience_contexts = {
            "executive": {
                "tone": "concise, strategic, business-focused",
                "focus": "high-level metrics, business impact, strategic recommendations",
                "length": "brief (2-3 pages)",
                "sections": "Executive Summary, Key Metrics, Strategic Recommendations, Next Steps"
            },
            "product_manager": {
                "tone": "actionable, feature-focused, user-centric",
                "focus": "actionable insights, feature recommendations, user behavior patterns",
                "length": "moderate (3-5 pages)",
                "sections": "Executive Summary, Key Insights, Feature Recommendations, Action Items, Experiment Suggestions"
            },
            "data_scientist": {
                "tone": "detailed, analytical, technical",
                "focus": "detailed metrics, statistical insights, experiment design, causal analysis",
                "length": "comprehensive (5-8 pages)",
                "sections": "Executive Summary, Technical Summary, Detailed Metrics, Segment Analysis, Insights, Recommendations, Experiment Suggestions, Guardrails"
            }
        }
        
        context = audience_contexts.get(audience, audience_contexts["data_scientist"])
        
        # Build report prompt with Pinterest-themed HTML template
        if format == "html":
            html_template = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>IAFA Report - {funnel_name}</title>
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      line-height: 1.6;
      color: #111827;
      background: linear-gradient(to bottom, #FAFAFA 0%, #FFFFFF 100%);
      padding: 40px 20px;
    }}
    .container {{
      max-width: 1000px;
      margin: 0 auto;
      background: white;
      border-radius: 16px;
      box-shadow: 0 4px 6px rgba(0,0,0,0.07), 0 10px 20px rgba(0,0,0,0.05);
      overflow: hidden;
    }}
    .header {{
      background: linear-gradient(135deg, #E60023 0%, #BD001F 100%);
      color: white;
      padding: 50px 40px;
      text-align: center;
    }}
    .header h1 {{
      font-size: 2.5em;
      font-weight: 700;
      margin-bottom: 10px;
      letter-spacing: -0.5px;
    }}
    .header p {{
      font-size: 1.1em;
      opacity: 0.95;
      font-weight: 300;
    }}
    .content {{
      padding: 50px 40px;
    }}
    .section {{
      margin-bottom: 50px;
    }}
    .section:last-child {{
      margin-bottom: 0;
    }}
    h2 {{
      color: #E60023;
      font-size: 1.8em;
      font-weight: 700;
      margin-bottom: 20px;
      padding-bottom: 10px;
      border-bottom: 3px solid #E60023;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    h2::before {{
      content: '';
      width: 4px;
      height: 24px;
      background: #E60023;
      border-radius: 2px;
    }}
    h3 {{
      color: #111827;
      font-size: 1.3em;
      font-weight: 600;
      margin-top: 30px;
      margin-bottom: 15px;
    }}
    .summary-box {{
      background: linear-gradient(135deg, #FEF2F2 0%, #FEFEFE 100%);
      border-left: 4px solid #E60023;
      border-radius: 12px;
      padding: 25px;
      margin: 20px 0;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    .metric-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 20px;
      margin: 25px 0;
    }}
    .metric-card {{
      background: #FAFAFA;
      border-radius: 12px;
      padding: 20px;
      text-align: center;
      border: 1px solid #E5E7EB;
      transition: transform 0.2s, box-shadow 0.2s;
    }}
    .metric-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(230,0,35,0.1);
    }}
    .metric-value {{
      font-size: 2em;
      font-weight: 700;
      color: #E60023;
      margin-bottom: 5px;
    }}
    .metric-label {{
      font-size: 0.9em;
      color: #6B7280;
      font-weight: 500;
    }}
    .insight-item {{
      background: #EFF6FF;
      border-left: 4px solid #3B82F6;
      border-radius: 8px;
      padding: 20px;
      margin: 15px 0;
    }}
    .recommendation-card {{
      background: white;
      border: 2px solid #E5E7EB;
      border-radius: 12px;
      padding: 25px;
      margin: 20px 0;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    .recommendation-card.high-priority {{
      border-color: #E60023;
      background: linear-gradient(135deg, #FEF2F2 0%, #FFFFFF 100%);
    }}
    .recommendation-card.medium-priority {{
      border-color: #F59E0B;
      background: linear-gradient(135deg, #FFFBEB 0%, #FFFFFF 100%);
    }}
    .priority-badge {{
      display: inline-block;
      padding: 6px 12px;
      border-radius: 20px;
      font-size: 0.85em;
      font-weight: 600;
      margin-bottom: 15px;
    }}
    .priority-badge.high {{
      background: #FEE2E2;
      color: #991B1B;
    }}
    .priority-badge.medium {{
      background: #FEF3C7;
      color: #92400E;
    }}
    .priority-badge.low {{
      background: #D1FAE5;
      color: #065F46;
    }}
    .action-item {{
      background: #F9FAFB;
      border-radius: 8px;
      padding: 15px;
      margin: 10px 0;
      border-left: 3px solid #E60023;
    }}
    .experiment-box {{
      background: linear-gradient(135deg, #F3E8FF 0%, #FAF5FF 100%);
      border: 2px solid #A78BFA;
      border-radius: 12px;
      padding: 25px;
      margin: 20px 0;
    }}
    .guardrail-box {{
      background: linear-gradient(135deg, #FEF3C7 0%, #FFFBEB 100%);
      border: 2px solid #F59E0B;
      border-radius: 12px;
      padding: 25px;
      margin: 20px 0;
    }}
    ul, ol {{
      margin: 15px 0;
      padding-left: 25px;
    }}
    li {{
      margin: 8px 0;
      line-height: 1.7;
    }}
    p {{
      margin: 15px 0;
      line-height: 1.8;
    }}
    .footer {{
      background: #F9FAFB;
      padding: 30px 40px;
      text-align: center;
      color: #6B7280;
      font-size: 0.9em;
      border-top: 1px solid #E5E7EB;
    }}
    .footer strong {{
      color: #E60023;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 25px 0;
      background: white;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    th {{
      background: #E60023;
      color: white;
      padding: 15px;
      text-align: left;
      font-weight: 600;
    }}
    td {{
      padding: 15px;
      border-bottom: 1px solid #E5E7EB;
    }}
    tr:hover {{
      background: #FAFAFA;
    }}
    .highlight {{
      background: #FEF2F2;
      padding: 2px 6px;
      border-radius: 4px;
      color: #E60023;
      font-weight: 600;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>📊 IAFA Journey Report</h1>
      <p>{funnel_name} • {start_date} to {end_date}</p>
    </div>
    <div class="content">
      {report_content}
    </div>
    <div class="footer">
      <p><strong>Inspiration-to-Action Funnel Analyzer (IAFA)</strong></p>
      <p>Generated on {generated_at} • Powered by AI Insights</p>
    </div>
  </div>
</body>
</html>
"""
            
            prompt = f"""You are a Product Data Scientist creating a beautifully styled HTML report for Pinterest with Pinterest-themed design.

Funnel Metrics:
{formatted_data}

AI-Generated Insights & Recommendations:
{json.dumps(recommendations, indent=2)}

Audience Context:
- Tone: {context['tone']}
- Focus: {context['focus']}
- Length: {context['length']}
- Sections: {context['sections']}

Generate a comprehensive HTML report with Pinterest-themed styling. Use the following HTML structure and CSS classes:

1. **Executive Summary** - Use `<div class="summary-box">` for the summary section
   - High-level overview of journey performance
   - Key findings and business impact
   - Top recommendations

2. **Key Metrics** - Use `<div class="metric-grid">` with `<div class="metric-card">` for each metric
   - Total users exposed (use `<span class="metric-value">` for numbers)
   - Overall progression rate
   - Stage-by-stage breakdown (use a table with proper styling)
   - Segment comparisons (if applicable)

3. **Insights** - Use `<div class="insight-item">` for each insight
   - Key patterns and trends
   - Segment differences
   - Bottleneck identification

4. **Recommendations** - Use `<div class="recommendation-card high-priority">` or `medium-priority` or `low-priority`
   - Add `<span class="priority-badge high">High Priority</span>` for priority badges
   - High-priority actions
   - Expected impact
   - Implementation steps (use `<div class="action-item">` for each action)

5. **Experiment Suggestions** - Use `<div class="experiment-box">` for each experiment
   - Testable hypotheses
   - Experiment designs
   - Success metrics

6. **Guardrails & Risks** - Use `<div class="guardrail-box">` for guardrails
   - Potential negative impacts
   - Metrics to monitor
   - Risk mitigation

7. **Next Steps** - Use `<div class="action-item">` for each action item
   - Immediate actions
   - Follow-up analysis
   - Timeline suggestions

HTML Structure Requirements:
- Use proper HTML5 semantic tags
- Use `<h2>` for main section headers (they will be styled with Pinterest red)
- Use `<h3>` for subsections
- Use the provided CSS classes for styling
- Include data-driven evidence for all claims
- Make it visually appealing with proper spacing
- Use tables for metric comparisons
- Use `<span class="highlight">` to highlight important numbers or metrics
- Be specific and actionable

Generate ONLY the content that goes inside `<div class="content">` (the {report_content} placeholder). Do NOT include the full HTML template, just the content sections with proper HTML tags and classes.

Format your response as clean HTML that will be inserted into the template:"""
        else:
            # For markdown and text, use simpler formatting
            prompt = f"""You are a Product Data Scientist creating a {format.upper()} report for {audience.replace('_', ' ').title()} audience.

Funnel Metrics:
{formatted_data}

AI-Generated Insights & Recommendations:
{json.dumps(recommendations, indent=2)}

Audience Context:
- Tone: {context['tone']}
- Focus: {context['focus']}
- Length: {context['length']}
- Sections: {context['sections']}

Generate a comprehensive {format.upper()} report with the following structure:

1. **Executive Summary** (2-3 paragraphs)
   - High-level overview of journey performance
   - Key findings and business impact
   - Top recommendations

2. **Key Metrics** (with context)
   - Total users exposed
   - Overall progression rate
   - Stage-by-stage breakdown
   - Segment comparisons (if applicable)

3. **Insights** (from AI analysis)
   - Key patterns and trends
   - Segment differences
   - Bottleneck identification

4. **Recommendations** (prioritized)
   - High-priority actions
   - Expected impact
   - Implementation steps

5. **Experiment Suggestions** (if applicable)
   - Testable hypotheses
   - Experiment designs
   - Success metrics

6. **Guardrails & Risks** (if applicable)
   - Potential negative impacts
   - Metrics to monitor
   - Risk mitigation

7. **Next Steps** (action items)
   - Immediate actions
   - Follow-up analysis
   - Timeline suggestions

Format Requirements:
- Use proper {format.upper()} formatting
- Include clear section headers
- Use bullet points and numbered lists where appropriate
- Make it scannable and easy to read
- Include data-driven evidence for all claims
- Be specific and actionable

Generate the complete report now:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are an expert at creating {format.upper()} reports for data science and product analytics. Create clear, professional, and actionable reports."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            report_content = response.choices[0].message.content.strip()
            
            # For HTML format, wrap content in Pinterest-themed template
            if format == "html":
                # Extract HTML content (remove any markdown code blocks if present)
                if "```html" in report_content:
                    report_content = report_content.split("```html")[1].split("```")[0].strip()
                elif "```" in report_content:
                    report_content = report_content.split("```")[1].split("```")[0].strip()
                
                # Format the HTML template with actual values
                from datetime import datetime as dt
                generated_at = dt.now().strftime("%B %d, %Y at %I:%M %p")
                
                full_html = html_template.format(
                    funnel_name=analytics_data.get('funnel_name', 'Unknown Journey'),
                    start_date=start_date,
                    end_date=end_date,
                    report_content=report_content,
                    generated_at=generated_at
                )
                report_content = full_html
            
            return {
                "report": report_content,
                "format": format,
                "audience": audience,
                "generated_at": datetime.now().isoformat(),
                "model_used": self.model
            }
            
        except Exception as e:
            return {
                "error": f"Failed to generate report: {str(e)}",
                "report": "",
                "format": format
            }
