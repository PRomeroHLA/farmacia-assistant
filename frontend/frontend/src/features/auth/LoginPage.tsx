import { useState, type FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/useAuth'

export function LoginPage() {
  const { login, error } = useAuth()
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    await login(username, password)
    if (!error) {
      navigate('/dashboard')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-50 flex items-center justify-center p-4">
      <main className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-xl p-8 border border-emerald-100">
          <div className="flex justify-center mb-6">
            <div className="bg-emerald-500 p-4 rounded-xl shadow-md">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-50">
                <span className="relative block h-5 w-3 rounded-full bg-emerald-500">
                  <span className="absolute inset-x-[-2px] top-1/2 h-1 -translate-y-1/2 rounded-full bg-emerald-50" />
                </span>
              </div>
            </div>
          </div>

          <h1 className="text-center text-lg font-semibold tracking-tight text-emerald-700 mb-4">
            Asistente de Recomendación Farmacéutica
          </h1>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="space-y-1">
              <label
                htmlFor="username"
                className="block text-gray-700 mb-2"
              >
                Usuario
              </label>
              <input
                id="username"
                name="username"
                type="text"
                value={username}
                onChange={(event) => setUsername(event.target.value)}
                className="w-full px-4 py-3 bg-white border border-emerald-300 rounded-lg shadow-[0_0_0_1px_rgba(16,185,129,0.25)] focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
              />
            </div>

            <div className="space-y-1">
              <label
                htmlFor="password"
                className="block text-gray-700 mb-2"
              >
                Contraseña
              </label>
              <input
                id="password"
                name="password"
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                className="w-full px-4 py-3 bg-white border border-emerald-300 rounded-lg shadow-[0_0_0_1px_rgba(16,185,129,0.25)] focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-emerald-500 hover:bg-emerald-600 text-white py-3 rounded-lg transition-colors duration-200 mt-6"
            >
              Iniciar sesión
            </button>

            {error ? (
              <p className="mt-2 text-sm text-red-600">{error}</p>
            ) : null}
          </form>
        </div>
      </main>
    </div>
  )
}
