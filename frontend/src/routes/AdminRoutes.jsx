import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import RegionList from '../components/Entities/Region/RegionList.jsx';
import CityList from '../components/Entities/City/CityList.jsx';
import SchoolList from '../components/Entities/School/SchoolList.jsx';
import SubjectList from '../components/Entities/Subject/SubjectList.jsx';
import NotFound from '../pages/NotFound.jsx';

export default function AdminRoutes() {
  return (
    <Routes>
      <Route index element={<Navigate to="regions" replace />} />
      <Route path="regions" element={<RegionList />} />
      <Route path="cities" element={<CityList />} />
      <Route path="schools" element={<SchoolList />} />
      <Route path="subjects" element={<SubjectList />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
