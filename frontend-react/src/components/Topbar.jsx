/**
 * Topbar – fixed navigation bar with burger and user menu.
 */
import React from 'react';
import UserMenu from './UserMenu';

function Topbar({ onLogout }) {
  return (
    <header className="topbar">
      <div className="navbar-left">
        <i className="bi bi-table" />
      </div>
      <div className="top-actions">
        <button className="search-btn" aria-label="Поиск">
          <i className="bi bi-search" />
        </button>
        <UserMenu onLogout={onLogout} />
      </div>
    </header>
  );
}

export default Topbar;
