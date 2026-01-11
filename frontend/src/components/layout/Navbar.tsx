import { Link, useLocation } from 'react-router-dom'

export default function Navbar() {
  const location = useLocation()

  const isActive = (path: string) => location.pathname === path

  return (
    <nav className="border-b" style={{ backgroundColor: '#FFFFFF', borderColor: '#E5E7EB' }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <h1 className="text-xl font-bold" style={{ color: '#E60023' }}>
                IAFA
              </h1>
              <span className="hidden md:inline ml-3 text-xs font-normal" style={{ color: '#6B7280' }}>Inspiration-to-Action Funnel Analyzer</span>
            </div>
            <div className="hidden sm:ml-12 sm:flex sm:space-x-8 sm:items-center">
              <Link
                to="/dashboard"
                className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-semibold transition-colors duration-150 ${
                  isActive('/dashboard')
                    ? 'text-black border-black'
                    : 'text-gray-600 hover:text-black border-transparent'
                }`}
              >
                Journey Overview
              </Link>
              <Link
                to="/funnels"
                className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-semibold transition-colors duration-150 ${
                  isActive('/funnels')
                    ? 'text-black border-black'
                    : 'text-gray-600 hover:text-black border-transparent'
                }`}
              >
                Journeys
              </Link>
            </div>
          </div>
        </div>
      </div>
    </nav>
  )
}
