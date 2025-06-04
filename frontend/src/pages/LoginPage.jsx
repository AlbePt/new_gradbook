import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './login.css';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = e => {
    e.preventDefault();
    // TODO: authenticate via API
    navigate('/');
  };

  return (
    <div className="login-page">
      <form className="login-form" onSubmit={handleSubmit}>
        <h2>Вход</h2>
        <label>
          Имя пользователя
          <input
            type="text"
            value={username}
            onChange={e => setUsername(e.target.value)}
            required
          />
        </label>
        <label>
          Пароль
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
        </label>
        <button type="submit">Войти</button>
      </form>
    </div>
  );
}
