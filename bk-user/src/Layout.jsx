import React from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';
import Header from './components/Header.jsx';
import Sidebar from './components/Sidebar.jsx';

const Layout = ({ heroLabel, heroTitle, heroDesc, children }) => {
  const [isHeroMinimized, setIsHeroMinimized] = React.useState(() => {
    return localStorage.getItem('heroMinimized') === 'true';
  });

  const toggleHero = () => {
    const newState = !isHeroMinimized;
    setIsHeroMinimized(newState);
    localStorage.setItem('heroMinimized', String(newState));
  };

  return (
    <div className="page">
      <Header />
      <Sidebar />

      <section className={`hero ${isHeroMinimized ? 'hero--minimized' : ''}`}>
        <button 
          onClick={toggleHero}
          className="hero__toggle"
          aria-label={isHeroMinimized ? "Expand banner" : "Minimize banner"}
        >
          {isHeroMinimized ? <ChevronDown size={20} /> : <ChevronUp size={20} />}
        </button>

        <div className={`hero__content ${isHeroMinimized ? 'hero__content--minimized' : 'hero__content--visible'}`}>
          <div className="hero__text-wrapper">
             {!isHeroMinimized && heroLabel && <div className="hero__label">{heroLabel}</div>}
             <h2 className={`hero__title ${isHeroMinimized ? 'hero__title--minimized' : ''}`}>{heroTitle}</h2>
             {!isHeroMinimized && heroDesc && <p className="hero__desc">{heroDesc}</p>}
          </div>
        </div>
      </section>

      <div className="container">
        {children}
      </div>
    </div>
  );
};

export default Layout;
