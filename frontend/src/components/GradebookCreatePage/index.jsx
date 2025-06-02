// src/components/GradebookCreatePage/index.jsx
import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { addGradebook } from '../../store/gradebookSlice';
import { useNavigate } from 'react-router-dom';

export default function GradebookCreatePage() {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await dispatch(addGradebook(formData));
      navigate('/', { state: { message: 'Журнал успешно создан!' } });
    } catch (error) {
      console.error('Ошибка создания:', error);
      setNotification({
        type: 'error',
        message: 'Не удалось создать журнал. Проверьте данные и попробуйте снова.'
      });
    }
  };

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
      <button type="submit">Создать журнал</button>
    </form>
  );
}