import React, { useState } from 'react';
import DataTable from '../components/GovStyle/DataTable.jsx';

export default function DashboardPage() {
  const [tab, setTab] = useState('data');

  return (
    <div>
      <h1>Название страницы</h1>
      <div className="tabs">
        <button
          className={tab === 'data' ? 'active' : ''}
          onClick={() => setTab('data')}
        >
          Данные
        </button>
        <button
          className={tab === 'settings' ? 'active' : ''}
          onClick={() => setTab('settings')}
        >
          Настройки
        </button>
      </div>
      <button className="add-btn">+ Добавить сущность</button>
      {tab === 'data' && <DataTable />}
      {tab === 'settings' && <p>Настройки недоступны</p>}
    </div>
  );
}
