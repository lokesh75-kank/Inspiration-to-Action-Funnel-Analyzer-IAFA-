import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts'

interface StageData {
  stage_name: string
  users: number
  conversion_rate: number
  drop_off_rate: number
}

interface FunnelBarChartProps {
  stages: StageData[]
}

export default function FunnelBarChart({ stages }: FunnelBarChartProps) {
  const chartData = stages.map((stage) => ({
    name: stage.stage_name,
    users: stage.users,
    conversionRate: stage.conversion_rate,
    dropOffRate: stage.drop_off_rate,
  }))

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart
        data={chartData}
        margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
        <XAxis 
          dataKey="name" 
          tick={{ fill: '#6B7280', fontSize: 12 }}
          angle={-45}
          textAnchor="end"
          height={80}
        />
        <YAxis 
          tick={{ fill: '#6B7280', fontSize: 12 }}
          label={{ value: 'Users', angle: -90, position: 'insideLeft', style: { fill: '#6B7280' } }}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: '#FFFFFF',
            border: '1px solid #E5E7EB',
            borderRadius: '8px',
          }}
          formatter={(value: number, name: string) => {
            if (name === 'users') return [value.toLocaleString(), 'Users']
            if (name === 'conversionRate') return [`${value.toFixed(1)}%`, 'Progression Rate']
            return [value, name]
          }}
        />
        <Legend 
          wrapperStyle={{ paddingTop: '20px' }}
          formatter={(value) => {
            if (value === 'users') return 'Users'
            if (value === 'conversionRate') return 'Progression Rate'
            return value
          }}
        />
        <Bar dataKey="users" fill="#E60023" radius={[4, 4, 0, 0]}>
          {chartData.map((_, index) => (
            <Cell key={`cell-${index}`} fill="#E60023" />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
