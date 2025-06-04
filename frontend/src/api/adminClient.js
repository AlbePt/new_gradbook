import axios from 'axios';

const adminClient = axios.create({
  baseURL: '/api/admin',
});

adminClient.interceptors.response.use(
  res => res,
  err => Promise.reject(err)
);

export default adminClient;
