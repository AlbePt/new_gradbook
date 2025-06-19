import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import adminClient from '../../../api/adminClient.js';
import { setTeachers } from './teacherSlice.js';

export default function TeacherList() {
  const dispatch = useDispatch();
  const teachers = useSelector(state => state.teachers.items) || [];

  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [contactInfo, setContactInfo] = useState('');
  const [schoolId, setSchoolId] = useState('');
  const [addOpen, setAddOpen] = useState(false);

  const [editId, setEditId] = useState(null);
  const [editFirstName, setEditFirstName] = useState('');
  const [editLastName, setEditLastName] = useState('');
  const [editContactInfo, setEditContactInfo] = useState('');
  const [editSchoolId, setEditSchoolId] = useState('');

  useEffect(() => {
    adminClient
      .get('/teachers')
      .then(res => dispatch(setTeachers(res.data)))
      .catch(() => {});
  }, [dispatch]);

  const addTeacher = () => {
    adminClient
      .post('/teachers', {
        first_name: firstName,
        last_name: lastName,
        contact_info: contactInfo || undefined,
        school_id: Number(schoolId),
      })
      .then(res => {
        dispatch(setTeachers([...teachers, res.data]));
        setFirstName('');
        setLastName('');
        setContactInfo('');
        setSchoolId('');
        setAddOpen(false);
      })
      .catch(() => {});
  };

  const startEdit = t => {
    setEditId(t.id);
    setEditFirstName(t.first_name);
    setEditLastName(t.last_name);
    setEditContactInfo(t.contact_info || '');
    setEditSchoolId(t.school_id);
  };

  const saveEdit = () => {
    adminClient
      .put(`/teachers/${editId}`, {
        first_name: editFirstName,
        last_name: editLastName,
        contact_info: editContactInfo || undefined,
        school_id: Number(editSchoolId),
      })
      .then(res => {
        dispatch(setTeachers(teachers.map(t => (t.id === editId ? res.data : t))));
        setEditId(null);
      })
      .catch(() => {});
  };

  const remove = id => {
    adminClient.delete(`/teachers/${id}`).then(() => {
      dispatch(setTeachers(teachers.filter(t => t.id !== id)));
    });
  };

  return (
    <div>
      <h1 className="mb-3">Преподаватели</h1>
      <button className="btn btn-primary mb-3" onClick={() => setAddOpen(true)}>
        Добавить
      </button>

      {addOpen && (
        <div className="modal d-block" tabIndex="-1" onClick={() => setAddOpen(false)}>
          <div className="modal-dialog" onClick={e => e.stopPropagation()}>
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Новый преподаватель</h5>
                <button type="button" className="btn-close" onClick={() => setAddOpen(false)}></button>
              </div>
              <div className="modal-body">
                <div className="mb-3">
                  <label className="form-label">Имя</label>
                  <input className="form-control" value={firstName} onChange={e => setFirstName(e.target.value)} />
                </div>
                <div className="mb-3">
                  <label className="form-label">Фамилия</label>
                  <input className="form-control" value={lastName} onChange={e => setLastName(e.target.value)} />
                </div>
                <div className="mb-3">
                  <label className="form-label">Контакт</label>
                  <input className="form-control" value={contactInfo} onChange={e => setContactInfo(e.target.value)} />
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
                <button className="btn btn-primary" onClick={addTeacher}>
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
            <th>Имя</th>
            <th>Фамилия</th>
            <th>Контакт</th>
            <th>Школа</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {teachers.map(t => (
            <tr key={t.id}>
              <td>{t.id}</td>
              <td>
                {editId === t.id ? (
                  <input value={editFirstName} onChange={e => setEditFirstName(e.target.value)} />
                ) : (
                  t.first_name
                )}
              </td>
              <td>
                {editId === t.id ? (
                  <input value={editLastName} onChange={e => setEditLastName(e.target.value)} />
                ) : (
                  t.last_name
                )}
              </td>
              <td>
                {editId === t.id ? (
                  <input value={editContactInfo} onChange={e => setEditContactInfo(e.target.value)} />
                ) : (
                  t.contact_info
                )}
              </td>
              <td>
                {editId === t.id ? (
                  <input value={editSchoolId} onChange={e => setEditSchoolId(e.target.value)} />
                ) : (
                  t.school_id
                )}
              </td>
              <td>
                {editId === t.id ? (
                  <button className="btn btn-sm btn-primary" onClick={saveEdit}>Сохранить</button>
                ) : (
                  <>
                    <button className="btn btn-sm btn-link" onClick={() => startEdit(t)}>
                      Ред.
                    </button>
                    <button className="btn btn-sm btn-link text-danger" onClick={() => remove(t.id)}>
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
