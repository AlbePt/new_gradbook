import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import adminClient from '../../../api/adminClient.js';
import { setRegions } from './regionSlice.js';

export default function RegionList() {
  const dispatch = useDispatch();
  const regions = useSelector(state => state.regions.items);
  const list = Array.isArray(regions) ? regions : [];
  const [name, setName] = useState('');
  const [editId, setEditId] = useState(null);
  const [editName, setEditName] = useState('');

  useEffect(() => {
    adminClient
      .get('/regions')
      .then(res => dispatch(setRegions(res.data)))
      .catch(() => {});
  }, [dispatch]);

  const addRegion = () => {
    adminClient
      .post('/regions', { name })
      .then(res => {
        dispatch(setRegions([...list, res.data]));
        setName('');
      })
      .catch(() => {});
  };

  const startEdit = r => {
    setEditId(r.id);
    setEditName(r.name);
  };

  const saveEdit = () => {
    adminClient
      .put(`/regions/${editId}`, { name: editName })
      .then(res => {
        dispatch(setRegions(list.map(r => (r.id === editId ? res.data : r))));
        setEditId(null);
      })
      .catch(() => {});
  };

  const remove = id => {
    adminClient.delete(`/regions/${id}`).then(() => {
      dispatch(setRegions(list.filter(r => r.id !== id)));
    });
  };

  return (
    <div>
      <h1>Регионы</h1>
      <div>
        <input
          placeholder="Название"
          value={name}
          onChange={e => setName(e.target.value)}
        />
        <button onClick={addRegion}>Добавить</button>
      </div>
      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Название</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {list.map(r => (
            <tr key={r.id}>
              <td>{r.id}</td>
              <td>
                {editId === r.id ? (
                  <input value={editName} onChange={e => setEditName(e.target.value)} />
                ) : (
                  r.name
                )}
              </td>
              <td>
                {editId === r.id ? (
                  <button onClick={saveEdit}>Сохранить</button>
                ) : (
                  <>
                    <button onClick={() => startEdit(r)}>Ред.</button>
                    <button onClick={() => remove(r.id)}>X</button>
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
