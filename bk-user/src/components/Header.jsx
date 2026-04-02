import React from 'react';
import { Link } from 'react-router-dom';
import { Bell, ChevronDown } from 'lucide-react';
import styles from '../user_dashboard.module.css';

const Header = () => {
  return (
    <nav className={styles.navbar}>
      <div className={styles.navbar__logo}>
        <div className={styles['navbar__logo-icon']}></div>
        <span>BantayKalusugan</span>
      </div>
      <div className={styles.navbar__menu}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginRight: '16px' }}>
          <button className={`${styles['top-header__btn']} ${styles['top-header__btn--icon']}`}>
            <Bell size={20} color="#4b5563" />
          </button>
          <Link to="/profile" className={styles['top-header__profile']}>
            <div className={styles['top-header__avatar']}>M</div>
            <span className={styles['top-header__name']}>Maria Santos</span>
            <ChevronDown size={16} color="#4b5563" />
          </Link>
        </div>
        <button className={`${styles.btn} ${styles['btn--outline-navy']} ${styles['btn--sm']}`}>Log Out</button>
      </div>
    </nav>
  );
};

export default Header;
