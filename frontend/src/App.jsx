import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Layout/Header.jsx';
import LoginPage from './pages/LoginPage.jsx';
import AdminDashboard from './pages/AdminDashboard.jsx';
import NotFound from './pages/NotFound.jsx';
import './styles/globals.css';

export default function App() {
  return (
    <>
      <Header />
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/admin/*" element={<AdminDashboard />} />
        <Route path="/" element={<div>Home</div>} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </>
  );
}
