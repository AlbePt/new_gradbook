import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';

const links = [
  { to: 'subjects', label: 'Предметы' },
  { to: 'teachers', label: 'Преподаватели' },
];

export default function Sidebar() {
  const [open, setOpen] = useState(true);

  return (
    <nav className={`sidebar bg-light p-3 ${open ? '' : 'collapsed'}`}>
      <button
        className="btn btn-sm btn-outline-secondary d-lg-none mb-3"
        onClick={() => setOpen(o => !o)}
      >
        ☰
      </button>
      <ul className="nav nav-pills flex-column">
        {links.map(link => (
          <li className="nav-item" key={link.label}>
            <NavLink to={link.to} end className="nav-link">
              {link.label}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  );
}
