// src/api/gradebookApi.js
import client from './client';
import axios from 'axios'

export const getGradebooks = () => client.get('/grades/');
export const getGradebook = id => client.get(`/grades/${id}`);
export const createGradebook = data => client.post('/grades/', data);
export const updateGradebook = (id, data) =>
  client.put(`/grades/${id}`, data);
export const deleteGradebook = id =>
  client.delete(`/grades/${id}`);

export const fetchGrades      = () => axios.get('/grades/')
export const fetchStudents    = () => axios.get('/students')
export const fetchSubjects    = () => axios.get('/subjects')
export const fetchTeachers    = () => axios.get('/teachers')