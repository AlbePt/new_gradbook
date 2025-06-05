import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { FiMenu } from 'react-icons/fi';

const links = [
  { to: '#a', label: 'Сущность A' },
  { to: '#b', label: 'Сущность B' },
  { to: '#c', label: 'Сущность C' },
  { to: '#d', label: 'Сущность D' },
];

export default function Sidebar() {
  const [open, setOpen] = useState(true);
  return (
    <aside className={`sidebar ${open ? '' : 'collapsed'}`}>
      <button className="toggle" onClick={() => setOpen(!open)}>
        <FiMenu />
      </button>
      <h2>НазваниеРаздела</h2>
      <ul>
        {links.map(link => (
          <li key={link.label}>
            <NavLink to={link.to}>{link.label}</NavLink>
          </li>
        ))}
      </ul>
    </aside>
  );
}
