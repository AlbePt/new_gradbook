import { useState } from 'react'
import Navbar from './components/Navbar'
import Sidebar from './components/Sidebar'
import LoginPane from './components/LoginPane'
import Dashboard from './components/Dashboard'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [token, setToken] = useState(() => localStorage.getItem('token'))
  const [schoolId, setSchoolId] = useState('')

  const login = async (username, password) => {
    const form = new URLSearchParams()
    form.append('username', username)
    form.append('password', password)
    const res = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: form.toString()
    })
    if (!res.ok) {
      alert('Ошибка входа')
      return
    }
    const data = await res.json()
    localStorage.setItem('token', data.access_token)
    setToken(data.access_token)
  }

  const logout = () => {
    localStorage.removeItem('token')
    setToken(null)
    setSchoolId('')
  }

  return (
    <>
      <Navbar onLogout={logout} />
      <div className="d-flex">
        <Sidebar token={token} schoolId={schoolId} onSchoolChange={setSchoolId} />
        <main className="flex-grow-1">
          <div className="container-fluid py-4">
            {!token ? <LoginPane onLogin={login} /> : <Dashboard token={token} schoolId={schoolId} />}
          </div>
        </main>
      </div>
    </>
  )
}

export default App
