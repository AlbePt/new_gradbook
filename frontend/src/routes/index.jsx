// src/routes/index.jsx
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import GradebookListPage from '../components/GradebookListPage';
import GradebookDetailPage from '../components/GradebookDetailPage';
import GradebookCreatePage from '../components/GradebookCreatePage';
import GradebookEditPage from '../components/GradebookEditPage';

const AppRoutes = () => (
  <Routes>
    <Route path="/" element={<GradebookListPage />} />
    <Route path="/grade/:id" element={<GradebookDetailPage />} />
    <Route path="/new" element={<GradebookCreatePage />} />
    <Route path="/grade/:id/edit" element={<GradebookEditPage />} />
  </Routes>
);

export default AppRoutes;