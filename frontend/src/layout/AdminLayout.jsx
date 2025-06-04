import React from 'react';
import { Link } from 'react-router-dom';
import './admin.css';

export default function AdminLayout({ children }) {
  return (
    <div className="admin-layout">
      <header className="admin-header">
        <div className="logo">Gradebook</div>
        <nav className="header-nav">
          <Link to="/" className="admin-btn">Панель управления</Link>
        </nav>
      </header>
      <div className="admin-body">
        <aside className="sidebar">
          <ul>
            <li><Link to="/regions">Регионы</Link></li>
            <li><Link to="/cities">Города</Link></li>
            <li><Link to="/schools">Школы</Link></li>
            <li><Link to="/users">Пользователи</Link></li>
          </ul>
        </aside>
        <main className="content">{children}</main>
      </div>
    </div>
  );
}
