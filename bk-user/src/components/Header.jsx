import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Bell, ChevronDown } from 'lucide-react';
import styles from '../user_dashboard.module.css';

const Header = () => {
  const [showNotifications, setShowNotifications] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowNotifications(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const notifications = [
    { id: 1, text: "New appointment set by Admin", time: "10 mins ago", read: false },
    { id: 2, text: "Your lab results are ready to be viewed.", time: "1 hour ago", read: false },
    { id: 3, text: "Reminder: Upcoming consultation tomorrow.", time: "1 day ago", read: true },
  ];

  const unreadCount = notifications.filter(n => !n.read).length;

  return (
    <nav className={styles.navbar}>
      <div className={styles.navbar__logo}>
        <div className={styles['navbar__logo-icon']}></div>
        <span>BantayKalusugan</span>
      </div>
      <div className={styles.navbar__menu}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginRight: '16px' }}>
          
          <div className={styles['notifications-wrapper']} ref={dropdownRef}>
            <button 
              className={`${styles['top-header__btn']} ${styles['top-header__btn--icon']}`}
              onClick={() => setShowNotifications(!showNotifications)}
            >
              <Bell size={20} color="#4b5563" />
              {unreadCount > 0 && <span className={styles['notifications-badge']}>{unreadCount}</span>}
            </button>
            
            {showNotifications && (
              <div className={styles['notifications-dropdown']}>
                <div className={styles['notifications-header']}>
                  <h3 className={styles['notifications-title']}>Notifications</h3>
                  <button className={styles['notifications-mark-all']}>Mark all as read</button>
                </div>
                <div className={styles['notifications-list']}>
                  {notifications.map(notif => (
                    <div key={notif.id} className={`${styles['notification-item']} ${notif.read ? styles['notification-item--read'] : styles['notification-item--unread']}`}>
                      {!notif.read && <div className={styles['notification-dot']}></div>}
                      <div className={styles['notification-content']}>
                        <p className={styles['notification-text']}>{notif.text}</p>
                        <span className={styles['notification-time']}>{notif.time}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

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
