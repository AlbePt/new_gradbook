import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import adminClient from '../../../api/adminClient.js';
import { setSubjects } from './subjectSlice.js';

export default function SubjectList() {
  const dispatch = useDispatch();
  const subjects = useSelector(state => state.subjects.items);
  const [name, setName] = useState('');
  const [schoolId, setSchoolId] = useState('');
  const [editId, setEditId] = useState(null);
  const [editName, setEditName] = useState('');
  const [editSchoolId, setEditSchoolId] = useState('');

  useEffect(() => {
    adminClient
      .get('/subjects')
      .then(res => dispatch(setSubjects(res.data)))
      .catch(() => {});
  }, [dispatch]);

  const addSubject = () => {
    adminClient
      .post('/subjects', { name, school_id: Number(schoolId) })
      .then(res => {
        dispatch(setSubjects([...subjects, res.data]));
        setName('');
        setSchoolId('');
      })
      .catch(() => {});
  };

  const startEdit = subj => {
    setEditId(subj.id);
    setEditName(subj.name);
    setEditSchoolId(subj.school_id);
  };

  const saveEdit = () => {
    adminClient
      .put(`/subjects/${editId}`, {
        name: editName,
        school_id: Number(editSchoolId),
      })
      .then(res => {
        dispatch(
          setSubjects(subjects.map(s => (s.id === editId ? res.data : s)))
        );
        setEditId(null);
      })
      .catch(() => {});
  };

  const remove = id => {
    adminClient.delete(`/subjects/${id}`).then(() => {
      dispatch(setSubjects(subjects.filter(s => s.id !== id)));
    });
  };

  return (
    <div>
      <h1>Предметы</h1>
      <div>
        <input
          placeholder="Название"
          value={name}
          onChange={e => setName(e.target.value)}
        />
        <input
          placeholder="ID школы"
          value={schoolId}
          onChange={e => setSchoolId(e.target.value)}
        />
        <button onClick={addSubject}>Добавить</button>
      </div>
      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Название</th>
            <th>Школа</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {subjects.map(s => (
            <tr key={s.id}>
              <td>{s.id}</td>
              <td>
                {editId === s.id ? (
                  <input
                    value={editName}
                    onChange={e => setEditName(e.target.value)}
                  />
                ) : (
                  s.name
                )}
              </td>
              <td>
                {editId === s.id ? (
                  <input
                    value={editSchoolId}
                    onChange={e => setEditSchoolId(e.target.value)}
                  />
                ) : (
                  s.school_id
                )}
              </td>
              <td>
                {editId === s.id ? (
                  <button onClick={saveEdit}>Сохранить</button>
                ) : (
                  <>
                    <button onClick={() => startEdit(s)}>Ред.</button>
                    <button onClick={() => remove(s.id)}>X</button>
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
