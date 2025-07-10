import React, { useEffect, useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function UserManagement({ token, schoolId }) {
  const [users, setUsers] = useState([])
  const [form, setForm] = useState({ username: '', password: '', role: 'teacher' })

  const loadUsers = async () => {
    const res = await fetch(`${API_URL}/users?school_id=${schoolId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (res.ok) setUsers(await res.json())
  }

  useEffect(() => { if (token && schoolId) loadUsers() }, [token, schoolId])

  const createUser = async () => {
    const res = await fetch(`${API_URL}/users`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ ...form, school_id: Number(schoolId) })
    })
    if (res.ok) {
      setForm({ username: '', password: '', role: 'teacher' })
      loadUsers()
    } else {
      alert('Ошибка создания пользователя')
    }
  }

  const deleteUser = async id => {
    if (!confirm('Удалить пользователя?')) return
    const res = await fetch(`${API_URL}/users/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` }
    })
    if (res.ok) loadUsers()
  }

  return (
    <div>
      <h5>Пользователи школы</h5>
      <table className="table table-sm">
        <thead>
          <tr><th>ID</th><th>Логин</th><th>Роль</th><th></th></tr>
        </thead>
        <tbody>
          {users.map(u => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.username}</td>
              <td>{u.role}</td>
              <td><button className="btn btn-sm btn-danger" onClick={() => deleteUser(u.id)}>Удалить</button></td>
            </tr>
          ))}
        </tbody>
      </table>
      <h6>Добавить пользователя</h6>
      <div className="row g-2 mb-3">
        <div className="col"><input className="form-control" placeholder="Логин" value={form.username} onChange={e => setForm(f => ({...f, username: e.target.value}))} /></div>
        <div className="col"><input type="password" className="form-control" placeholder="Пароль" value={form.password} onChange={e => setForm(f => ({...f, password: e.target.value}))} /></div>
        <div className="col">
          <select className="form-select" value={form.role} onChange={e => setForm(f => ({...f, role: e.target.value}))}>
            <option value="administrator">Администратор</option>
            <option value="teacher">Учитель</option>
            <option value="student">Ученик</option>
            <option value="parent">Родитель</option>
          </select>
        </div>
        <div className="col-auto"><button className="btn btn-primary" onClick={createUser}>Добавить</button></div>
      </div>
    </div>
  )
}

export default UserManagement
