/**
 * Report Generator Utilities
 * Generates formatted reports for leadership export
 */

export interface ReportData {
  funnel_name: string
  date_range: { start: string; end: string }
  total_users?: number
  completed_users?: number
  overall_conversion_rate?: number
  stages?: Array<{
    stage_name: string
    users: number
    conversion_rate: number
    drop_off_rate: number
  }>
  segments?: Record<string, {
    total_users: number
    completed_users: number
    overall_conversion_rate: number
    stages?: Array<{
      stage_name: string
      users: number
      conversion_rate: number
    }>
  }>
  segment_by?: string
}

/**
 * Generate a formatted text report for leadership
 */
export function generateTextReport(data: ReportData): string {
  const lines: string[] = []
  
  // Header
  lines.push('='.repeat(80))
  lines.push('INSPIRATION-TO-ACTION FUNNEL ANALYZER (IAFA) - EXECUTIVE REPORT')
  lines.push('='.repeat(80))
  lines.push('')
  
  // Journey Information
  lines.push(`Journey: ${data.funnel_name}`)
  lines.push(`Date Range: ${formatDate(data.date_range.start)} to ${formatDate(data.date_range.end)}`)
  lines.push('')
  lines.push('-'.repeat(80))
  lines.push('')
  
  // Executive Summary
  if (data.total_users !== undefined) {
    lines.push('EXECUTIVE SUMMARY')
    lines.push('')
    lines.push(`Total Users Exposed: ${data.total_users.toLocaleString()}`)
    lines.push(`Users Advanced to Action: ${data.completed_users?.toLocaleString() || 0}`)
    lines.push(`Overall Progression Rate: ${(data.overall_conversion_rate || 0).toFixed(2)}%`)
    lines.push('')
  }
  
  // Journey Stages
  if (data.stages && data.stages.length > 0) {
    lines.push('JOURNEY STAGE PERFORMANCE')
    lines.push('')
    lines.push(`${'Stage'.padEnd(30)} ${'Users'.padStart(15)} ${'Progression Rate'.padStart(20)} ${'Drop-off Rate'.padStart(20)}`)
    lines.push('-'.repeat(80))
    
    data.stages.forEach((stage, index) => {
      const nextStage = data.stages![index + 1]
      const dropOff = nextStage ? nextStage.drop_off_rate : 0
      lines.push(
        `${stage.stage_name.padEnd(30)} ${stage.users.toLocaleString().padStart(15)} ${stage.conversion_rate.toFixed(2).padStart(19)}% ${dropOff.toFixed(2).padStart(19)}%`
      )
    })
    lines.push('')
  }
  
  // Segment Breakdown
  if (data.segments && Object.keys(data.segments).length > 0) {
    lines.push('SEGMENT ANALYSIS')
    lines.push(`Breakdown by: ${formatSegmentBy(data.segment_by || '')}`)
    lines.push('')
    
    Object.entries(data.segments).forEach(([segmentValue, segmentData]) => {
      lines.push(`${segmentValue}:`)
      lines.push(`  Total Users: ${segmentData.total_users.toLocaleString()}`)
      lines.push(`  Completed Users: ${segmentData.completed_users.toLocaleString()}`)
      lines.push(`  Progression Rate: ${segmentData.overall_conversion_rate.toFixed(2)}%`)
      lines.push('')
    })
    
    // Key Insights
    lines.push('KEY INSIGHTS')
    lines.push('')
    const insights = generateInsights(data)
    insights.forEach(insight => {
      lines.push(`• ${insight}`)
    })
    lines.push('')
  }
  
  // Footer
  lines.push('-'.repeat(80))
  lines.push(`Report Generated: ${new Date().toLocaleString()}`)
  lines.push('='.repeat(80))
  
  return lines.join('\n')
}

/**
 * Generate CSV report
 */
