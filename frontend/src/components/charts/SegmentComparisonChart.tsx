import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts'

interface SegmentData {
  [segmentValue: string]: {
    total_users: number
    completed_users: number
    overall_conversion_rate: number
  }
}

interface SegmentComparisonChartProps {
  segments: SegmentData
  segmentBy?: string
}

export default function SegmentComparisonChart({ segments }: SegmentComparisonChartProps) {
  const chartData = Object.entries(segments).map(([segmentValue, data]) => ({
    segment: segmentValue,
    conversionRate: data.overall_conversion_rate,
    totalUsers: data.total_users,
  }))

  const colors = ['#E60023', '#1E40AF', '#059669', '#DC2626', '#7C3AED']

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart
        data={chartData}
        margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
        <XAxis 
          dataKey="segment" 
          tick={{ fill: '#6B7280', fontSize: 12 }}
          angle={-45}
          textAnchor="end"
          height={80}
        />
        <YAxis 
          tick={{ fill: '#6B7280', fontSize: 12 }}
          label={{ value: 'Progression Rate (%)', angle: -90, position: 'insideLeft', style: { fill: '#6B7280' } }}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: '#FFFFFF',
            border: '1px solid #E5E7EB',
            borderRadius: '8px',
          }}
          formatter={(value: number) => [`${value.toFixed(1)}%`, 'Progression Rate']}
        />
        <Legend />
        <Bar dataKey="conversionRate" radius={[4, 4, 0, 0]}>
          {chartData.map((_, index) => (
            <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
