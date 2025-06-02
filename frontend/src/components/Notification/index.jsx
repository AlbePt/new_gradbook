// src/components/Notification/index.jsx
import { useEffect } from 'react';
import styles from './notification.module.css';

export default function Notification({ message, type, onClose }) {
  useEffect(() => {
    const timer = setTimeout(onClose, 3000);
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div className={`${styles.notification} ${styles[type]}`}>
      {message}
    </div>
  );
}