/**
 * Sidebar – navigation with school selector.
 */
import React, { useEffect, useState } from 'react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function Sidebar({ token, schoolId, onSchoolChange, onSelect, current }) {
  const [schools, setSchools] = useState([]);

  useEffect(() => {
    async function fetchSchools() {
      const res = await fetch(`${API_URL}/schools`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        const data = await res.json();
        setSchools(data);
        if (!schoolId && data.length) {
          onSchoolChange(String(data[0].id));
        }
      }
    }
    if (token) fetchSchools();
  }, [token]);

  return (
    <aside className="sidebar">
      <div className="school-select">
        <select value={schoolId || ''} onChange={(e) => onSchoolChange(e.target.value)}>
          {schools.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name}
            </option>
          ))}
        </select>
      </div>
      <ul className="menu">
        <li className={current === 'dashboard' ? 'active' : ''} onClick={() => onSelect('dashboard')}>
          <i className="bi bi-bar-chart"></i>
          <span>Отчёты</span>
        </li>
        <li className={current === 'students' ? 'active' : ''} onClick={() => onSelect('students')}>
          <i className="bi bi-people"></i>
          <span>Ученики</span>
        </li>
        <li className={current === 'subjects' ? 'active' : ''} onClick={() => onSelect('subjects')}>
          <i className="bi bi-book"></i>
          <span>Предметы</span>
        </li>
        <li className={current === 'grades' ? 'active' : ''} onClick={() => onSelect('grades')}>
          <i className="bi bi-card-checklist"></i>
          <span>Оценки</span>
        </li>
        <li className={current === 'settings' ? 'active' : ''} onClick={() => onSelect('settings')}>
          <i className="bi bi-gear"></i>
          <span>Настройки</span>
        </li>
      </ul>
      <footer className="version">v0.1.0 • 2025</footer>
    </aside>
  );
}

export default Sidebar;
