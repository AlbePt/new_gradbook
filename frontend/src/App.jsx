import React, { Suspense, lazy } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { CircularProgress } from '@mui/material';
import PageLayout from './components/Layout/PageLayout.jsx';
import './styles/globals.css';

const LoginPage = lazy(() => import('./pages/LoginPage.jsx'));
const AdminDashboard = lazy(() => import('./pages/AdminDashboard.jsx'));
const NotFound = lazy(() => import('./pages/NotFound.jsx'));

export default function App() {
  return (
    <BrowserRouter>
      <PageLayout>
        <Suspense fallback={<CircularProgress />}>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/admin/*" element={<AdminDashboard />} />
            <Route path="/" element={<div>Home</div>} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Suspense>
      </PageLayout>
    </BrowserRouter>
  );
}
