// components/SearchInput.jsx
import styles from './searchInput.module.css';
import { FaSearch } from 'react-icons/fa';  // импорт иконки поиска

export default function SearchInput({ value, onChange, placeholder }) {
  return (
    <div className={styles.searchContainer}>
      <input
        type="text"
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className={styles.input}
      />
      <FaSearch className={styles.icon} />
    </div>
  );
}

