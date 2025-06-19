import React from 'react';
import AdminRoutes from '../routes/AdminRoutes.jsx';
import Sidebar from '../components/Layout/Sidebar.jsx';
import Notifications from '../components/Layout/Notifications.jsx';

export default function AdminDashboard() {
  return (
    <div className="admin-wrapper d-flex">
      <div className="admin-sidebar">
        <Sidebar />
      </div>
      <div className="admin-content-scroll flex-grow-1">
        <AdminRoutes />
        <Notifications />
      </div>
    </div>
  );
}
