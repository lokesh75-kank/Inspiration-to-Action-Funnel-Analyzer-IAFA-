import { useState, useEffect } from 'react'
import { analyticsApi } from '../../services/api'

interface AIInsights {
  insights?: string[]
  recommendations?: Array<{
    priority: string
    title: string
    rationale: string
    expected_impact: string
    action_items: string[]
    estimated_effort?: string
    risk_level?: string
  }>
  guardrails?: Array<{
    type: string
    severity: string
    message: string
    metric?: string
    recommendation?: string
  }>
  experiment_suggestions?: Array<{
    hypothesis: string
    test_design: string
    success_metrics: string[]
    expected_outcome: string
    duration?: string
    sample_size?: string
  }>
  summary?: {
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
  const [expandedRecommendations, setExpandedRecommendations] = useState<Set<number>>(new Set())

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

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'high':
        return 'text-red-600'
      case 'medium':
        return 'text-yellow-600'
      case 'low':
        return 'text-blue-600'
      default:
        return 'text-gray-600'
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
          {/* Insights */}
          {insights.insights && insights.insights.length > 0 && (
            <div>
              <h3 className="text-md font-semibold text-gray-900 mb-2">💡 Key Insights</h3>
              <ul className="space-y-1">
                {insights.insights.map((insight, index) => (
                  <li key={index} className="text-sm text-gray-700 flex items-start">
                    <span className="mr-2">•</span>
                    <span>{insight}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Recommendations */}
          {insights.recommendations && insights.recommendations.length > 0 && (
            <div>
              <h3 className="text-md font-semibold text-gray-900 mb-3">⭐ Recommendations</h3>
              <div className="space-y-3">
                {insights.recommendations.map((rec, index) => {
                  const isExpanded = expandedRecommendations.has(index)
                  return (
                    <div
                      key={index}
                      className="p-4 bg-white rounded-lg border border-gray-200"
                    >
                      <div className="flex items-start justify-between mb-2">
                        <h4 className="font-semibold text-gray-900 flex-1">{rec.title}</h4>
                        <div className="flex items-center gap-2">
                          <span
                            className={`px-2 py-1 text-xs font-medium rounded border ${getPriorityColor(rec.priority)}`}
                          >
                            {rec.priority} Priority
                          </span>
                          <button
                            onClick={() => {
                              const newExpanded = new Set(expandedRecommendations)
                              if (isExpanded) {
                                newExpanded.delete(index)
                              } else {
                                newExpanded.add(index)
                              }
                              setExpandedRecommendations(newExpanded)
                            }}
                            className="text-xs text-gray-500 hover:text-gray-700"
                          >
                            {isExpanded ? '▼' : '▶'}
                          </button>
                        </div>
                      </div>
                      {isExpanded && (
                        <>
                          <p className="text-sm text-gray-700 mb-2">{rec.rationale}</p>
                          <div className="flex items-center gap-4 text-xs text-gray-600 mb-2 flex-wrap">
                            {rec.expected_impact && (
                              <span className="bg-green-50 px-2 py-1 rounded">
                                <strong>Expected Impact:</strong> {rec.expected_impact}
                              </span>
                            )}
                            {rec.estimated_effort && (
                              <span><strong>Effort:</strong> {rec.estimated_effort}</span>
                            )}
                            {rec.risk_level && (
                              <span><strong>Risk:</strong> {rec.risk_level}</span>
                            )}
                          </div>
                          {rec.action_items && rec.action_items.length > 0 && (
                            <div className="mt-2">
                              <p className="text-xs font-semibold text-gray-600 mb-1">Action Items:</p>
                              <ul className="list-disc list-inside text-xs text-gray-700 space-y-1">
                                {rec.action_items.map((item, itemIndex) => (
                                  <li key={itemIndex}>{item}</li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </>
                      )}
                    </div>
                  )
                })}
              </div>
            </div>
          )}

          {/* Guardrails */}
          {insights.guardrails && insights.guardrails.length > 0 && (
            <div>
              <h3 className="text-md font-semibold text-gray-900 mb-2">⚠️ Guardrails</h3>
              <div className="space-y-2">
                {insights.guardrails.map((guardrail, index) => (
                  <div
                    key={index}
                    className="p-3 bg-yellow-50 border border-yellow-200 rounded-md"
                  >
                    <div className="flex items-start justify-between mb-1">
                      <p className="text-sm font-medium text-gray-900">{guardrail.message}</p>
                      <span className={`text-xs font-medium ${getSeverityColor(guardrail.severity)}`}>
                        {guardrail.severity} Severity
                      </span>
                    </div>
                    {guardrail.metric && (
                      <p className="text-xs text-gray-600 mb-1">Metric: {guardrail.metric}</p>
                    )}
                    {guardrail.recommendation && (
                      <p className="text-xs text-gray-700">{guardrail.recommendation}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Experiment Suggestions */}
          {insights.experiment_suggestions && insights.experiment_suggestions.length > 0 && (
            <div>
              <h3 className="text-md font-semibold text-gray-900 mb-3">🧪 Experiment Suggestions</h3>
              <div className="space-y-3">
                {insights.experiment_suggestions.map((exp, index) => (
                  <div
                    key={index}
                    className="p-4 bg-purple-50 border border-purple-200 rounded-lg"
                  >
                    <h4 className="font-semibold text-gray-900 mb-2">Hypothesis: {exp.hypothesis}</h4>
                    <div className="space-y-2 text-sm">
                      <p className="text-gray-700">
                        <strong>Test Design:</strong> {exp.test_design}
                      </p>
                      {exp.success_metrics && exp.success_metrics.length > 0 && (
                        <div>
                          <strong className="text-gray-700">Success Metrics:</strong>
                          <ul className="list-disc list-inside text-gray-600 ml-2">
                            {exp.success_metrics.map((metric, mIndex) => (
                              <li key={mIndex}>{metric}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      {exp.expected_outcome && (
                        <p className="text-gray-700">
                          <strong>Expected Outcome:</strong> {exp.expected_outcome}
                        </p>
                      )}
                      <div className="flex gap-4 text-xs text-gray-600">
                        {exp.duration && (
                          <span><strong>Duration:</strong> {exp.duration}</span>
                        )}
                        {exp.sample_size && (
                          <span><strong>Sample Size:</strong> {exp.sample_size}</span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Summary */}
          {insights.summary && (
            <div className="p-4 bg-blue-50 border border-blue-200 rounded-md">
              <h3 className="text-md font-semibold text-gray-900 mb-2">📝 Summary</h3>
              {insights.summary.executive && (
                <p className="text-sm text-gray-700 mb-2">{insights.summary.executive}</p>
              )}
              {insights.summary.technical && (
                <details className="mt-2">
                  <summary className="text-xs font-semibold text-gray-600 cursor-pointer">Technical Details</summary>
                  <p className="text-xs text-gray-600 mt-1">{insights.summary.technical}</p>
                </details>
              )}
            </div>
          )}

          {insights.generated_at && (
            <p className="text-xs text-gray-500 text-right">
              Generated: {new Date(insights.generated_at).toLocaleString()}
            </p>
          )}
        </div>
      )}
    </div>
  )
}
