// src/App.jsx
import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import { useSelector, useDispatch } from 'react-redux';
import store from './store';
import AppRoutes from './routes';
import Navbar from './components/Navbar';
import Notification from './components/Notification';
import { clearError } from './store/gradebookSlice'; // Теперь импорт корректен

function AppWrapper() {
  const { status, error } = useSelector(state => state.gradebooks);
  const dispatch = useDispatch();

  const handleCloseNotification = () => {
    dispatch(clearError()); // Диспатчим action для очистки ошибки
  };

  return (
    <>
      <Navbar />
      <main className="main-content">
        <AppRoutes />
      </main>
      
      {status === 'failed' && (
        <Notification 
          type="error" 
          message={error} 
          onClose={handleCloseNotification}
        />
      )}
    </>
  );
}

function App() {
  return (
    <Provider store={store}>
      <BrowserRouter>
        <AppWrapper />
      </BrowserRouter>
    </Provider>
  );
}

export default App;