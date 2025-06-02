// src/components/Navbar/index.jsx
import { Link } from 'react-router-dom';
import styles from './navbar.module.css';

export default function Navbar() {
  return (
    <nav className={styles.navbar}>
      <div className={styles.logo}>Gradebook</div>
      <div className={styles.links}>
        <Link to="/" className={styles.link}>Журналы</Link>
        <Link to="/new" className={styles.button}>Создать журнал</Link>
      </div>
    </nav>
  );
}