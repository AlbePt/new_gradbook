// components/ProgressBar.jsx
import styles from './ProgressBar.module.css';

export default function ProgressBar({ progress, label }) {
  return (
    <div className={styles.progressContainer}>
      <div className={styles.bar}>
        <div
          className={styles.fill}
          style={{ width: `${progress}%` }}
        />
      </div>
      <span className={styles.label}>{label}</span>
    </div>
  );
}
