import { useState } from 'react'
import { projectsApi } from '../../services/api'

interface TrackingCodeProps {
  projectId: string
}

export default function TrackingCode({ projectId }: TrackingCodeProps) {
  const [code, setCode] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [copied, setCopied] = useState(false)

  const fetchTrackingCode = async () => {
    setLoading(true)
    try {
      const response = await projectsApi.getTrackingCode(projectId)
      setCode(response.data.tracking_code)
    } catch (error) {
      console.error('Failed to fetch tracking code', error)
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = () => {
    if (code) {
      navigator.clipboard.writeText(code)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">Tracking Code</h3>
      {!code ? (
        <button
          onClick={fetchTrackingCode}
          disabled={loading}
          className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
        >
          {loading ? 'Loading...' : 'Generate Tracking Code'}
        </button>
      ) : (
        <div>
          <div className="mb-4 p-4 bg-gray-50 rounded-md">
            <pre className="text-xs overflow-x-auto">
              <code>{code}</code>
            </pre>
          </div>
          <div className="flex gap-2">
            <button
              onClick={copyToClipboard}
              className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
            >
              {copied ? '✓ Copied!' : 'Copy to Clipboard'}
            </button>
            <button
              onClick={() => setCode(null)}
              className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300"
            >
              Close
            </button>
          </div>
          <p className="mt-4 text-sm text-gray-600">
            Copy and paste this code before the <code className="bg-gray-100 px-1 rounded">&lt;/body&gt;</code> tag
            on your website.
          </p>
        </div>
      )}
    </div>
  )
}
