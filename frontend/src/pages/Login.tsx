import { Navigate } from 'react-router-dom'

export default function Login() {
  // POC: No authentication required - redirect to dashboard
  return <Navigate to="/dashboard" replace />
}
