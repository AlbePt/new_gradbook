import React from 'react';
import { NavLink } from 'react-router-dom';
import { FiUser } from 'react-icons/fi';

const menu = [
  { to: '/', label: 'Главная' },
  { to: '/journal', label: 'Журнал' },
  { to: '/planning', label: 'Планирование' },
  { to: '/admin', label: 'Панель управления' },
  { to: '/reports', label: 'Отчёты' },
];

export default function Header() {
  return (
    <header className="app-header">
      <div className="logo-square"></div>
      <nav className="main-menu">
        {menu.map(item => (
          <NavLink key={item.to} to={item.to} className="menu-link">
            {item.label}
          </NavLink>
        ))}
      </nav>
      <div className="bar-right">
        <NavLink to="/help">Справка</NavLink>
        <FiUser />
      </div>
    </header>
  );
}
