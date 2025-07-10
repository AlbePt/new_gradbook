import React, { useState } from 'react'

function LoginPane({ onLogin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const submit = async (e) => {
    e.preventDefault()
    await onLogin(username, password)
  }

  return (
    <div>
      <h3 className="mb-3">Вход</h3>
      <form onSubmit={submit} className="row g-3" style={{ maxWidth: 300 }}>
        <div className="col-12">
          <label className="form-label">Логин</label>
          <input type="text" className="form-control" value={username} onChange={(e) => setUsername(e.target.value)} required />
        </div>
        <div className="col-12">
          <label className="form-label">Пароль</label>
          <input type="password" className="form-control" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        <div className="col-12">
          <button type="submit" className="btn btn-primary">Войти</button>
        </div>
      </form>
    </div>
  )
}

export default LoginPane
