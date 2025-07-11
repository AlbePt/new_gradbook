/**
 * UserMenu – dropdown with profile actions.
 */
import React from 'react';

function UserMenu({ onLogout }) {
  return (
    <li className="nav-item dropdown">
      <a
        className="nav-link dropdown-toggle"
        href="#"
        role="button"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        <img src="https://placehold.co/32x32" className="rounded-circle me-1" alt="" /> Админ
      </a>
      <ul className="dropdown-menu dropdown-menu-end">
        <li>
          <a className="dropdown-item" href="#">
            Настройки
          </a>
        </li>
        <li>
          <button className="dropdown-item" onClick={onLogout} type="button">
            Выход
          </button>
        </li>
      </ul>
    </li>
  );
}

export default UserMenu;
