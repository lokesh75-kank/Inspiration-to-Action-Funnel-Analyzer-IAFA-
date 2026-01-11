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
        
        # Build report prompt
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
