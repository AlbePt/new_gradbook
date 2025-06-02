// components/StatusBadge.jsx
import styles from './StatusBadge.module.css';

export default function StatusBadge({ status }) {
  return (
    <span className={`${styles.badge} ${styles[status]}`}>
      {status === 'active' ? 'Активный' : 'Архивный'}
    </span>
  );
}
