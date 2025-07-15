/**
 * App – main application container.
 */
import { useState } from 'react';
import Topbar from './components/Topbar';
import Sidebar from './components/Sidebar';
import LoginPane from './components/LoginPane';
import Dashboard from './components/Dashboard';
import UserManagement from './components/UserManagement';
import PagePlaceholder from './components/PagePlaceholder';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [token, setToken] = useState(() => localStorage.getItem('token'));
  const [schoolId, setSchoolId] = useState('');
  const [page, setPage] = useState('reports-cr');

  const login = async (username, password) => {
    const form = new URLSearchParams();
    form.append('username', username);
    form.append('password', password);
    const res = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: form.toString(),
    });
    if (!res.ok) {
      alert('Ошибка входа');
      return;
    }
    const data = await res.json();
    localStorage.setItem('token', data.access_token);
    setToken(data.access_token);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setSchoolId('');
  };

  return (
    <>
      <Topbar onLogout={logout} />
      <div className="d-flex">
        <Sidebar
          token={token}
          schoolId={schoolId}
          onSchoolChange={setSchoolId}
          onSelect={setPage}
          current={page}
        />
        <main className="flex-grow-1">
          <div className="container-fluid py-4">
            {!token ? (
              <LoginPane onLogin={login} />
            ) : page === 'settings' ? (
              <UserManagement token={token} schoolId={schoolId} onSchoolChange={setSchoolId} />
            ) : page === 'students' || page === 'subjects' || page === 'grades' ? (
              <PagePlaceholder page={page} />
            ) : page.startsWith('reports') ? (
              <Dashboard token={token} schoolId={schoolId} role={page.split('-')[1]} />
            ) : (
              <PagePlaceholder page={page} />
            )}
          </div>
        </main>
      </div>
    </>
  );
}

export default App;
