import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import adminClient from '../../../api/adminClient.js';
import { setSubjects } from './subjectSlice.js';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

export default function SubjectList() {
  const dispatch = useDispatch();
  const subjects = useSelector(state => state.subjects.items);
  const list = Array.isArray(subjects) ? subjects : [];
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
        dispatch(setSubjects([...list, res.data]));
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
        dispatch(setSubjects(list.map(s => (s.id === editId ? res.data : s))));
        setEditId(null);
      })
      .catch(() => {});
  };

  const remove = id => {
    adminClient.delete(`/subjects/${id}`).then(() => {
      dispatch(setSubjects(list.filter(s => s.id !== id)));
    });
  };

  return (
    <div>
      <h1>Предметы</h1>
      <Button variant="contained" className="add-btn" onClick={() => setAddOpen(true)}>
        Добавить
      </Button>
      <Dialog open={addOpen} onClose={() => setAddOpen(false)}>
        <DialogTitle>Новый предмет</DialogTitle>
        <DialogContent sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
          <TextField label="Название" value={name} onChange={e => setName(e.target.value)} />
          <TextField
            label="ID школы"
            value={schoolId}
            onChange={e => setSchoolId(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAddOpen(false)}>Отмена</Button>
          <Button onClick={addSubject} variant="contained">
            Сохранить
          </Button>
        </DialogActions>
      </Dialog>
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
          {list.map(s => (
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
