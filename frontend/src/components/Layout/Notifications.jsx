import React from 'react';
import { useSelector } from 'react-redux';

export default function Notifications() {
  const toasts = useSelector(state => state.notifications.items);
  return (
    <div className="toast-container">
      {toasts.map(t => (
        <div key={t.id} className={`toast ${t.type}`}>{t.message}</div>
      ))}
    </div>
  );
}
