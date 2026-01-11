import { useEffect, useState } from 'react'
import { funnelsApi, eventsApi } from '../services/api'
import { useProjectStore } from '../store/projectStore'

interface Funnel {
  id: string
  project_id: string
  name: string
  description?: string
  stages: Array<{ order: number; name: string; event_type: string }>
  is_active: boolean
  created_at: string
}

export default function Funnels() {
  const { currentProject } = useProjectStore()
  const [funnels, setFunnels] = useState<Funnel[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [funnelName, setFunnelName] = useState('')
  const [funnelDescription, setFunnelDescription] = useState('')
  const [stages, setStages] = useState<Array<{ order: number; name: string; event_type: string }>>([
    { order: 1, name: '', event_type: '' }
  ])
  const [availableEventTypes, setAvailableEventTypes] = useState<string[]>([])

  useEffect(() => {
    if (currentProject) {
      loadFunnels()
      loadAvailableEventTypes()
    }
  }, [currentProject])
  
  const loadAvailableEventTypes = async () => {
    if (!currentProject) return
    try {
      const response = await eventsApi.getEventTypes(currentProject.id)
      setAvailableEventTypes(response.data)
    } catch (err) {
      // If no data yet, use empty array (will allow any event type)
      setAvailableEventTypes([])
    }
  }

  const loadFunnels = async () => {
    if (!currentProject) return
    setLoading(true)
    setError(null)
    try {
      const response = await funnelsApi.list(currentProject.id)
      setFunnels(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load journeys')
    } finally {
      setLoading(false)
    }
  }

  const handleAddStage = () => {
    if (stages.length >= 5) {
      alert('Maximum 5 stages allowed')
      return
    }
    setStages([...stages, { order: stages.length + 1, name: '', event_type: '' }])
  }

  const handleRemoveStage = (index: number) => {
    if (stages.length <= 1) {
      alert('At least one stage is required')
      return
    }
    const newStages = stages.filter((_, i) => i !== index)
    // Reorder stages
    newStages.forEach((stage, i) => {
      stage.order = i + 1
    })
    setStages(newStages)
  }

  const handleStageChange = (index: number, field: 'name' | 'event_type', value: string) => {
    const newStages = [...stages]
    newStages[index][field] = value
    setStages(newStages)
  }

  const handleCreateFunnel = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!currentProject) {
      setError('Please select a project first')
      return
    }

    // Validate stages
    if (stages.some(s => !s.name || !s.event_type)) {
      setError('All stages must have a name and event type')
      return
    }

    setLoading(true)
    setError(null)
    try {
      await funnelsApi.create({
        project_id: currentProject.id,
        name: funnelName,
        description: funnelDescription || undefined,
        stages: stages.map(s => ({ order: s.order, name: s.name, event_type: s.event_type }))
      })
      setShowCreateForm(false)
      setFunnelName('')
      setFunnelDescription('')
      setStages([{ order: 1, name: '', event_type: '' }])
      loadFunnels()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create journey')
    } finally {
      setLoading(false)
    }
  }

  if (!currentProject) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 mb-4">Please select a project first</p>
          <a href="/projects" className="text-indigo-600 hover:text-indigo-800">
            Go to Projects →
          </a>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#F5F5F5' }}>
      <div className="max-w-7xl mx-auto py-8 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center mb-6 pb-6 border-b" style={{ borderColor: '#E5E7EB' }}>
          <div>
            <h1 className="text-4xl font-bold mb-3" style={{ color: '#111827' }}>Journeys</h1>
            <p className="text-sm" style={{ color: '#6B7280' }}>Create and manage inspiration-to-action journeys</p>
          </div>
          <button
            onClick={() => setShowCreateForm(!showCreateForm)}
            className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
          >
            {showCreateForm ? 'Cancel' : 'Create Journey'}
          </button>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-red-800">{error}</p>
            <button onClick={() => setError(null)} className="mt-2 text-red-600 hover:text-red-800">
              Dismiss
            </button>
          </div>
        )}

        {showCreateForm && (
          <div className="mb-6 p-6 bg-white rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Create New Journey</h2>
            <form onSubmit={handleCreateFunnel}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Journey Name
                </label>
                <input
                  type="text"
                  required
                  value={funnelName}
                  onChange={(e) => setFunnelName(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  placeholder="Pin Discovery to Save"
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Description (optional)
                </label>
                <textarea
                  value={funnelDescription}
                  onChange={(e) => setFunnelDescription(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  rows={2}
                  placeholder="Track users from page view to purchase"
                />
              </div>
              <div className="mb-4">
                <div className="flex justify-between items-center mb-2">
                  <label className="block text-sm font-medium text-gray-700">
                    Journey Stages (max 5)
                  </label>
                  <button
                    type="button"
                    onClick={handleAddStage}
                    disabled={stages.length >= 5}
                    className="text-sm text-indigo-600 hover:text-indigo-800 disabled:text-gray-400"
                  >
                    + Add Stage
                  </button>
                </div>
                {stages.map((stage, index) => (
                  <div key={index} className="mb-3 p-3 border border-gray-200 rounded-md">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm font-medium text-gray-700">Stage {stage.order}</span>
                      {stages.length > 1 && (
                        <button
                          type="button"
                          onClick={() => handleRemoveStage(index)}
                          className="text-sm text-red-600 hover:text-red-800"
                        >
                          Remove
                        </button>
                      )}
                    </div>
                    <div className="grid grid-cols-2 gap-2">
                      <input
                        type="text"
                        required
                        value={stage.name}
                        onChange={(e) => handleStageChange(index, 'name', e.target.value)}
                        className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                        placeholder="Stage Name (e.g., Page View)"
                      />
                      {availableEventTypes.length > 0 ? (
                        <select
                          required
                          value={stage.event_type}
                          onChange={(e) => handleStageChange(index, 'event_type', e.target.value)}
                          className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                        >
                          <option value="">Select event type...</option>
                          {availableEventTypes.map((eventType) => (
                            <option key={eventType} value={eventType}>
                              {eventType}
                            </option>
                          ))}
                        </select>
                      ) : (
                        <input
                          type="text"
                          required
                          value={stage.event_type}
                          onChange={(e) => handleStageChange(index, 'event_type', e.target.value)}
                          className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                          placeholder="Event Type (e.g., pin_view)"
                        />
                      )}
                    </div>
                  </div>
                ))}
              </div>
              <div className="flex gap-2">
                <button
                  type="submit"
                  disabled={loading}
                  className="px-4 py-2 text-white rounded-full font-semibold shadow-sm transition-all hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
                  style={{ backgroundColor: '#E60023' }}
                  onMouseEnter={(e) => !loading && (e.currentTarget.style.backgroundColor = '#BD001F')}
                  onMouseLeave={(e) => !loading && (e.currentTarget.style.backgroundColor = '#E60023')}
                >
                    {loading ? 'Creating...' : 'Create Journey'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowCreateForm(false)
                    setFunnelName('')
                    setFunnelDescription('')
                    setStages([{ order: 1, name: '', event_type: '' }])
                  }}
                  className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {loading && !funnels.length ? (
          <div className="text-center py-12">
            <p className="text-gray-500">Loading journeys...</p>
          </div>
        ) : funnels.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <p className="text-gray-500 mb-4">No journeys yet. Create your first journey!</p>
          </div>
        ) : (
          <div className="grid gap-4">
            {funnels.map((funnel) => (
              <div key={funnel.id} className="p-6 bg-white rounded-lg shadow">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-semibold text-gray-900">{funnel.name}</h3>
                    {funnel.description && (
                      <p className="text-sm text-gray-500 mt-1">{funnel.description}</p>
                    )}
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm ${
                    funnel.is_active 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-gray-100 text-gray-800'
                  }`}>
                    {funnel.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>
                <div className="border-t border-gray-200 pt-4">
                  <h4 className="text-sm font-medium text-gray-700 mb-2">Stages:</h4>
                  <div className="space-y-2">
                    {funnel.stages.map((stage, idx) => (
                      <div key={idx} className="flex items-center gap-3 text-sm">
                        <span className="w-8 h-8 flex items-center justify-center bg-indigo-100 text-indigo-800 rounded-full font-medium">
                          {stage.order}
                        </span>
                        <span className="font-medium text-gray-900">{stage.name}</span>
                        <span className="text-gray-500">→</span>
                        <code className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
                          {stage.event_type}
                        </code>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <a
                    href={`/dashboard?funnel=${funnel.id}`}
                    className="text-sm font-semibold hover:underline"
                    style={{ color: '#E60023' }}
                    onMouseEnter={(e) => e.currentTarget.style.color = '#BD001F'}
                    onMouseLeave={(e) => e.currentTarget.style.color = '#E60023'}
                  >
                    View Analytics →
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
