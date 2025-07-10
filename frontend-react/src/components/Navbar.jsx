import React from 'react'

function Navbar({ onLogout }) {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary fixed-top shadow-sm">
      <div className="container-fluid">
        <button className="btn btn-outline-light d-lg-none me-2" data-bs-toggle="offcanvas" data-bs-target="#sidebar">
          <i className="bi bi-list"></i>
        </button>
        <a className="navbar-brand" href="#"><i className="bi bi-journal-code me-2"></i>Gradebook</a>
        <div className="collapse navbar-collapse">
          <ul className="navbar-nav ms-auto align-items-lg-center">
            <li className="nav-item me-lg-3">
              <a className="nav-link" href="#"><i className="bi bi-search"></i></a>
            </li>
            <li className="nav-item dropdown">
              <a className="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                <img src="https://placehold.co/32x32" className="rounded-circle me-1" alt="" /> Админ
              </a>
              <ul className="dropdown-menu dropdown-menu-end">
                <li><a className="dropdown-item" href="#">Настройки</a></li>
                <li><button className="dropdown-item" onClick={onLogout}>Выход</button></li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
