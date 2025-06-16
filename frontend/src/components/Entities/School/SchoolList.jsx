import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import adminClient from '../../../api/adminClient.js';
import { setSchools } from './schoolSlice.js';

export default function SchoolList() {
  const dispatch = useDispatch();
  const schools = useSelector(state => state.schools.items);
  const list = Array.isArray(schools) ? schools : [];
  const [name, setName] = useState('');
  const [cityId, setCityId] = useState('');
  const [editId, setEditId] = useState(null);
  const [editName, setEditName] = useState('');
  const [editCityId, setEditCityId] = useState('');

  useEffect(() => {
    adminClient
      .get('/schools')
      .then(res => dispatch(setSchools(res.data)))
      .catch(() => {});
  }, [dispatch]);

  const addSchool = () => {
    adminClient
      .post('/schools', { name, city_id: Number(cityId) })
      .then(res => {
        dispatch(setSchools([...list, res.data]));
        setName('');
        setCityId('');
      })
      .catch(() => {});
  };

  const startEdit = s => {
    setEditId(s.id);
    setEditName(s.name);
    setEditCityId(s.city_id);
  };

  const saveEdit = () => {
    adminClient
      .put(`/schools/${editId}`, { name: editName, city_id: Number(editCityId) })
      .then(res => {
        dispatch(setSchools(list.map(s => (s.id === editId ? res.data : s))));
        setEditId(null);
      })
      .catch(() => {});
  };

  const remove = id => {
    adminClient.delete(`/schools/${id}`).then(() => {
      dispatch(setSchools(list.filter(s => s.id !== id)));
    });
  };

  return (
    <div>
      <h1>Школы</h1>
      <div>
        <input
          placeholder="Название"
          value={name}
          onChange={e => setName(e.target.value)}
        />
        <input
          placeholder="ID города"
          value={cityId}
          onChange={e => setCityId(e.target.value)}
        />
        <button onClick={addSchool}>Добавить</button>
      </div>
      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Название</th>
            <th>Город</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {list.map(s => (
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
                  <input value={editCityId} onChange={e => setEditCityId(e.target.value)} />
                ) : (
                  s.city_id
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
