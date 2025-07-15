/**
 * Dashboard – statistics view with filters and KPI cards.
 */
import React, { useEffect, useMemo, useState } from 'react';
import PagePlaceholder from './PagePlaceholder';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function Dashboard({ token, schoolId, role }) {
  const [stats, setStats] = useState({ avg: '–', excellent: '–', failing: '–' });
  const [academicYears, setAcademicYears] = useState([]);
  const [classes, setClasses] = useState([]);
  const [selectedYear, setSelectedYear] = useState('');
  const [selectedClass, setSelectedClass] = useState('all');
  const [selectedQuarter, setSelectedQuarter] = useState('all');

  const classOptions = useMemo(() => {
    return classes.map((c) => ({ id: c.id, name: c.name }));
  }, [classes]);

  useEffect(() => {
    async function fetchYears() {
      const res = await fetch(`${API_URL}/academic-years`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        const data = await res.json();
        setAcademicYears(data);
        if (data.length && !selectedYear) {
          setSelectedYear(String(data[0].id));
        }
      }
    }
    if (token) fetchYears();
  }, [token]);

  useEffect(() => {
    if (!schoolId || !selectedYear) {
      setClasses([]);
      return;
    }
    async function fetchClasses() {
      const res = await fetch(
        `${API_URL}/classes?school_id=${schoolId}&academic_year_id=${selectedYear}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        },
      );
      if (res.ok) {
        setClasses(await res.json());
      }
    }
    fetchClasses();
  }, [schoolId, selectedYear, token]);

  useEffect(() => {
    if (!schoolId || !selectedYear) return;
    async function fetchStats() {
      let url = `${API_URL}/stats/average-grade?school_id=${schoolId}&academic_year_id=${selectedYear}`;
      if (selectedClass !== 'all') url += `&class_id=${selectedClass}`;
      if (selectedQuarter !== 'all') url += `&quarter=${selectedQuarter}`;
      const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
      if (res.ok) {
        const data = await res.json();
        setStats({
          avg: data.average ? Number(data.average).toFixed(2) : '–',
          excellent: '–',
          failing: '–',
        });
      }
    }
    fetchStats();
  }, [schoolId, selectedYear, selectedClass, selectedQuarter, token]);

  return (
    <div id="contentPane">
      {role !== 'cr' ? (
        <PagePlaceholder page={role} />
      ) : (
        <>
          <div className="row g-3 mb-3">
            <div className="col-auto">
              <select
                className="form-select"
                value={selectedYear}
                onChange={(e) => setSelectedYear(e.target.value)}
              >
                {academicYears.map((y) => (
                  <option key={y.id} value={y.id}>
                    {y.name}
                  </option>
                ))}
              </select>
            </div>
            <div className="col-auto">
              <select
                className="form-select"
                value={selectedClass}
                onChange={(e) => setSelectedClass(e.target.value)}
              >
                <option value="all">Все классы</option>
                {classOptions.map((o) => (
                  <option key={o.id} value={o.id}>
                    {o.name}
                  </option>
                ))}
              </select>
            </div>
            <div className="col-auto">
              <select
                className="form-select"
                value={selectedQuarter}
                onChange={(e) => setSelectedQuarter(e.target.value)}
              >
                <option value="all">Весь год</option>
                <option value="1">1 четверть</option>
                <option value="2">2 четверть</option>
                <option value="3">3 четверть</option>
                <option value="4">4 четверть</option>
              </select>
            </div>
          </div>
          <div className="cards">
            <div className="card">
              <h3>Средний балл</h3>
              <p className="value" id="avgGrade">{stats.avg}</p>
            </div>
            <div className="card">
              <h3>Отличники</h3>
              <p className="value" id="excellentCount">{stats.excellent}</p>
            </div>
            <div className="card">
              <h3>Неуспевающие</h3>
              <p className="value text-danger" id="failingCount">{stats.failing}</p>
            </div>
            <div className="card">
              <h3>Пропуски (%)</h3>
              <p className="value" id="absencePercent">–</p>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default Dashboard;
