/**
 * Topbar – fixed navigation bar with burger and user menu.
 */
import React from 'react';
import UserMenu from './UserMenu';

function Topbar({ onLogout }) {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary fixed-top shadow-sm">
      <div className="container-fluid">
        <button
          className="btn btn-outline-light d-lg-none me-2"
          id="sidebarToggle"
          aria-label="Toggle sidebar"
        >
          <i className="bi bi-list" />
        </button>
        <a className="navbar-brand" href="#">
          <i className="bi bi-journal-code me-2" />
          Gradebook
        </a>
        <div className="collapse navbar-collapse">
          <ul className="navbar-nav ms-auto align-items-lg-center">
            <li className="nav-item me-lg-3">
              <a className="nav-link" href="#" aria-label="Search">
                <i className="bi bi-search" />
              </a>
            </li>
            <UserMenu onLogout={onLogout} />
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default Topbar;
