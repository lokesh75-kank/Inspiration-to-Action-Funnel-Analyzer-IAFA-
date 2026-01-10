import { useEffect, useState } from 'react'
import { useProjectStore } from '../store/projectStore'
import TrackingCode from '../components/funnel/TrackingCode'

export default function Projects() {
  const { projects, currentProject, loading, error, fetchProjects, setCurrentProject, createProject, clearError } = useProjectStore()
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [projectName, setProjectName] = useState('')
  const [productSurface, setProductSurface] = useState('')

  useEffect(() => {
    fetchProjects()
  }, [fetchProjects])

  const handleCreateProject = async (e: React.FormEvent) => {
    e.preventDefault()
    clearError()
    const newProject = await createProject(projectName, productSurface || undefined)
    if (newProject) {
      setShowCreateForm(false)
      setProjectName('')
      setProductSurface('')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Projects</h1>
            <p className="text-sm text-gray-500 mt-1">
              Product initiatives, experiment scope, and surface-specific analysis
            </p>
          </div>
          <button
            onClick={() => setShowCreateForm(!showCreateForm)}
            className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
          >
            {showCreateForm ? 'Cancel' : 'Create Project'}
          </button>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-red-800">{error}</p>
            <button onClick={clearError} className="mt-2 text-red-600 hover:text-red-800">
              Dismiss
            </button>
          </div>
        )}

        {showCreateForm && (
          <div className="mb-6 p-6 bg-white rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Create New Project</h2>
            <p className="text-sm text-gray-600 mb-4">
              Projects represent product initiatives, experiment scope, or surface-specific analysis (e.g., "Home Feed Ranking Refresh", "Search Relevance Update").
            </p>
            <form onSubmit={handleCreateProject}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Project Name <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  required
                  value={projectName}
                  onChange={(e) => setProjectName(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  placeholder="e.g., Home Feed Ranking Refresh, Search Relevance Update"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Name your product initiative, experiment, or surface-specific analysis
                </p>
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Product Surface / Environment (optional)
                </label>
                <input
                  type="text"
                  value={productSurface}
                  onChange={(e) => setProductSurface(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  placeholder="e.g., Home Feed, Search, Boards, Ads Manager"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Identifies the product surface or environment generating events (e.g., Home Feed, Search, Boards, Ads Manager)
                </p>
              </div>
              <div className="flex gap-2">
                <button
                  type="submit"
                  disabled={loading}
                  className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
                >
                  {loading ? 'Creating...' : 'Create Project'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowCreateForm(false)
                    setProjectName('')
                    setProductSurface('')
                  }}
                  className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {loading && !projects.length ? (
          <div className="text-center py-12">
            <p className="text-gray-500">Loading projects...</p>
          </div>
        ) : projects.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <p className="text-gray-500 mb-4">No projects yet. Create your first project!</p>
          </div>
        ) : (
          <div className="grid gap-4">
            {projects.map((project) => (
              <div
                key={project.id}
                className={`p-6 bg-white rounded-lg shadow cursor-pointer transition ${
                  currentProject?.id === project.id ? 'ring-2 ring-indigo-500' : ''
                }`}
                onClick={() => setCurrentProject(project)}
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="text-xl font-semibold text-gray-900">{project.name}</h3>
                    {project.domain && (
                      <p className="text-sm text-gray-500 mt-1">
                        <span className="font-medium">Product Surface:</span> {project.domain}
                      </p>
                    )}
                    <p className="text-xs text-gray-400 mt-2">
                      Created: {new Date(project.created_at).toLocaleDateString()}
                    </p>
                  </div>
                  {currentProject?.id === project.id && (
                    <span className="px-3 py-1 bg-indigo-100 text-indigo-800 text-sm rounded-full">
                      Active
                    </span>
                  )}
                </div>
                {currentProject?.id === project.id && (
                  <div className="mt-4 pt-4 border-t border-gray-200 space-y-4">
                    <div>
                      <p className="text-sm text-gray-600 mb-2">
                        <strong>API Key:</strong> {project.api_key}
                      </p>
                      <p className="text-xs text-gray-500">
                        Use this API key to track events. See Journeys page to create inspiration-to-action journeys.
                      </p>
                    </div>
                    <TrackingCode projectId={project.id} />
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
