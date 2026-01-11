import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { analyticsApi, funnelsApi } from '../services/api'
import { useProjectStore } from '../store/projectStore'
import DatePicker from 'react-datepicker'
import 'react-datepicker/dist/react-datepicker.css'
import ChartSwitcher from '../components/charts/ChartSwitcher'
import ExportReportButton from '../components/ui/ExportReportButton'
import { ReportData } from '../utils/reportGenerator'

interface Funnel {
  id: string
  name: string
  stages: Array<{ order: number; name: string; event_type: string }>
}

interface StageMetrics {
  stage_name: string
  stage_order: number
  users: number
  conversion_rate: number
  drop_off_rate: number
}

interface FunnelAnalytics {
  funnel_id: string
  funnel_name: string
  date_range: { start: string; end: string }
  stages?: StageMetrics[]
  overall_conversion_rate?: number
  total_users?: number
  completed_users?: number
  // Segment breakdown (Phase 2)
  segment_by?: string
  segments?: Record<string, {
    stages: StageMetrics[]
    total_users: number
    completed_users: number
    overall_conversion_rate: number
  }>
  total?: {
    stages: StageMetrics[]
    total_users: number
    completed_users: number
    overall_conversion_rate: number
  }
}

// Convert analytics data to report format
function convertAnalyticsToReportData(analytics: FunnelAnalytics): ReportData {
  if (analytics.segments && analytics.total) {
    // Segment breakdown mode
    return {
      funnel_name: analytics.funnel_name,
      date_range: analytics.date_range,
      total_users: analytics.total.total_users,
      completed_users: analytics.total.completed_users,
      overall_conversion_rate: analytics.total.overall_conversion_rate,
      stages: analytics.total.stages.map(stage => ({
        stage_name: stage.stage_name,
        users: stage.users,
        conversion_rate: stage.conversion_rate,
        drop_off_rate: stage.drop_off_rate,
      })),
      segments: Object.entries(analytics.segments).reduce((acc, [key, value]) => {
        acc[key] = {
          total_users: value.total_users,
          completed_users: value.completed_users,
          overall_conversion_rate: value.overall_conversion_rate,
          stages: value.stages.map(stage => ({
            stage_name: stage.stage_name,
            users: stage.users,
            conversion_rate: stage.conversion_rate,
          })),
        }
        return acc
      }, {} as Record<string, any>),
      segment_by: analytics.segment_by,
    }
  } else {
    // Regular mode
    return {
      funnel_name: analytics.funnel_name,
      date_range: analytics.date_range,
      total_users: analytics.total_users,
      completed_users: analytics.completed_users,
      overall_conversion_rate: analytics.overall_conversion_rate,
      stages: analytics.stages?.map(stage => ({
        stage_name: stage.stage_name,
        users: stage.users,
        conversion_rate: stage.conversion_rate,
        drop_off_rate: stage.drop_off_rate,
      })),
    }
  }
}

