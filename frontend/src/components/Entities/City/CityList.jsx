import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import adminClient from '../../../api/adminClient.js';
import { setCities } from './citySlice.js';

export default function CityList() {
  const dispatch = useDispatch();
  const cities = useSelector(state => state.cities.items);
  const list = Array.isArray(cities) ? cities : [];
  const [name, setName] = useState('');
  const [regionId, setRegionId] = useState('');
  const [editId, setEditId] = useState(null);
  const [editName, setEditName] = useState('');
  const [editRegionId, setEditRegionId] = useState('');

  useEffect(() => {
    adminClient
      .get('/cities')
      .then(res => dispatch(setCities(res.data)))
      .catch(() => {});
  }, [dispatch]);

  const addCity = () => {
    adminClient
      .post('/cities', { name, region_id: Number(regionId) })
      .then(res => {
        dispatch(setCities([...list, res.data]));
        setName('');
        setRegionId('');
      })
      .catch(() => {});
  };

  const startEdit = c => {
    setEditId(c.id);
    setEditName(c.name);
    setEditRegionId(c.region_id);
  };

  const saveEdit = () => {
    adminClient
      .put(`/cities/${editId}`, { name: editName, region_id: Number(editRegionId) })
      .then(res => {
        dispatch(setCities(list.map(c => (c.id === editId ? res.data : c))));
        setEditId(null);
      })
      .catch(() => {});
  };

  const remove = id => {
    adminClient.delete(`/cities/${id}`).then(() => {
      dispatch(setCities(list.filter(c => c.id !== id)));
    });
  };

  return (
    <div>
      <h1>Города</h1>
      <div>
        <input
          placeholder="Название"
          value={name}
          onChange={e => setName(e.target.value)}
        />
        <input
          placeholder="ID региона"
          value={regionId}
          onChange={e => setRegionId(e.target.value)}
        />
        <button onClick={addCity}>Добавить</button>
      </div>
      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Название</th>
            <th>Регион</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {list.map(c => (
            <tr key={c.id}>
              <td>{c.id}</td>
              <td>
                {editId === c.id ? (
                  <input value={editName} onChange={e => setEditName(e.target.value)} />
                ) : (
                  c.name
                )}
              </td>
              <td>
                {editId === c.id ? (
                  <input value={editRegionId} onChange={e => setEditRegionId(e.target.value)} />
                ) : (
                  c.region_id
                )}
              </td>
              <td>
                {editId === c.id ? (
                  <button onClick={saveEdit}>Сохранить</button>
                ) : (
                  <>
                    <button onClick={() => startEdit(c)}>Ред.</button>
                    <button onClick={() => remove(c.id)}>X</button>
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
