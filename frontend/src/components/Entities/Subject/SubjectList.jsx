import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import adminClient from '../../../api/adminClient.js';
import { setSubjects } from './subjectSlice.js';
import '../../../styles/subjects.css';

export default function SubjectList() {
  const dispatch = useDispatch();
  const list = useSelector(state => state.subjects.items) || [];

  useEffect(() => {
    adminClient
      .get('/subjects')
      .then(res => dispatch(setSubjects(res.data)))
      .catch(() => {});
  }, [dispatch]);

  return (
    <section className="subjects-page">
      <h1 className="subjects-title">П Р Е Д М Е Т Ы</h1>
      <div className="year-switch">
        <span>&larr;</span>
        <span>2024-2025</span>
        <span>&rarr;</span>
      </div>
      <div className="subject-tabs">
        <button className="active">■ Предметы для уроков</button>
        <button>Предметы для внеурочной деятельности</button>
      </div>
      <button className="add-btn">+ Добавить предметы</button>
      <p className="count">Всего предметов: {list.length}</p>
      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              <th>№</th>
              <th>Название</th>
              <th>Ступени</th>
              <th>Область</th>
            </tr>
          </thead>
          <tbody>
            {list.map((s, idx) => (
              <tr key={s.id || idx}>
                <td>{idx + 1}</td>
                <td>{s.name}</td>
                <td>-</td>
                <td>-</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
