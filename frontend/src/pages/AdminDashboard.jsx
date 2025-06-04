import React from 'react';
import AdminRoutes from '../routes/AdminRoutes.jsx';
import Sidebar from '../components/Layout/Sidebar.jsx';
import Notifications from '../components/Layout/Notifications.jsx';

export default function AdminDashboard() {
  return (
    <div className="admin-container">
      <Sidebar />
      <div className="admin-content">
        <AdminRoutes />
      </div>
      <Notifications />
    </div>
  );
}
