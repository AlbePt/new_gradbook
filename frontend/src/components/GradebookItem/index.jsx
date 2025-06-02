// src/components/GradebookItem/index.jsx (обновленная версия)
import { Link } from 'react-router-dom';
import styles from './gradebookItem.module.css';

export default function GradebookItem({ gradebook }) {
  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <h2>{gradebook.name}</h2>
        <StatusBadge status={gradebook.status} />
      </div>
      
      <div className={styles.meta}>
        <span>Класс: {gradebook.class}</span>
        <span>Учеников: {gradebook.students.length}</span>
      </div>

      <ProgressBar 
        progress={gradebook.completion} 
        label={`Заполнено: ${gradebook.completion}%`}
      />

      <div className={styles.actions}>
        <Button variant="primary" to={`/grade/${gradebook.id}`}>
          Открыть
        </Button>
        <Button variant="secondary" to={`/grade/${gradebook.id}/edit`}>
          Редактировать
        </Button>
      </div>
    </div>
  );
}