// src/index.jsx
import React from 'react';
import { createRoot } from 'react-dom/client'; // Изменяем импорт
import App from './App';
import './styles/globals.css';

const root = createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);