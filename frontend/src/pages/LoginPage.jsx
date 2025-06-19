import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

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
    <div className="d-flex align-items-center justify-content-center min-vh-100 bg-light">
      <form className="p-4 bg-white rounded shadow" style={{ minWidth: '320px' }} onSubmit={handleSubmit}>
        <h2 className="mb-3 text-center">Вход</h2>
        <div className="mb-3">
          <label className="form-label">Имя пользователя</label>
          <input
            type="text"
            className="form-control"
            value={username}
            onChange={e => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Пароль</label>
          <input
            type="password"
            className="form-control"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary w-100">
          Войти
        </button>
      </form>
    </div>
  );
}
