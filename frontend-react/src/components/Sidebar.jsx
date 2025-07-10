import React from 'react'

function Sidebar() {
  return (
    <aside id="sidebar" className="sidebar offcanvas-lg offcanvas-start text-bg-dark flex-shrink-0 p-3" tabIndex="-1">
      <div className="offcanvas-body">
        <a href="#" className="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-white text-decoration-none">
          <i className="bi bi-speedometer2 me-2 fs-4"></i>
          <span className="fs-5">Навигация</span>
        </a>
        <hr />
        <ul className="nav nav-pills flex-column mb-auto">
          <li className="nav-item"><a href="#" className="nav-link text-white active"><i className="bi bi-bar-chart me-2"></i>Отчёты</a></li>
          <li><a href="#" className="nav-link text-white"><i className="bi bi-people me-2"></i>Ученики</a></li>
          <li><a href="#" className="nav-link text-white"><i className="bi bi-book me-2"></i>Предметы</a></li>
          <li><a href="#" className="nav-link text-white"><i className="bi bi-card-checklist me-2"></i>Оценки</a></li>
          <li><a href="#" className="nav-link text-white"><i className="bi bi-gear me-2"></i>Настройки</a></li>
        </ul>
        <hr />
        <small className="text-white-50">v0.1.0 • 2025</small>
      </div>
    </aside>
  )
}

export default Sidebar
