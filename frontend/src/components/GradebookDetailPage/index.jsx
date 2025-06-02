// src/components/GradebookDetailPage/index.jsx
import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { fetchGradebookById, removeGradebook } from '../../store/gradebookSlice';
import GradebookItem from '../GradebookItem';

export default function GradebookDetailPage() {
  const { id } = useParams();
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { current, status, error } = useSelector(state => state.gradebooks);

  useEffect(() => {
    dispatch(fetchGradebookById(id));
  }, [dispatch, id]);

  const handleDelete = async () => {
    const confirmed = window.confirm('Вы уверены, что хотите удалить этот журнал?');
    if (confirmed) {
      await dispatch(removeGradebook(id));
      navigate('/');
    }
  };

  if (status === 'loading') return <p>Загрузка...</p>;
  if (status === 'failed') return <p>Ошибка: {error}</p>;
  if (!current) return <p>Журнал не найден.</p>;

  return (
    <div>
      <GradebookItem gradebook={current} />
      <button onClick={handleDelete} style={{ marginTop: '1rem' }}>
        Удалить журнал
      </button>
    </div>
  );
}