import { useState, useEffect } from 'react'
import { analyticsApi } from '../../services/api'

interface ReportPreviewModalProps {
  isOpen: boolean
  onClose: () => void
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
  audience?: string
  format?: string
  onExport: (content: string, format: string) => void
}

export default function ReportPreviewModal({
  isOpen,
  onClose,
  funnelId,
  startDate,
  endDate,
  filters = {},
  audience: initialAudience = 'data_scientist',
  format: initialFormat = 'html',
  onExport
}: ReportPreviewModalProps) {
  const [report, setReport] = useState<string>('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [audience, setAudience] = useState(initialAudience)
  const [format, setFormat] = useState(initialFormat)

  useEffect(() => {
    if (isOpen && funnelId) {
      generateReport()
    }
  }, [isOpen, funnelId, startDate, endDate, audience, format])

  const generateReport = async () => {
    if (!funnelId || !startDate || !endDate) {
      setError('Missing required parameters')
      return
    }

    setLoading(true)
    setError(null)
    setReport('')

    try {
      const response = await analyticsApi.generateAIReport(
        funnelId,
        startDate,
        endDate,
        filters,
        'poc-org',
        audience,
        format
      )

      if (response.data.error) {
        setError(response.data.error)
      } else {
        setReport(response.data.report || '')
      }
    } catch (err: any) {
      console.error('Failed to generate report:', err)
      setError(err.response?.data?.detail || 'Failed to generate report. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleExport = () => {
    if (report) {
      onExport(report, format)
      onClose()
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-xl max-w-4xl w-full max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex-1">
            <h2 className="text-xl font-semibold text-gray-900">AI Report Preview</h2>
            <div className="flex items-center gap-4 mt-3">
              <div>
                <label className="text-xs font-medium text-gray-600 mb-1 block">Audience</label>
                <select
                  value={audience}
                  onChange={(e) => {
                    setAudience(e.target.value)
                    setReport('')
                    setError(null)
                    // Regenerate with new audience
                    setTimeout(() => {
                      generateReport()
                    }, 100)
                  }}
                  className="text-sm border border-gray-300 rounded-lg px-3 py-1.5 bg-white"
                >
                  <option value="data_scientist">Data Scientist</option>
                  <option value="executive">Executive</option>
                  <option value="product_manager">Product Manager</option>
                </select>
              </div>
              <div>
                <label className="text-xs font-medium text-gray-600 mb-1 block">Format</label>
                <select
                  value={format}
                  onChange={(e) => {
                    setFormat(e.target.value)
                    setReport('')
                    setError(null)
                    // Regenerate with new format
                    setTimeout(() => {
                      generateReport()
                    }, 100)
                  }}
                  className="text-sm border border-gray-300 rounded-lg px-3 py-1.5 bg-white"
                >
                  <option value="html">HTML</option>
                  <option value="markdown">Markdown</option>
                  <option value="text">Text</option>
                </select>
              </div>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-2xl ml-4"
          >
            ×
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto p-6">
          {loading && (
            <div className="flex items-center justify-center py-12">
              <div className="text-center">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-[#E60023] mb-4"></div>
                <p className="text-gray-600">Generating AI report...</p>
              </div>
            </div>
          )}

          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800 text-sm">{error}</p>
            </div>
          )}

          {report && !loading && (
            <div className="prose max-w-none">
              {format === 'html' ? (
                <div dangerouslySetInnerHTML={{ __html: report }} />
              ) : (
                <pre className="whitespace-pre-wrap font-mono text-sm bg-gray-50 p-4 rounded-lg border border-gray-200">
                  {report}
                </pre>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between p-6 border-t border-gray-200 bg-gray-50">
          <button
            onClick={generateReport}
            disabled={loading}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
          >
            {loading ? 'Generating...' : 'Regenerate'}
          </button>
          <div className="flex gap-3">
            <button
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              onClick={handleExport}
              disabled={!report || loading}
              className="px-4 py-2 text-sm font-semibold text-white rounded-lg transition-colors disabled:opacity-50"
              style={{ backgroundColor: '#E60023' }}
              onMouseEnter={(e) => {
                if (!e.currentTarget.disabled) {
                  e.currentTarget.style.backgroundColor = '#BD001F'
                }
              }}
              onMouseLeave={(e) => {
                if (!e.currentTarget.disabled) {
                  e.currentTarget.style.backgroundColor = '#E60023'
                }
              }}
            >
              Export Report
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
