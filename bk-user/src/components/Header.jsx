import React from 'react';
import { Link } from 'react-router-dom';
import { Bell, ChevronDown } from 'lucide-react';

const Header = () => {
  return (
    <nav className="navbar">
      <div className="navbar__logo">
        <div className="navbar__logo-icon"></div>
        <span>BantayKalusugan</span>
      </div>
      <div className="navbar__menu">
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginRight: '16px' }}>
          <button className="top-header__btn top-header__btn--icon">
            <Bell size={20} color="#4b5563" />
          </button>
          <Link to="/profile" className="top-header__profile">
            <div className="top-header__avatar">M</div>
            <span className="top-header__name">Maria Santos</span>
            <ChevronDown size={16} color="#4b5563" />
          </Link>
        </div>
        <button className="btn btn--outline-navy btn--sm">Log Out</button>
      </div>
    </nav>
  );
};

export default Header;
