import React, { useEffect, useMemo, useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function calcStats(grades) {
  let sum = 0
  const byStudent = {}
  for (const g of grades) {
    const v = parseFloat(g.value)
    sum += v
    byStudent[g.student_id] = (byStudent[g.student_id] || []).concat(v)
  }
  const avg = grades.length ? (sum / grades.length).toFixed(2) : '–'
  let excellent = 0
  let failing = 0
  Object.values(byStudent).forEach(arr => {
    const avgG = arr.reduce((a,b)=>a+b,0)/arr.length
    if (avgG >= 4.5) excellent++
    if (avgG < 3) failing++
  })
  return { avg, excellent, failing }
}

function Dashboard({ token }) {
  const [stats, setStats] = useState({ avg: '–', excellent: '–', failing: '–' })
  const [grades, setGrades] = useState([])
  const [students, setStudents] = useState([])
  const [selectedClass, setSelectedClass] = useState('all')
  const [selectedQuarter, setSelectedQuarter] = useState('all')

  const classOptions = useMemo(() => {
    const uniq = {}
    students.forEach(s => {
      uniq[s.class_id] = s.class_name
    })
    return Object.entries(uniq).map(([id, name]) => ({ id, name }))
  }, [students])

  useEffect(() => {
    async function fetchGrades() {
      const res = await fetch(`${API_URL}/grades`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      if (!res.ok) throw new Error('Failed to fetch grades')
      return await res.json()
    }

    async function fetchStudents() {
      const res = await fetch(`${API_URL}/students`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      if (!res.ok) throw new Error('Failed to fetch students')
      return await res.json()
    }

    async function update() {
      try {
        const [g, s] = await Promise.all([fetchGrades(), fetchStudents()])
        setGrades(g)
        setStudents(s)
      } catch (e) {
        console.error(e)
      }
    }

    update()
  }, [token])

  useEffect(() => {
    if (!grades.length) return
    const studentMap = {}
    students.forEach(s => {
      studentMap[s.id] = s
    })
    const filtered = grades.filter(g => {
      if (selectedQuarter !== 'all') {
        if (g.term_type !== 'quarter' || String(g.term_index) !== selectedQuarter) return false
      }
      if (selectedClass !== 'all') {
        const st = studentMap[g.student_id]
        if (!st || String(st.class_id) !== selectedClass) return false
      }
      return true
    })
    setStats(calcStats(filtered))
  }, [grades, students, selectedClass, selectedQuarter])

  return (
    <div id="contentPane">
      <ul className="nav nav-tabs mb-4" id="roleTabs" role="tablist">
        <li className="nav-item" role="presentation">
          <button className="nav-link active" id="cr-tab" data-bs-toggle="tab" data-bs-target="#crPane" role="tab">Классные руководители</button>
        </li>
        <li className="nav-item" role="presentation">
          <button className="nav-link" id="teachers-tab" data-bs-toggle="tab" data-bs-target="#teachersPane" role="tab">Педагоги</button>
        </li>
        <li className="nav-item" role="presentation">
          <button className="nav-link" id="admin-tab" data-bs-toggle="tab" data-bs-target="#adminPane" role="tab">Администрация</button>
        </li>
        <li className="nav-item" role="presentation">
          <button className="nav-link" id="ahc-tab" data-bs-toggle="tab" data-bs-target="#ahcPane" role="tab">АХЧ</button>
        </li>
      </ul>
      <div className="tab-content">
        <div className="tab-pane fade show active" id="crPane" role="tabpanel">
          <div className="row g-3 mb-3">
            <div className="col-auto">
              <select className="form-select" value={selectedClass} onChange={e => setSelectedClass(e.target.value)}>
                <option value="all">Все классы</option>
                {classOptions.map(o => (
                  <option key={o.id} value={o.id}>{o.name}</option>
                ))}
              </select>
            </div>
            <div className="col-auto">
              <select className="form-select" value={selectedQuarter} onChange={e => setSelectedQuarter(e.target.value)}>
                <option value="all">Весь год</option>
                <option value="1">1 четверть</option>
                <option value="2">2 четверть</option>
                <option value="3">3 четверть</option>
                <option value="4">4 четверть</option>
              </select>
            </div>
          </div>
          <div className="row row-cols-2 row-cols-lg-4 g-4 mb-4" id="kpiCards">
            <div className="col">
              <div className="card h-100 shadow-sm border-0">
                <div className="card-body">
                  <h6 className="card-title text-muted">Средний балл</h6>
                  <h3 className="fw-bold mb-0" id="avgGrade">{stats.avg}</h3>
                </div>
              </div>
            </div>
            <div className="col">
              <div className="card h-100 shadow-sm border-0">
                <div className="card-body">
                  <h6 className="card-title text-muted">Отличники</h6>
                  <h3 className="fw-bold mb-0" id="excellentCount">{stats.excellent}</h3>
                </div>
              </div>
            </div>
            <div className="col">
              <div className="card h-100 shadow-sm border-0">
                <div className="card-body">
                  <h6 className="card-title text-muted">Неуспевающие</h6>
                  <h3 className="fw-bold mb-0 text-danger" id="failingCount">{stats.failing}</h3>
                </div>
              </div>
            </div>
            <div className="col">
              <div className="card h-100 shadow-sm border-0">
                <div className="card-body">
                  <h6 className="card-title text-muted">Пропуски (%)</h6>
                  <h3 className="fw-bold mb-0" id="absencePercent">–</h3>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
