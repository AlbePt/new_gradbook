import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { FiMenu } from 'react-icons/fi';

const links = [
  { to: 'subjects', label: 'Предметы' },
  { to: 'teachers', label: 'Преподаватели' },
];

export default function Sidebar() {
  const [open, setOpen] = useState(true);
  return (
    <aside className={`sidebar ${open ? '' : 'collapsed'}`}>
      <button className="toggle" onClick={() => setOpen(!open)}>
        <FiMenu />
      </button>
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
