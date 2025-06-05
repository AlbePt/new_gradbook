import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import SubjectList from '../components/Entities/Subject/SubjectList.jsx';
import NotFound from '../pages/NotFound.jsx';

export default function AdminRoutes() {
  return (
    <Routes>
      <Route index element={<Navigate to="subjects" replace />} />
      <Route path="subjects" element={<SubjectList />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
