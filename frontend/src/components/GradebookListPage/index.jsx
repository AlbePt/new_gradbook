// components/GradebookListPage/index.jsx (обновленная версия)
import { useState } from 'react';
import SearchInput from '../SearchInput';
import StatusBadge from '../StatusBadge';
import ProgressBar from '../ProgressBar';

// Добавляем импорт FilterDropdown, который вам нужно создать в ../FilterDropdown.jsx
import FilterDropdown from '../FilterDropdown';

// Предполагаем, что useGradebooks — кастомный хук для получения данных, 
// если у вас его нет — замените или реализуйте
import useGradebooks from '../../hooks/useGradebooks'; 

// Импорт стилей (если используете CSS Modules или похожий подход)
import styles from './gradebookList.module.css';

export default function GradebookListPage() {
  const { gradebooks, status, error } = useGradebooks();
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('all');

  const filteredGradebooks = gradebooks.filter(gb => {
    const matchesSearch = gb.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filter === 'all' || gb.status === filter;
    return matchesSearch && matchesFilter;
  });

  if (status === 'loading') return <ProgressBar />;
  if (error) return <div>Ошибка загрузки данных: {error.message}</div>;

  return (
    <div className={styles.container}>
      <div className={styles.controls}>
        <SearchInput 
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Поиск по названию..."
        />
        <FilterDropdown
          options={[
            { value: 'all', label: 'Все журналы' },
            { value: 'active', label: 'Активные' },
            { value: 'archived', label: 'Архивные' }
          ]}
          selectedValue={filter}
          onSelect={setFilter}
        />
      </div>

      <div className={styles.list}>
        {filteredGradebooks.length === 0 
          ? <div>Журналы не найдены</div>
          : filteredGradebooks.map(gb => (
            <div key={gb.id} className={styles.gradebookItem}>
              <h3>{gb.name}</h3>
              <StatusBadge status={gb.status} />
              {/* Другие данные журнала */}
            </div>
          ))
        }
      </div>
    </div>
  );
}