export default function Dashboard() {
  const { currentProject, fetchProjects, loading: projectsLoading } = useProjectStore()
  const [searchParams, setSearchParams] = useSearchParams()
  const [funnels, setFunnels] = useState<Funnel[]>([])
  const [selectedFunnelId, setSelectedFunnelId] = useState<string | null>(
    searchParams.get('funnel') || null
  )
  const [analytics, setAnalytics] = useState<FunnelAnalytics | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [startDate, setStartDate] = useState<Date>(new Date(Date.now() - 30 * 24 * 60 * 60 * 1000))
  const [endDate, setEndDate] = useState<Date>(new Date())
  
  // Segment filters (Phase 2)
  const [userIntent, setUserIntent] = useState<string[]>([])
  const [contentCategory, setContentCategory] = useState<string[]>([])
  const [surface, setSurface] = useState<string[]>([])
  const [userTenure, setUserTenure] = useState<string[]>([])
  const [segmentBy, setSegmentBy] = useState<string>('')

  // Fetch projects on mount (this will auto-select the first project)
  useEffect(() => {
    if (!currentProject) {
      fetchProjects()
    }
  }, [currentProject, fetchProjects])

  useEffect(() => {
    if (currentProject) {
      loadFunnels()
    }
  }, [currentProject])

  useEffect(() => {
    if (selectedFunnelId && currentProject) {
      loadAnalytics()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedFunnelId, startDate, endDate, currentProject?.id, JSON.stringify(userIntent), JSON.stringify(contentCategory), JSON.stringify(surface), JSON.stringify(userTenure), segmentBy])

  const loadFunnels = async () => {
    if (!currentProject) return
    try {
      const response = await funnelsApi.list(currentProject.id)
      setFunnels(response.data)
      if (response.data.length > 0 && !selectedFunnelId) {
        setSelectedFunnelId(response.data[0].id)
      }
    } catch (err) {
      console.error('Failed to load funnels', err)
    }
  }

  const loadAnalytics = async () => {
    if (!selectedFunnelId) return
    setLoading(true)
    setError(null)
    try {
      const response = await analyticsApi.getFunnelAnalytics(
        selectedFunnelId,
        startDate.toISOString().split('T')[0],
        endDate.toISOString().split('T')[0],
        {
          user_intent: userIntent.length > 0 ? userIntent : undefined,
          content_category: contentCategory.length > 0 ? contentCategory : undefined,
          surface: surface.length > 0 ? surface : undefined,
          user_tenure: userTenure.length > 0 ? userTenure : undefined,
          segment_by: segmentBy || undefined,
        }
      )
      setAnalytics(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load analytics')
    } finally {
      setLoading(false)
    }
  }

  // Show loading while fetching projects
  if (projectsLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 mb-4">Loading projects...</p>
        </div>
      </div>
    )
  }

  // Show no project state if loading is done and no project found
  if (!currentProject) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 mb-4">No projects found. The default Pinterest project should be created automatically.</p>
          <p className="text-sm text-gray-500 mb-4">If you see this message, please check:</p>
          <ul className="text-sm text-gray-500 mb-4 text-left inline-block">
            <li>1. Backend server is running (port 8000)</li>
            <li>2. Default project exists in backend</li>
            <li>3. API is accessible</li>
          </ul>
          <a href="/projects" className="text-indigo-600 hover:text-indigo-800 underline">
            Go to Projects →
          </a>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#F5F5F5' }}>
      <div className="max-w-7xl mx-auto py-8 sm:px-6 lg:px-8">
        <div className="mb-8 pb-6 border-b" style={{ borderColor: '#E5E7EB' }}>
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-4xl font-bold mb-3" style={{ color: '#111827' }}>Journey Overview</h1>
              <p className="text-sm" style={{ color: '#6B7280' }}>Analyze inspiration-to-action journeys with segment-level insights</p>
            </div>
            {analytics && (
              <div className="mt-2">
                <ExportReportButton data={convertAnalyticsToReportData(analytics)} />
              </div>
            )}
          </div>
        </div>

        {/* Journey Selector */}
        <div className="mb-6 p-5 rounded-xl shadow-sm border border-gray-200" style={{ backgroundColor: '#FAFAFA' }}>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Select Journey
          </label>
          <select
            value={selectedFunnelId || ''}
            onChange={(e) => {
              const funnelId = e.target.value || null
              setSelectedFunnelId(funnelId)
              if (funnelId) {
                setSearchParams({ funnel: funnelId })
              } else {
                setSearchParams({})
              }
            }}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="">-- Select a journey --</option>
            {funnels.map((funnel) => (
              <option key={funnel.id} value={funnel.id}>
                {funnel.name}
              </option>
            ))}
          </select>
        </div>

        {/* Date Range Selector */}
        {selectedFunnelId && (
          <div className="mb-6 p-5 bg-white rounded-xl shadow-sm border border-gray-200">
            <h3 className="text-sm font-medium text-gray-900 mb-4">Date Range</h3>
            <div className="flex gap-4 items-center">
              <div>
                <label className="block text-xs text-gray-500 mb-1">Start Date</label>
                <DatePicker
                  selected={startDate}
                  onChange={(date: Date) => setStartDate(date)}
                  selectsStart
                  startDate={startDate}
                  endDate={endDate}
                  className="px-3 py-2 border border-gray-300 rounded-md"
                />
              </div>
              <div>
                <label className="block text-xs text-gray-500 mb-1">End Date</label>
                <DatePicker
                  selected={endDate}
                  onChange={(date: Date) => setEndDate(date)}
                  selectsEnd
                  startDate={startDate}
                  endDate={endDate}
                  minDate={startDate}
                  className="px-3 py-2 border border-gray-300 rounded-md"
                />
              </div>
            </div>
          </div>
        )}

        {/* Segment Filters (Phase 2) */}
        {selectedFunnelId && (
          <div className="mb-6 p-5 rounded-xl shadow-sm border border-gray-200" style={{ backgroundColor: '#FAFAFA' }}>
            <h3 className="text-sm font-medium text-gray-900 mb-4">Segment Filters</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
              {/* User Intent Filter */}
              <div>
                <label className="block text-xs text-gray-500 mb-1">User Intent</label>
                <select
                  multiple
                  value={userIntent}
                  onChange={(e) => {
                    const values = Array.from(e.target.selectedOptions, option => option.value)
                    setUserIntent(values)
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                  size={4}
                >
                  <option value="Browser">Browser</option>
                  <option value="Planner">Planner</option>
                  <option value="Actor">Actor</option>
                  <option value="Curator">Curator</option>
                </select>
                {userIntent.length > 0 && (
                  <button
                    onClick={() => setUserIntent([])}
                    className="mt-1 text-xs text-indigo-600 hover:text-indigo-800"
                  >
                    Clear
                  </button>
                )}
              </div>

              {/* Surface Filter */}
              <div>
                <label className="block text-xs text-gray-500 mb-1">Surface</label>
                <select
                  multiple
                  value={surface}
                  onChange={(e) => {
                    const values = Array.from(e.target.selectedOptions, option => option.value)
                    setSurface(values)
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                  size={4}
                >
                  <option value="Home">Home</option>
                  <option value="Search">Search</option>
                  <option value="Boards">Boards</option>
                  <option value="Profile">Profile</option>
                </select>
                {surface.length > 0 && (
                  <button
                    onClick={() => setSurface([])}
                    className="mt-1 text-xs text-indigo-600 hover:text-indigo-800"
                  >
                    Clear
                  </button>
                )}
              </div>

              {/* User Tenure Filter */}
              <div>
                <label className="block text-xs text-gray-500 mb-1">User Tenure</label>
                <select
                  multiple
                  value={userTenure}
                  onChange={(e) => {
                    const values = Array.from(e.target.selectedOptions, option => option.value)
                    setUserTenure(values)
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                  size={3}
                >
                  <option value="New">New</option>
                  <option value="Retained">Retained</option>
                </select>
                {userTenure.length > 0 && (
                  <button
                    onClick={() => setUserTenure([])}
                    className="mt-1 text-xs text-indigo-600 hover:text-indigo-800"
                  >
                    Clear
                  </button>
                )}
              </div>

              {/* Content Category Filter */}
              <div>
                <label className="block text-xs text-gray-500 mb-1">Content Category</label>
                <input
                  type="text"
                  placeholder="e.g., home_decor, recipes"
                  value={contentCategory.join(',')}
                  onChange={(e) => {
                    const values = e.target.value.split(',').map(s => s.trim()).filter(s => s)
                    setContentCategory(values)
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                />
                <p className="text-xs text-gray-400 mt-1">Comma-separated</p>
              </div>

              {/* Segment By (Breakdown) */}
              <div>
                <label className="block text-xs text-gray-500 mb-1">Break Down By</label>
                <select
                  value={segmentBy}
                  onChange={(e) => setSegmentBy(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                >
                  <option value="">None (Aggregate)</option>
                  <option value="user_intent">User Intent</option>
                  <option value="surface">Surface</option>
                  <option value="user_tenure">User Tenure</option>
                  <option value="content_category">Content Category</option>
                </select>
              </div>
            </div>
            <div className="mt-4">
              <button
                onClick={() => {
                  setUserIntent([])
                  setContentCategory([])
                  setSurface([])
                  setUserTenure([])
                  setSegmentBy('')
                }}
                className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 text-sm"
              >
                Clear All Filters
              </button>
            </div>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-red-800">{error}</p>
          </div>
        )}

        {/* Analytics Display */}
        {loading ? (
          <div className="text-center py-12">
            <p className="text-gray-500">Loading analytics...</p>
          </div>
        ) : analytics ? (
          <div className="space-y-6">
            {/* Check if we have segment breakdown */}
            {analytics.segments && analytics.segment_by ? (
              /* Segment Breakdown View (Phase 2) */
              <>
                {/* Total Summary Cards */}
                {analytics.total && (
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="p-6 bg-white rounded-lg shadow">
                      <p className="text-sm text-gray-500">Total Users (All Segments)</p>
                      <p className="text-3xl font-bold text-gray-900 mt-2">
                        {analytics.total.total_users.toLocaleString()}
                      </p>
                    </div>
                    <div className="p-6 bg-white rounded-lg shadow">
                      <p className="text-sm text-gray-500">Completed Users (All Segments)</p>
                      <p className="text-3xl font-bold text-gray-900 mt-2">
                        {analytics.total.completed_users.toLocaleString()}
                      </p>
                    </div>
                    <div className="p-6 bg-white rounded-lg shadow">
                      <p className="text-sm text-gray-500">Overall Conversion Rate</p>
                      <p className="text-3xl font-bold text-indigo-600 mt-2">
                        {analytics.total.overall_conversion_rate.toFixed(2)}%
                      </p>
                    </div>
                  </div>
                )}


                {/* Segment Comparison */}
                <div className="p-6 bg-white rounded-lg shadow">
                  <h2 className="text-xl font-semibold mb-4">
                    Segment Breakdown: {analytics.segment_by?.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()) || ''}
                  </h2>
                  <div className="space-y-6">
                    {Object.entries(analytics.segments).map(([segmentValue, segmentData]) => (
                      <div key={segmentValue} className="border border-gray-200 rounded-lg p-4">
                        <h3 className="text-lg font-semibold text-gray-900 mb-3">
                          {segmentValue} ({segmentData.total_users} users, {segmentData.overall_conversion_rate.toFixed(2)}% conversion)
                        </h3>
                        <div className="space-y-3">
                          {segmentData.stages.map((stage, index) => {
                            const widthPercent = stage.conversion_rate
                            const isLast = index === segmentData.stages.length - 1
                            const nextStage = !isLast ? segmentData.stages[index + 1] : null
                            const dropOffRate = nextStage ? nextStage.drop_off_rate : 0
                            return (
                              <div key={stage.stage_order} className="relative">
                                <div className="flex items-center gap-4 mb-2">
                                  <div className="w-32 text-sm font-medium text-gray-700">
                                    {stage.stage_name}
                                  </div>
                                  <div className="flex-1">
                                    <div className="relative h-10">
                                      <div
                                        className="h-10 rounded transition-all absolute top-0 left-0"
                                        style={{ width: `${widthPercent}%`, backgroundColor: '#E60023' }}
                                      />
                                      {widthPercent >= 15 ? (
                                        <div className="absolute inset-0 flex items-center justify-center text-white font-semibold text-xs z-10">
                                          {stage.users.toLocaleString()} ({stage.conversion_rate.toFixed(1)}%)
                                        </div>
                                      ) : (
                                        <div 
                                          className="absolute top-0 left-0 flex items-center h-full text-gray-700 font-semibold text-xs z-10 whitespace-nowrap"
                                          style={{ left: `${Math.max(widthPercent + 1, 0)}%`, paddingLeft: '8px' }}
                                        >
                                          {stage.users.toLocaleString()} ({stage.conversion_rate.toFixed(1)}%)
                                        </div>
                                      )}
                                    </div>
                                  </div>
                                </div>
                                {!isLast && (
                                  <div className="ml-32 text-xs text-red-600 mb-2">
                                    ↓ {dropOffRate.toFixed(1)}% drop-off
                                  </div>
                                )}
                              </div>
                            )
                          })}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Segment Comparison Table */}
                <div className="p-6 bg-white rounded-xl shadow-lg border border-gray-100">
                  <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                    <span className="w-1 h-8 bg-gradient-to-b from-indigo-500 to-purple-500 rounded-full mr-3"></span>
                    Segment Comparison
                  </h2>
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Segment</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Total Users</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Completed</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Conversion Rate</th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {Object.entries(analytics.segments).map(([segmentValue, segmentData]) => (
                          <tr key={segmentValue}>
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                              {segmentValue}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {segmentData.total_users.toLocaleString()}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {segmentData.completed_users.toLocaleString()}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-indigo-600">
                              {segmentData.overall_conversion_rate.toFixed(2)}%
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </>
            ) : (
              /* Regular Aggregate View */
              <>
                {/* Summary Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                  <div className="p-5 bg-white rounded-xl shadow-sm border border-gray-200">
                    <p className="text-sm font-medium text-gray-600">Total Users</p>
                    <p className="text-2xl font-semibold text-gray-900 mt-2">
                      {(analytics.total_users || 0).toLocaleString()}
                    </p>
                  </div>
                  <div className="p-5 bg-white rounded-xl shadow-sm border border-gray-200">
                    <p className="text-sm font-medium text-gray-600">Completed Users</p>
                    <p className="text-2xl font-semibold text-gray-900 mt-2">
                      {(analytics.completed_users || 0).toLocaleString()}
                    </p>
                  </div>
                  <div className="p-5 bg-white rounded-xl shadow-sm border border-gray-200">
                    <p className="text-sm font-medium text-gray-600">Overall Conversion Rate</p>
                    <p className="text-2xl font-semibold mt-2" style={{ color: '#E60023' }}>
                      {(analytics.overall_conversion_rate || 0).toFixed(2)}%
                    </p>
                  </div>
                </div>

                {/* Funnel Visualization */}
                {analytics.stages && analytics.stages.length > 0 && (
                  <>
                    {/* Chart Switcher - Switch between different chart views */}
                    <div className="mb-6">
                      <ChartSwitcher 
                        stages={analytics.stages}
                        segments={analytics.segments}
                      />
                    </div>

                    {/* Stage-by-Stage Breakdown */}
                    <div className="p-6 rounded-xl shadow-sm border border-gray-200" style={{ backgroundColor: '#FAFAFA' }}>
                      <h2 className="text-lg font-semibold text-gray-900 mb-6">Journey Stages</h2>
                      <div className="space-y-4">
                        {analytics.stages.map((stage, index) => {
                          const widthPercent = stage.conversion_rate
                          const isLast = index === analytics.stages!.length - 1
                          const nextStage = !isLast ? analytics.stages![index + 1] : null
                          const dropOffRate = nextStage ? nextStage.drop_off_rate : 0
                          return (
                            <div key={stage.stage_order} className="relative">
                              <div className="flex items-center gap-4 mb-2">
                                <div className="w-32 text-sm font-medium text-gray-700">
                                  {stage.stage_name}
                                </div>
                                <div className="flex-1">
                                  <div className="relative h-12">
                                    <div
                                      className="h-12 bg-indigo-600 rounded transition-all absolute top-0 left-0"
                                      style={{ width: `${widthPercent}%` }}
                                    />
                                    {widthPercent >= 15 ? (
                                      <div className="absolute inset-0 flex items-center justify-center text-white font-semibold z-10">
                                        {stage.users.toLocaleString()} users ({stage.conversion_rate.toFixed(1)}%)
                                      </div>
                                    ) : (
                                      <div 
                                        className="absolute top-0 left-0 flex items-center h-full text-gray-700 font-semibold z-10 whitespace-nowrap"
                                        style={{ left: `${Math.max(widthPercent + 1, 0)}%`, paddingLeft: '8px' }}
                                      >
                                        {stage.users.toLocaleString()} users ({stage.conversion_rate.toFixed(1)}%)
                                      </div>
                                    )}
                                  </div>
                                </div>
                              </div>
                              {!isLast && (
                                <div className="ml-32 text-xs text-red-600 mb-2">
                                  ↓ {dropOffRate.toFixed(1)}% drop-off
                                </div>
                              )}
                            </div>
                          )
                        })}
                      </div>
                    </div>

                    {/* Stage Details Table */}
                    <div className="p-6 bg-white rounded-lg shadow">
                      <h2 className="text-xl font-semibold mb-4">Stage Details</h2>
                      <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-gray-200">
                          <thead className="bg-gray-50">
                            <tr>
                              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Stage</th>
                              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Users</th>
                              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Conversion Rate</th>
                              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Drop-off Rate</th>
                            </tr>
                          </thead>
                          <tbody className="bg-white divide-y divide-gray-200">
                            {analytics.stages.map((stage) => (
                              <tr key={stage.stage_order}>
                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                  {stage.stage_name}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                  {stage.users.toLocaleString()}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                  {stage.conversion_rate.toFixed(2)}%
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-red-600">
                                  {stage.drop_off_rate.toFixed(2)}%
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </>
                )}
              </>
            )}
          </div>
        ) : selectedFunnelId ? (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <p className="text-gray-500">No analytics data available for selected date range.</p>
            <p className="text-sm text-gray-400 mt-2">Try tracking some events first!</p>
          </div>
        ) : (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <p className="text-gray-500">Please select a journey to view analytics.</p>
          </div>
        )}
      </div>
    </div>
  )
}
