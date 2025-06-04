import React from 'react';
import { Link } from 'react-router-dom';
import { FiSettings } from 'react-icons/fi';

export default function Header() {
  return (
    <header className="app-header">
      <div className="logo">
        <Link to="/">SchoolInfoSystem</Link>
      </div>
      <nav className="nav-right">
        <Link to="/admin" className="admin-link">
          <FiSettings /> <span>Панель управления</span>
        </Link>
      </nav>
    </header>
  );
}
