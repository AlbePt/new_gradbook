import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import adminClient from '../../../api/adminClient.js';
import { setTeachers } from './teacherSlice.js';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

export default function TeacherList() {
  const dispatch = useDispatch();
  const teachers = useSelector(state => state.teachers.items);
  const list = Array.isArray(teachers) ? teachers : [];

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
        dispatch(setTeachers([...list, res.data]));
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
        dispatch(setTeachers(list.map(t => (t.id === editId ? res.data : t))));
        setEditId(null);
      })
      .catch(() => {});
  };

  const remove = id => {
    adminClient.delete(`/teachers/${id}`).then(() => {
      dispatch(setTeachers(list.filter(t => t.id !== id)));
    });
  };

  return (
    <div>
      <h1>Преподаватели</h1>
      <Button variant="contained" className="add-btn" onClick={() => setAddOpen(true)}>
        Добавить
      </Button>
      <Dialog open={addOpen} onClose={() => setAddOpen(false)}>
        <DialogTitle>Новый преподаватель</DialogTitle>
        <DialogContent sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
          <TextField label="Имя" value={firstName} onChange={e => setFirstName(e.target.value)} />
          <TextField label="Фамилия" value={lastName} onChange={e => setLastName(e.target.value)} />
          <TextField label="Контакт" value={contactInfo} onChange={e => setContactInfo(e.target.value)} />
          <TextField label="ID школы" value={schoolId} onChange={e => setSchoolId(e.target.value)} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAddOpen(false)}>Отмена</Button>
          <Button onClick={addTeacher} variant="contained">
            Сохранить
          </Button>
        </DialogActions>
      </Dialog>
      <table className="data-table">
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
          {list.map(t => (
            <tr key={t.id}>
              <td>{t.id}</td>
              <td>
                {editId === t.id ? (
                  <input
                    value={editFirstName}
                    onChange={e => setEditFirstName(e.target.value)}
                  />
                ) : (
                  t.first_name
                )}
              </td>
              <td>
                {editId === t.id ? (
                  <input
                    value={editLastName}
                    onChange={e => setEditLastName(e.target.value)}
                  />
                ) : (
                  t.last_name
                )}
              </td>
              <td>
                {editId === t.id ? (
                  <input
                    value={editContactInfo}
                    onChange={e => setEditContactInfo(e.target.value)}
                  />
                ) : (
                  t.contact_info
                )}
              </td>
              <td>
                {editId === t.id ? (
                  <input
                    value={editSchoolId}
                    onChange={e => setEditSchoolId(e.target.value)}
                  />
                ) : (
                  t.school_id
                )}
              </td>
              <td>
                {editId === t.id ? (
                  <button onClick={saveEdit}>Сохранить</button>
                ) : (
                  <>
                    <button onClick={() => startEdit(t)}>Ред.</button>
                    <button onClick={() => remove(t.id)}>X</button>
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
