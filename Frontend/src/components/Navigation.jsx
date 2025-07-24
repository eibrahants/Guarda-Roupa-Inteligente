import React from 'react';
const Navigation = ({ currentView, onViewChange }) => {
  const navItems = [
    { id: 'sugestao', label: 'Sugestão IA', icon: '' },
    { id: 'guarda-roupa', label: 'Guarda-roupa', icon: '' }
  ];
  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          <div className="logo">
            <span>👕</span>
            <span>Guarda Roupa Inteligente</span>
          </div>
          <div className="nav-buttons">
            {navItems.map(item => (
              <button
                key={item.id}
                onClick={() => onViewChange(item.id)}
                className={`nav-btn ${currentView === item.id ? 'active' : ''}`}
              >
                <span>{item.icon}</span>
                <span>{item.label}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </header>
  );
};
export default Navigation;
