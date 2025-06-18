import React from 'react';
import { NavLink } from 'react-router-dom';
import '../../styles/header.css';

const menu = [
  { to: '/', label: 'Главная' },
  { to: '/journal', label: 'Журнал' },
  { to: '/planning', label: 'Планирование' },
  { to: '/admin', label: 'Панель управления' },
  { to: '/reports', label: 'Отчёты' },
];

export default function Header() {
  return (
    <header className="header">
      <div className="top-bar">
        <div className="logo-square" />
        <span className="title">Электронный журнал Свердловской области</span>
        <NavLink to="/help" className="help-link">
          Справка
        </NavLink>
      </div>
      <nav className="nav-menu">
        <span className="school">МАОУ СОШ № 9</span>
        {menu.map(item => (
          <NavLink key={item.to} to={item.to} className={({ isActive }) => (isActive ? 'active' : '')}>
            {item.label}
          </NavLink>
        ))}
        <span className="dots">⋮</span>
        <span className="profile">Габдрахманов А. А.</span>
        <span className="logout">⎘</span>
      </nav>
    </header>
  );
}