export function generateCSVReport(data: ReportData): string {
  const lines: string[] = []
  
  // Header
  lines.push('IAFA Executive Report')
  lines.push(`Journey: ${data.funnel_name}`)
  lines.push(`Date Range: ${data.date_range.start} to ${data.date_range.end}`)
  lines.push('')
  
  // Summary
  if (data.total_users !== undefined) {
    lines.push('Executive Summary')
    lines.push('Metric,Value')
    lines.push(`Total Users,${data.total_users}`)
    lines.push(`Completed Users,${data.completed_users || 0}`)
    lines.push(`Overall Progression Rate,${(data.overall_conversion_rate || 0).toFixed(2)}%`)
    lines.push('')
  }
  
  // Stages
  if (data.stages && data.stages.length > 0) {
    lines.push('Journey Stages')
    lines.push('Stage Name,Users,Progression Rate (%),Drop-off Rate (%)')
    data.stages.forEach((stage, index) => {
      const nextStage = data.stages![index + 1]
      const dropOff = nextStage ? nextStage.drop_off_rate : 0
      lines.push(`${stage.stage_name},${stage.users},${stage.conversion_rate.toFixed(2)},${dropOff.toFixed(2)}`)
    })
    lines.push('')
  }
  
  // Segments
  if (data.segments && Object.keys(data.segments).length > 0) {
    lines.push('Segment Analysis')
    lines.push(`Breakdown by: ${data.segment_by || ''}`)
    lines.push('Segment,Total Users,Completed Users,Progression Rate (%)')
    Object.entries(data.segments).forEach(([segmentValue, segmentData]) => {
      lines.push(`${segmentValue},${segmentData.total_users},${segmentData.completed_users},${segmentData.overall_conversion_rate.toFixed(2)}`)
    })
  }
  
  return lines.join('\n')
}

/**
 * Generate HTML report
 */
