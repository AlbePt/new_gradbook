// components/FilterDropdown.jsx
import styles from './FilterDropdown.module.css';

export default function FilterDropdown({ options, selectedValue, onSelect }) {
  return (
    <select
      value={selectedValue}
      onChange={e => onSelect(e.target.value)}
      className={styles.select}
    >
      {options.map(opt => (
        <option key={opt.value} value={opt.value}>
          {opt.label}
        </option>
      ))}
    </select>
  );
}
