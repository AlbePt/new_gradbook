// src/components/GradebookEditPage/index.jsx
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchGradebookById, editGradebook } from '../../store/gradebookSlice';
import { useParams, useNavigate } from 'react-router-dom';

export default function GradebookEditPage() {
  const { id } = useParams();
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { current, status, error } = useSelector(state => state.gradebooks);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  useEffect(() => {
    dispatch(fetchGradebookById(id));
  }, [dispatch, id]);

  useEffect(() => {
    if (current) {
      setName(current.name);
      setDescription(current.description);
    }
  }, [current]);

  const handleSubmit = async e => {
    e.preventDefault();
    await dispatch(editGradebook({ id, data: { name, description } }));
    navigate(`/grade/${id}`);
  };

  if (status === 'loading') return <p>Загрузка...</p>;
  if (status === 'failed') return <p>Ошибка: {error}</p>;

  return (
    <form onSubmit={handleSubmit} style={{ padding: '1rem' }}>
      <div>
        <label>Название:</label>
        <input
          type="text"
          value={name}
          onChange={e => setName(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Описание:</label>
        <textarea
          value={description}
          onChange={e => setDescription(e.target.value)}
        />
      </div>
      <button type="submit">Сохранить изменения</button>
    </form>
  );
}