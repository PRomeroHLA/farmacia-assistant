import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/useAuth'

export function DashboardPage() {
  const { user } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    if (!user) {
      navigate('/login')
    }
  }, [user, navigate])

  return (
    <main>
      <h1>Dashboard</h1>
      <p>Área principal (placeholder).</p>
    </main>
  )
}

