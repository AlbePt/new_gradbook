import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { FiMenu } from 'react-icons/fi';

const links = [
  { to: 'cities', label: 'Города' },
  { to: 'schools', label: 'Школы' },
  { to: 'academic-years', label: 'Учебные годы' },
  { to: 'classes', label: 'Классы' },
  { to: 'subjects', label: 'Предметы' },
  { to: 'teachers', label: 'Учителя' },
  { to: 'students', label: 'Студенты' },
  { to: 'parents', label: 'Родители' },
  { to: 'attendance', label: 'Посещения' },
  { to: 'grades', label: 'Оценки' },
  { to: 'teacher-subjects', label: 'Назначения' },
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
          <li key={link.to}>
            <NavLink to={link.to}>{link.label}</NavLink>
          </li>
        ))}
      </ul>
    </aside>
  );
}
