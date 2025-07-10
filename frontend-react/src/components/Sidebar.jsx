import React, { useEffect, useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function Sidebar({ token, schoolId, onSchoolChange }) {
  const [schools, setSchools] = useState([])

  useEffect(() => {
    async function fetchSchools() {
      const res = await fetch(`${API_URL}/schools`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      if (res.ok) {
        const data = await res.json()
        setSchools(data)
        if (!schoolId && data.length) {
          onSchoolChange(String(data[0].id))
        }
      }
    }
    if (token) fetchSchools()
  }, [token])

  return (
    <aside className="sidebar text-bg-dark flex-shrink-0 p-3">
        <div className="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-white">
          <i className="bi bi-speedometer2 me-2 fs-4"></i>
          <select className="form-select form-select-sm bg-dark text-white border-0" value={schoolId || ''} onChange={e => onSchoolChange(e.target.value)}>
            {schools.map(s => (
              <option key={s.id} value={s.id}>{s.name}</option>
            ))}
          </select>
        </div>
        <hr />
        <ul className="nav nav-pills flex-column mb-auto">
          <li className="nav-item"><a href="#" className="nav-link text-white active"><i className="bi bi-bar-chart me-2"></i>Отчёты</a></li>
          <li><a href="#" className="nav-link text-white"><i className="bi bi-people me-2"></i>Ученики</a></li>
          <li><a href="#" className="nav-link text-white"><i className="bi bi-book me-2"></i>Предметы</a></li>
          <li><a href="#" className="nav-link text-white"><i className="bi bi-card-checklist me-2"></i>Оценки</a></li>
          <li><a href="#" className="nav-link text-white"><i className="bi bi-gear me-2"></i>Настройки</a></li>
        </ul>
        <hr />
        <small className="text-white-50">v0.1.0 • 2025</small>
    </aside>
  )
}

export default Sidebar
