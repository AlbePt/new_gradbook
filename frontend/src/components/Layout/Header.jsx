import React from 'react';
import { NavLink } from 'react-router-dom';
import { FaBook, FaUserCircle } from 'react-icons/fa';

const menu = [
  { to: '/', label: 'Главная' },
  { to: '/journal', label: 'Журнал' },
  { to: '/planning', label: 'Планирование' },
  { to: '/admin', label: 'Панель управления' },
  { to: '/reports', label: 'Отчёты' },
];

export default function Header() {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary fixed-top shadow-sm">
      <div className="container-fluid">
        <NavLink className="navbar-brand d-flex align-items-center gap-2" to="/">
          <FaBook /> Gradebook
        </NavLink>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#mainNav"
          aria-controls="mainNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="mainNav">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            {menu.map(item => (
              <li className="nav-item" key={item.to}>
                <NavLink to={item.to} className="nav-link">
                  {item.label}
                </NavLink>
              </li>
            ))}
          </ul>
          <NavLink to="/help" className="nav-link text-white me-3">
            Справка
          </NavLink>
          <FaUserCircle className="text-white" />
        </div>
      </div>
    </nav>
  );
}
