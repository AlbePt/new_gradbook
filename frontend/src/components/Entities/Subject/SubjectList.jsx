import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import adminClient from '../../../api/adminClient.js';
import { setSubjects } from './subjectSlice.js';

export default function SubjectList() {
  const dispatch = useDispatch();
  const subjects = useSelector(state => state.subjects.items) || [];
  const [name, setName] = useState('');
  const [schoolId, setSchoolId] = useState('');
  const [addOpen, setAddOpen] = useState(false);
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
        setAddOpen(false);
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
        dispatch(setSubjects(subjects.map(s => (s.id === editId ? res.data : s))));
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
      <h1 className="mb-3">Предметы</h1>
      <button className="btn btn-primary mb-3" onClick={() => setAddOpen(true)}>
        Добавить
      </button>

      {addOpen && (
        <div className="modal d-block" tabIndex="-1" onClick={() => setAddOpen(false)}>
          <div className="modal-dialog" onClick={e => e.stopPropagation()}>
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Новый предмет</h5>
                <button type="button" className="btn-close" onClick={() => setAddOpen(false)}></button>
              </div>
              <div className="modal-body">
                <div className="mb-3">
                  <label className="form-label">Название</label>
                  <input className="form-control" value={name} onChange={e => setName(e.target.value)} />
                </div>
                <div className="mb-3">
                  <label className="form-label">ID школы</label>
                  <input className="form-control" value={schoolId} onChange={e => setSchoolId(e.target.value)} />
                </div>
              </div>
              <div className="modal-footer">
                <button className="btn btn-secondary" onClick={() => setAddOpen(false)}>
                  Отмена
                </button>
                <button className="btn btn-primary" onClick={addSubject}>
                  Сохранить
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      <table className="table table-hover align-middle">
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
                  <input value={editName} onChange={e => setEditName(e.target.value)} />
                ) : (
                  s.name
                )}
              </td>
              <td>
                {editId === s.id ? (
                  <input value={editSchoolId} onChange={e => setEditSchoolId(e.target.value)} />
                ) : (
                  s.school_id
                )}
              </td>
              <td>
                {editId === s.id ? (
                  <button className="btn btn-sm btn-primary" onClick={saveEdit}>Сохранить</button>
                ) : (
                  <>
                    <button className="btn btn-sm btn-link" onClick={() => startEdit(s)}>
                      Ред.
                    </button>
                    <button className="btn btn-sm btn-link text-danger" onClick={() => remove(s.id)}>
                      X
                    </button>
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
