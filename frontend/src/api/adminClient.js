import axios from 'axios';

// Use the backend API running on port 8000. Requests go directly to the
// FastAPI server rather than the Parcel dev server to avoid 405 errors.
const adminClient = axios.create({
  baseURL: 'http://localhost:8000',
});

adminClient.interceptors.response.use(
  res => res,
  err => Promise.reject(err)
);

export default adminClient;
