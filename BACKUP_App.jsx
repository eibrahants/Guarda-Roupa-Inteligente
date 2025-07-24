import React, { useState } from 'react';
import Navigation from './components/Navigation';
import SugestaoRoupa from './components/SugestaoRoupa';
import RoupasList from './components/RoupasList';

function App() {
  const [currentView, setCurrentView] = useState('sugestao');
  
  const renderCurrentView = () => {
    switch (currentView) {
      case 'sugestao':
        return <SugestaoRoupa />;
      case 'guarda-roupa':
        return <RoupasList />;
      default:
        return <SugestaoRoupa />;
    }
  };
  
  return (
    <div>
      <Navigation 
        currentView={currentView} 
        onViewChange={setCurrentView} 
      />
      <main>
        {renderCurrentView()}
      </main>
    </div>
  );
}

export default App;