export function generateHTMLReport(data: ReportData): string {
  const insights = generateInsights(data)
  
  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>IAFA Executive Report - ${data.funnel_name}</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      max-width: 1200px;
      margin: 0 auto;
      padding: 40px 20px;
      background-color: #f5f5f5;
    }
    .container {
      background: white;
      padding: 40px;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 {
      color: #E60023;
      border-bottom: 3px solid #E60023;
      padding-bottom: 10px;
      margin-bottom: 30px;
    }
    h2 {
      color: #111827;
      margin-top: 30px;
      margin-bottom: 15px;
      font-size: 1.5em;
    }
    .summary {
      background: #f9fafb;
      padding: 20px;
      border-radius: 8px;
      margin: 20px 0;
      border-left: 4px solid #E60023;
    }
    .summary-item {
      display: flex;
      justify-content: space-between;
      padding: 10px 0;
      border-bottom: 1px solid #e5e7eb;
    }
    .summary-item:last-child {
      border-bottom: none;
    }
    .summary-label {
      font-weight: 600;
      color: #6b7280;
    }
    .summary-value {
      font-weight: 700;
      color: #111827;
      font-size: 1.1em;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
    }
    th {
      background: #f9fafb;
      padding: 12px;
      text-align: left;
      font-weight: 600;
      color: #374151;
      border-bottom: 2px solid #e5e7eb;
    }
    td {
      padding: 12px;
      border-bottom: 1px solid #e5e7eb;
    }
    tr:hover {
      background: #f9fafb;
    }
    .insights {
      background: #eff6ff;
      padding: 20px;
      border-radius: 8px;
      margin: 20px 0;
      border-left: 4px solid #3b82f6;
    }
    .insights ul {
      margin: 0;
      padding-left: 20px;
    }
    .insights li {
      margin: 8px 0;
    }
    .footer {
      margin-top: 40px;
      padding-top: 20px;
      border-top: 1px solid #e5e7eb;
      color: #6b7280;
      font-size: 0.9em;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Inspiration-to-Action Funnel Analyzer (IAFA)</h1>
    <h2>Executive Report</h2>
    
    <div style="margin-bottom: 30px;">
      <p><strong>Journey:</strong> ${data.funnel_name}</p>
      <p><strong>Date Range:</strong> ${formatDate(data.date_range.start)} to ${formatDate(data.date_range.end)}</p>
    </div>
    
    ${data.total_users !== undefined ? `
    <div class="summary">
      <h2>Executive Summary</h2>
      <div class="summary-item">
        <span class="summary-label">Total Users Exposed</span>
        <span class="summary-value">${data.total_users.toLocaleString()}</span>
      </div>
      <div class="summary-item">
        <span class="summary-label">Users Advanced to Action</span>
        <span class="summary-value">${data.completed_users?.toLocaleString() || 0}</span>
      </div>
      <div class="summary-item">
        <span class="summary-label">Overall Progression Rate</span>
        <span class="summary-value">${(data.overall_conversion_rate || 0).toFixed(2)}%</span>
      </div>
    </div>
    ` : ''}
    
    ${data.stages && data.stages.length > 0 ? `
    <h2>Journey Stage Performance</h2>
    <table>
      <thead>
        <tr>
          <th>Stage</th>
          <th>Users</th>
          <th>Progression Rate</th>
          <th>Drop-off Rate</th>
        </tr>
      </thead>
      <tbody>
        ${data.stages.map((stage, index) => {
          const nextStage = data.stages![index + 1]
          const dropOff = nextStage ? nextStage.drop_off_rate : 0
          return `
          <tr>
            <td>${stage.stage_name}</td>
            <td>${stage.users.toLocaleString()}</td>
            <td>${stage.conversion_rate.toFixed(2)}%</td>
            <td>${dropOff.toFixed(2)}%</td>
          </tr>
          `
        }).join('')}
      </tbody>
    </table>
    ` : ''}
    
    ${data.segments && Object.keys(data.segments).length > 0 ? `
    <h2>Segment Analysis</h2>
    <p><strong>Breakdown by:</strong> ${formatSegmentBy(data.segment_by || '')}</p>
    <table>
      <thead>
        <tr>
          <th>Segment</th>
          <th>Total Users</th>
          <th>Completed Users</th>
          <th>Progression Rate</th>
        </tr>
      </thead>
      <tbody>
        ${Object.entries(data.segments).map(([segmentValue, segmentData]) => `
        <tr>
          <td>${segmentValue}</td>
          <td>${segmentData.total_users.toLocaleString()}</td>
          <td>${segmentData.completed_users.toLocaleString()}</td>
          <td>${segmentData.overall_conversion_rate.toFixed(2)}%</td>
        </tr>
        `).join('')}
      </tbody>
    </table>
    ` : ''}
    
    ${insights.length > 0 ? `
    <div class="insights">
      <h2>Key Insights</h2>
      <ul>
        ${insights.map(insight => `<li>${insight}</li>`).join('')}
      </ul>
    </div>
    ` : ''}
    
    <div class="footer">
      <p>Report Generated: ${new Date().toLocaleString()}</p>
      <p>Inspiration-to-Action Funnel Analyzer (IAFA)</p>
    </div>
  </div>
</body>
</html>
  `.trim()
}

/**
 * Generate key insights from data
 */
function generateInsights(data: ReportData): string[] {
  const insights: string[] = []
  
  if (data.stages && data.stages.length > 0) {
    // Find stage with highest drop-off
    let maxDropOff = 0
    let maxDropOffStage = ''
    data.stages.forEach((stage, index) => {
      const nextStage = data.stages![index + 1]
      if (nextStage && nextStage.drop_off_rate > maxDropOff) {
        maxDropOff = nextStage.drop_off_rate
        maxDropOffStage = stage.stage_name
      }
    })
    
    if (maxDropOffStage) {
      insights.push(`Highest drop-off occurs after "${maxDropOffStage}" stage (${maxDropOff.toFixed(1)}% natural attrition)`)
    }
  }
  
  if (data.segments && Object.keys(data.segments).length > 0) {
    const segmentEntries = Object.entries(data.segments)
    if (segmentEntries.length > 1) {
      // Find best and worst performing segments
      segmentEntries.sort((a, b) => b[1].overall_conversion_rate - a[1].overall_conversion_rate)
      const best = segmentEntries[0]
      const worst = segmentEntries[segmentEntries.length - 1]
      
      if (best[1].overall_conversion_rate > worst[1].overall_conversion_rate) {
        const difference = ((best[1].overall_conversion_rate / worst[1].overall_conversion_rate - 1) * 100).toFixed(0)
        insights.push(`${best[0]} segment shows ${difference}% higher progression rate than ${worst[0]} segment`)
      }
    }
  }
  
  if (data.overall_conversion_rate !== undefined) {
    if (data.overall_conversion_rate < 10) {
      insights.push('Overall progression rate is below 10%, indicating significant opportunity for improvement')
    } else if (data.overall_conversion_rate > 50) {
      insights.push('Strong overall progression rate indicates effective journey design')
    }
  }
  
  return insights
}

/**
 * Format date string
 */
function formatDate(dateStr: string): string {
  try {
    const date = new Date(dateStr)
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
  } catch {
    return dateStr
  }
}

/**
 * Format segment_by string for display
 */
function formatSegmentBy(segmentBy: string): string {
  return segmentBy
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}
