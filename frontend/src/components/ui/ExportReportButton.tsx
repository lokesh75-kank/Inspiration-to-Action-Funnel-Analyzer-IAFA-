import { useState, useRef, useEffect } from 'react'
import { generateTextReport, generateCSVReport, generateHTMLReport, ReportData } from '../../utils/reportGenerator'

interface ExportReportButtonProps {
  data: ReportData
}

export default function ExportReportButton({ data }: ExportReportButtonProps) {
  const [exporting, setExporting] = useState(false)
  const [showMenu, setShowMenu] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setShowMenu(false)
      }
    }

    if (showMenu) {
      document.addEventListener('mousedown', handleClickOutside)
      return () => document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [showMenu])

  const handleExport = async (format: 'text' | 'csv' | 'html') => {
    setExporting(true)
    try {
      let content: string
      let mimeType: string
      let extension: string

      switch (format) {
        case 'text':
          content = generateTextReport(data)
          mimeType = 'text/plain'
          extension = 'txt'
          break
        case 'csv':
          content = generateCSVReport(data)
          mimeType = 'text/csv'
          extension = 'csv'
          break
        case 'html':
          content = generateHTMLReport(data)
          mimeType = 'text/html'
          extension = 'html'
          break
      }

      // Create blob and download
      const blob = new Blob([content], { type: mimeType })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      
      // Generate filename
      const funnelName = data.funnel_name.replace(/[^a-z0-9]/gi, '_').toLowerCase()
      const dateStr = new Date().toISOString().split('T')[0]
      link.download = `iafa_report_${funnelName}_${dateStr}.${extension}`
      
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Export failed:', error)
      alert('Failed to export report. Please try again.')
    } finally {
      setExporting(false)
    }
  }

  return (
    <div className="relative">
      <div className="relative" ref={menuRef}>
        <button
          onClick={() => setShowMenu(!showMenu)}
          disabled={exporting}
          className="inline-flex items-center px-4 py-2 rounded-full text-sm font-semibold text-white transition-colors"
          style={{ backgroundColor: '#E60023' }}
          onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#BD001F'}
          onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#E60023'}
        >
        {exporting ? (
          <>
            <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Exporting...
          </>
        ) : (
          <>
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            Export Report
          </>
        )}
        </button>
        
        {/* Dropdown Menu */}
        {showMenu && (
          <div
            className="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg border border-gray-200 z-10"
            style={{ minWidth: '200px' }}
          >
            <div className="py-1">
              <button
                onClick={() => {
                  handleExport('html')
                  setShowMenu(false)
                }}
                className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                <div className="font-medium">Export as HTML</div>
                <div className="text-xs text-gray-500">Formatted report for sharing</div>
              </button>
              <button
                onClick={() => {
                  handleExport('csv')
                  setShowMenu(false)
                }}
                className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                <div className="font-medium">Export as CSV</div>
                <div className="text-xs text-gray-500">Data for Excel/Sheets</div>
              </button>
              <button
                onClick={() => {
                  handleExport('text')
                  setShowMenu(false)
                }}
                className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                <div className="font-medium">Export as Text</div>
                <div className="text-xs text-gray-500">Plain text format</div>
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
