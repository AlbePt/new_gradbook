import React from 'react';
import { Routes, Route } from 'react-router-dom';
import DashboardPage from '../pages/DashboardPage.jsx';
import CityList from '../components/Entities/City/CityList.jsx';
import SchoolList from '../components/Entities/School/SchoolList.jsx';
import NotFound from '../pages/NotFound.jsx';

export default function AdminRoutes() {
  return (
    <Routes>
      <Route index element={<DashboardPage />} />
      <Route path="cities" element={<CityList />} />
      <Route path="schools" element={<SchoolList />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
