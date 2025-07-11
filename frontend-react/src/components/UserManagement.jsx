/**
 * UserManagement – CRUD interface for managing school users.
 */
import React, { useEffect, useState } from 'react';
import DataTable from './DataTable';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function UserManagement({ token, schoolId }) {
  const [users, setUsers] = useState([]);
  const [teachers, setTeachers] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [classes, setClasses] = useState([]);

  const [showAdmin, setShowAdmin] = useState(false);
  const [adminForm, setAdminForm] = useState({ username: '', password: '', full_name: '' });

  const [showTeacher, setShowTeacher] = useState(false);
  const [teacherForm, setTeacherForm] = useState({
    username: '',
    password: '',
    mode: 'existing',
    teacher_id: '',
    teacher_full_name: '',
    contact_info: '',
    subject_id: '',
    class_id: '',
  });

  const loadUsers = async () => {
    const res = await fetch(`${API_URL}/users?school_id=${schoolId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (res.ok) setUsers(await res.json());
  };

  const loadTeachers = async () => {
    const res = await fetch(`${API_URL}/teachers?limit=1000`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (res.ok) {
      const data = await res.json();
      setTeachers(data.filter((t) => t.school_id === Number(schoolId)));
    }
  };

  const loadSubjects = async () => {
    const res = await fetch(`${API_URL}/subjects`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (res.ok) setSubjects(await res.json());
  };

  const loadClasses = async () => {
    const res = await fetch(`${API_URL}/classes?school_id=${schoolId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (res.ok) setClasses(await res.json());
  };

  useEffect(() => {
    if (token && schoolId) {
      loadUsers();
      loadTeachers();
      loadClasses();
    }
  }, [token, schoolId]);

  useEffect(() => {
    if (token) loadSubjects();
  }, [token]);

  const createAdministrator = async () => {
    const res = await fetch(`${API_URL}/users/administrators`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ ...adminForm, school_id: Number(schoolId) }),
    });
    if (res.ok) {
      setShowAdmin(false);
      setAdminForm({ username: '', password: '', full_name: '' });
      loadUsers();
    } else {
      alert('Ошибка создания администратора');
    }
  };

  const createTeacher = async () => {
    const body = {
      username: teacherForm.username,
      password: teacherForm.password,
      school_id: Number(schoolId),
      mode: teacherForm.mode,
      teacher_id: teacherForm.mode === 'existing' ? Number(teacherForm.teacher_id) : undefined,
      teacher_full_name: teacherForm.mode === 'new' ? teacherForm.teacher_full_name : undefined,
      contact_info: teacherForm.mode === 'new' ? teacherForm.contact_info : undefined,
    };
    const res = await fetch(`${API_URL}/users/teachers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify(body),
    });
    if (res.ok) {
      setShowTeacher(false);
      setTeacherForm({
        username: '',
        password: '',
        mode: 'existing',
        teacher_id: '',
        teacher_full_name: '',
        contact_info: '',
        subject_id: '',
        class_id: '',
      });
      loadUsers();
    } else {
      alert('Ошибка создания учителя');
    }
  };

  const deleteUser = async (id) => {
    if (!confirm('Удалить пользователя?')) return;
    const res = await fetch(`${API_URL}/users/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` },
    });
    if (res.ok) loadUsers();
  };

  return (
    <div>
      <h5>Пользователи школы</h5>
      <DataTable>
        <thead>
          <tr>
            <th>ID</th>
            <th>Логин</th>
            <th>Роль</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {users.map((u) => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.username}</td>
              <td>{u.role}</td>
              <td>
                <button className="btn danger btn-sm" onClick={() => deleteUser(u.id)}>
                  Удалить
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </DataTable>
      <div className="mb-3">
        <button className="btn primary me-2" onClick={() => setShowAdmin(true)}>
          Добавить администратора
        </button>
        <button className="btn primary me-2" onClick={() => setShowTeacher(true)}>
          Добавить учителя
        </button>
        <button className="btn primary me-2" disabled onClick={() => alert('В разработке')}>
          Добавить ученика
        </button>
        <button className="btn primary" disabled onClick={() => alert('В разработке')}>
          Добавить родителя
        </button>
      </div>

      {showAdmin && (
        <div className="modal d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Добавить администратора</h5>
                <button
                  type="button"
                  className="btn-close"
                  onClick={() => setShowAdmin(false)}
                ></button>
              </div>
              <div className="modal-body">
                <div className="mb-2">
                  <input
                    className="form-control"
                    placeholder="Логин"
                    value={adminForm.username}
                    onChange={(e) => setAdminForm((f) => ({ ...f, username: e.target.value }))}
                  />
                </div>
                <div className="mb-2">
                  <input
                    type="password"
                    className="form-control"
                    placeholder="Пароль"
                    value={adminForm.password}
                    onChange={(e) => setAdminForm((f) => ({ ...f, password: e.target.value }))}
                  />
                </div>
                <div className="mb-2">
                  <input
                    className="form-control"
                    placeholder="ФИО"
                    value={adminForm.full_name}
                    onChange={(e) => setAdminForm((f) => ({ ...f, full_name: e.target.value }))}
                  />
                </div>
              </div>
              <div className="modal-footer">
                <button className="btn" onClick={() => setShowAdmin(false)}>
                  Отмена
                </button>
                <button className="btn primary" onClick={createAdministrator}>
                  Добавить
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {showTeacher && (
        <div className="modal d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Добавить учителя</h5>
                <button
                  type="button"
                  className="btn-close"
                  onClick={() => setShowTeacher(false)}
                ></button>
              </div>
              <div className="modal-body">
                <div className="mb-2">
                  <input
                    className="form-control"
                    placeholder="Логин"
                    value={teacherForm.username}
                    onChange={(e) => setTeacherForm((f) => ({ ...f, username: e.target.value }))}
                  />
                </div>
                <div className="mb-3">
                  <input
                    type="password"
                    className="form-control"
                    placeholder="Пароль"
                    value={teacherForm.password}
                    onChange={(e) => setTeacherForm((f) => ({ ...f, password: e.target.value }))}
                  />
                </div>
                <div className="mb-2">
                  <div className="form-check form-check-inline">
                    <input
                      className="form-check-input"
                      type="radio"
                      value="existing"
                      checked={teacherForm.mode === 'existing'}
                      onChange={(e) => setTeacherForm((f) => ({ ...f, mode: e.target.value }))}
                    />
                    <label className="form-check-label">Существующий</label>
                  </div>
                  <div className="form-check form-check-inline">
                    <input
                      className="form-check-input"
                      type="radio"
                      value="new"
                      checked={teacherForm.mode === 'new'}
                      onChange={(e) => setTeacherForm((f) => ({ ...f, mode: e.target.value }))}
                    />
                    <label className="form-check-label">Новый</label>
                  </div>
                </div>
                {teacherForm.mode === 'existing' ? (
                  <div className="mb-2">
                    <select
                      className="form-select"
                      value={teacherForm.teacher_id}
                      onChange={(e) =>
                        setTeacherForm((f) => ({ ...f, teacher_id: e.target.value }))
                      }
                    >
                      <option value="">Выберите учителя</option>
                      {teachers.map((t) => (
                        <option key={t.id} value={t.id}>
                          {t.full_name}
                        </option>
                      ))}
                    </select>
                  </div>
                ) : (
                  <>
                    <div className="mb-2">
                      <input
                        className="form-control"
                        placeholder="ФИО"
                        value={teacherForm.teacher_full_name}
                        onChange={(e) =>
                          setTeacherForm((f) => ({ ...f, teacher_full_name: e.target.value }))
                        }
                      />
                    </div>
                    <div className="mb-2">
                      <select
                        className="form-select"
                        value={teacherForm.subject_id}
                        onChange={(e) =>
                          setTeacherForm((f) => ({ ...f, subject_id: e.target.value }))
                        }
                      >
                        <option value="">Предмет</option>
                        {subjects.map((s) => (
                          <option key={s.id} value={s.id}>
                            {s.name}
                          </option>
                        ))}
                      </select>
                    </div>
                    <div className="mb-2">
                      <select
                        className="form-select"
                        value={teacherForm.class_id}
                        onChange={(e) =>
                          setTeacherForm((f) => ({ ...f, class_id: e.target.value }))
                        }
                      >
                        <option value="">Класс (если классный рук.)</option>
                        {classes.map((c) => (
                          <option key={c.id} value={c.id}>
                            {c.name}
                          </option>
                        ))}
                      </select>
                    </div>
                    <div className="mb-2">
                      <input
                        className="form-control"
                        placeholder="Контактная информация"
                        value={teacherForm.contact_info}
                        onChange={(e) =>
                          setTeacherForm((f) => ({ ...f, contact_info: e.target.value }))
                        }
                      />
                    </div>
                  </>
                )}
              </div>
              <div className="modal-footer">
                <button className="btn" onClick={() => setShowTeacher(false)}>
                  Отмена
                </button>
                <button className="btn primary" onClick={createTeacher}>
                  Добавить
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default UserManagement;
