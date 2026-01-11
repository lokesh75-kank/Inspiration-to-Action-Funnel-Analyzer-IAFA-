import { useState, useEffect } from 'react'
import { analyticsApi } from '../../services/api'

interface AIInsights {
  insights?: string[]
  recommendations?: Array<{
    priority: string
    title: string
    action?: string
    impact?: string
    effort?: string
    // Legacy fields for backward compatibility
    rationale?: string
    expected_impact?: string
    action_items?: string[]
    estimated_effort?: string
    risk_level?: string
  }>
  guardrails?: Array<{
    metric?: string
    threshold?: string
    why?: string
    // Legacy fields
    type?: string
    severity?: string
    message?: string
    recommendation?: string
  }>
  experiment?: {
    hypothesis: string
    test: string
    metric: string
  }
  // Legacy experiment format
  experiment_suggestions?: Array<{
    hypothesis: string
    test_design: string
    success_metrics: string[]
    expected_outcome: string
    duration?: string
    sample_size?: string
  }>
  summary?: string | {
    executive?: string
    technical?: string
  }
  error?: string
  cache_hit?: boolean
  generated_at?: string
}

interface AIInsightsPanelProps {
  funnelId: string
  startDate: string
  endDate: string
  filters?: {
    user_intent?: string[]
    content_category?: string[]
    surface?: string[]
    user_tenure?: string[]
    segment_by?: string
  }
  orgId?: string
}

export default function AIInsightsPanel({
  funnelId,
  startDate,
  endDate,
  filters = {},
  orgId = 'poc-org'
}: AIInsightsPanelProps) {
  const [insights, setInsights] = useState<AIInsights | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [expanded, setExpanded] = useState(true)

  const fetchInsights = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await analyticsApi.getFunnelRecommendations(
        funnelId,
        startDate,
        endDate,
        filters,
        orgId
      )
      setInsights(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to generate insights')
      setInsights(null)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (funnelId && startDate && endDate) {
      fetchInsights()
    }
  }, [funnelId, startDate, endDate, JSON.stringify(filters)])

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-300'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300'
      case 'low':
        return 'bg-blue-100 text-blue-800 border-blue-300'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300'
    }
  }

  if (!funnelId || !startDate || !endDate) {
    return null
  }

  return (
    <div className="p-6 rounded-xl shadow-sm border border-gray-200 mb-6" style={{ backgroundColor: '#FAFAFA' }}>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <h2 className="text-lg font-semibold text-gray-900">🤖 AI-Powered Insights & Recommendations</h2>
          {insights?.cache_hit && (
            <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">Cached</span>
          )}
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={fetchInsights}
            disabled={loading}
            className="px-3 py-1 text-sm bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50"
          >
            {loading ? 'Generating...' : 'Refresh'}
          </button>
          <button
            onClick={() => setExpanded(!expanded)}
            className="px-3 py-1 text-sm bg-white border border-gray-300 rounded-md hover:bg-gray-50"
          >
            {expanded ? 'Collapse' : 'Expand'}
          </button>
        </div>
      </div>

      {loading && !insights && (
        <div className="text-center py-8">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-[#E60023]"></div>
          <p className="mt-2 text-gray-600">Generating AI insights...</p>
        </div>
      )}

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-md mb-4">
          <p className="text-red-800 text-sm">
            {error === 'OpenAI API key not configured' 
              ? '⚠️ OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.'
              : error}
          </p>
        </div>
      )}

      {insights && expanded && (
        <div className="space-y-4">
          {/* Summary - Show first for quick overview */}
          {insights.summary && (
            <div className="p-3 bg-blue-50 border-l-4 border-blue-500 rounded-r-md">
              <p className="text-sm text-gray-800 font-medium">
                {typeof insights.summary === 'string' 
                  ? insights.summary 
                  : insights.summary.executive || insights.summary.technical}
              </p>
            </div>
          )}

          {/* Insights - Compact list */}
          {insights.insights && insights.insights.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-gray-900 mb-2">💡 Key Insights</h3>
              <ul className="space-y-1">
                {insights.insights.map((insight, index) => (
                  <li key={index} className="text-sm text-gray-700 flex items-start">
                    <span className="text-[#E60023] mr-2">•</span>
                    <span>{insight}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Recommendations - Compact cards */}
          {insights.recommendations && insights.recommendations.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-gray-900 mb-2">⭐ Recommendations</h3>
              <div className="space-y-2">
                {insights.recommendations.map((rec, index) => (
                  <div
                    key={index}
                    className="p-3 bg-white rounded-lg border border-gray-200 flex items-start justify-between gap-3"
                  >
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <span className={`px-1.5 py-0.5 text-xs font-medium rounded ${getPriorityColor(rec.priority)}`}>
                          {rec.priority}
                        </span>
                        <span className="font-medium text-gray-900 text-sm truncate">{rec.title}</span>
                      </div>
                      <p className="text-xs text-gray-600">
                        {rec.action || rec.rationale}
                        {(rec.impact || rec.expected_impact) && (
                          <span className="text-green-600 font-medium ml-1">
                            → {rec.impact || rec.expected_impact}
                          </span>
                        )}
                      </p>
                    </div>
                    {(rec.effort || rec.estimated_effort) && (
                      <span className="text-xs text-gray-500 whitespace-nowrap">
                        {rec.effort || rec.estimated_effort}
                      </span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Guardrails - Compact warnings */}
          {insights.guardrails && insights.guardrails.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-gray-900 mb-2">⚠️ Guardrails</h3>
              <div className="space-y-1">
                {insights.guardrails.map((guardrail, index) => (
                  <div
                    key={index}
                    className="p-2 bg-amber-50 border-l-3 border-amber-400 rounded-r text-sm"
                  >
                    <span className="font-medium text-gray-900">
                      {guardrail.metric || guardrail.message}
                    </span>
                    {guardrail.threshold && (
                      <span className="text-gray-600 ml-1">— {guardrail.threshold}</span>
                    )}
                    {guardrail.why && (
                      <span className="text-gray-500 text-xs ml-1">({guardrail.why})</span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Experiment - Single compact card */}
          {(insights.experiment || (insights.experiment_suggestions && insights.experiment_suggestions.length > 0)) && (
            <div>
              <h3 className="text-sm font-semibold text-gray-900 mb-2">🧪 Next Experiment</h3>
              <div className="p-3 bg-purple-50 border border-purple-200 rounded-lg text-sm">
                {insights.experiment ? (
                  <>
                    <p className="text-gray-800"><strong>If</strong> {insights.experiment.hypothesis}</p>
                    <p className="text-gray-600 text-xs mt-1">
                      <strong>Test:</strong> {insights.experiment.test} | <strong>Metric:</strong> {insights.experiment.metric}
                    </p>
                  </>
                ) : insights.experiment_suggestions && insights.experiment_suggestions[0] && (
                  <>
                    <p className="text-gray-800"><strong>Hypothesis:</strong> {insights.experiment_suggestions[0].hypothesis}</p>
                    <p className="text-gray-600 text-xs mt-1">
                      <strong>Test:</strong> {insights.experiment_suggestions[0].test_design}
                    </p>
                  </>
                )}
              </div>
            </div>
          )}

          {insights.generated_at && (
            <p className="text-xs text-gray-400 text-right">
              {new Date(insights.generated_at).toLocaleTimeString()}
            </p>
          )}
        </div>
      )}
    </div>
  )
}
