import { useState } from 'react'
import FunnelBarChart from './FunnelBarChart'
import SegmentComparisonChart from './SegmentComparisonChart'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface StageData {
  stage_name: string
  users: number
  conversion_rate: number
  drop_off_rate: number
}

interface SegmentData {
  [segmentValue: string]: {
    total_users: number
    completed_users: number
    overall_conversion_rate: number
  }
}

interface ChartSwitcherProps {
  stages?: StageData[]
  segments?: SegmentData
}

type ChartType = 'funnel' | 'segment' | 'trend'

export default function ChartSwitcher({ stages, segments }: ChartSwitcherProps) {
  const [chartType, setChartType] = useState<ChartType>('funnel')

  // Prepare trend data (conversion rate over stages)
  const trendData = stages?.map((stage, index) => ({
    stage: stage.stage_name,
    conversionRate: stage.conversion_rate,
    users: stage.users,
    order: index + 1,
  })) || []

  return (
    <div className="p-6 rounded-xl shadow-sm border border-gray-200" style={{ backgroundColor: '#FAFAFA' }}>
      {/* Chart Type Switcher */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold text-gray-900">Analytics Visualization</h2>
        <div className="flex gap-2 bg-white rounded-lg p-1 border border-gray-200">
          <button
            onClick={() => setChartType('funnel')}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              chartType === 'funnel'
                ? 'bg-[#E60023] text-white'
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
            }`}
          >
            Funnel View
          </button>
          {segments && Object.keys(segments).length > 0 && (
            <button
              onClick={() => setChartType('segment')}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                chartType === 'segment'
                  ? 'bg-[#E60023] text-white'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              Segment Comparison
            </button>
          )}
          {stages && stages.length > 0 && (
            <button
              onClick={() => setChartType('trend')}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                chartType === 'trend'
                  ? 'bg-[#E60023] text-white'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              Trend View
            </button>
          )}
        </div>
      </div>

      {/* Chart Display */}
      <div className="mt-4">
        {chartType === 'funnel' && stages && stages.length > 0 && (
          <FunnelBarChart stages={stages} />
        )}
        
        {chartType === 'segment' && segments && Object.keys(segments).length > 0 && (
          <SegmentComparisonChart segments={segments} />
        )}
        
        {chartType === 'trend' && stages && stages.length > 0 && (
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={trendData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
              <XAxis 
                dataKey="stage" 
                tick={{ fill: '#6B7280', fontSize: 12 }}
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis 
                tick={{ fill: '#6B7280', fontSize: 12 }}
                label={{ value: 'Conversion Rate (%)', angle: -90, position: 'insideLeft', style: { fill: '#6B7280' } }}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#FFFFFF',
                  border: '1px solid #E5E7EB',
                  borderRadius: '8px',
                }}
                formatter={(value: number) => [`${value.toFixed(1)}%`, 'Conversion Rate']}
              />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="conversionRate" 
                stroke="#E60023" 
                strokeWidth={3}
                dot={{ fill: '#E60023', r: 5 }}
                activeDot={{ r: 8 }}
              />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  )
}
