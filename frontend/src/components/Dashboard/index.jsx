// components/Dashboard/index.jsx
import { useGradebooks } from '../../hooks/useGradebooks';

export default function Dashboard() {
  const { gradebooks } = useGradebooks();
  
  const stats = {
    total: gradebooks.length,
    active: gradebooks.filter(g => g.status === 'active').length,
    archived: gradebooks.filter(g => g.status === 'archived').length
  };

  return (
    <div className={styles.dashboard}>
      <div className={styles.statCard}>
        <h3>Всего журналов</h3>
        <div className={styles.value}>{stats.total}</div>
      </div>
      <div className={styles.statCard}>
        <h3>Активных</h3>
        <div className={styles.value}>{stats.active}</div>
      </div>
      <div className={styles.statCard}>
        <h3>Архивных</h3>
        <div className={styles.value}>{stats.archived}</div>
      </div>
    </div>
  );
}