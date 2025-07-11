/**
 * UserMenu – dropdown with profile actions.
 */
import React from 'react';

function UserMenu({ onLogout }) {
  return (
    <div className="dropdown profile">
      <span className="avatar">A</span>
      <span className="name">Админ</span>
      <i
        className="bi bi-chevron-down"
        role="button"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      ></i>
      <ul className="dropdown-menu dropdown-menu-end">
        <li>
          <button className="dropdown-item" onClick={onLogout} type="button">
            Выход
          </button>
        </li>
      </ul>
    </div>
  );
}

export default UserMenu;
