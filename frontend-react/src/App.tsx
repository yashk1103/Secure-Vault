import React, { useState } from 'react';
import './App.css';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import Dashboard from './components/Dashboard';
import Header from './components/Header';

export interface User {
  id: number;
  username: string;
}

type ViewType = 'login' | 'register' | 'dashboard';

const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<ViewType>('login');
  const [user, setUser] = useState<User | null>(null);

  const handleLogin = (userData: User): void => {
    setUser(userData);
    setCurrentView('dashboard');
  };

  const handleLogout = (): void => {
    setUser(null);
    setCurrentView('login');
  };

  const handleRegister = (): void => {
    setCurrentView('login');
  };

  const handleAccountDeleted = (): void => {
    setUser(null);
    setCurrentView('login');
  };

  return (
    <div className="app">
      <Header user={user} onLogout={handleLogout} />
      
      <main className="main-content">
        {currentView === 'login' && (
          <LoginForm 
            onLogin={handleLogin} 
            onSwitchToRegister={() => setCurrentView('register')} 
          />
        )}
        
        {currentView === 'register' && (
          <RegisterForm 
            onRegister={handleRegister}
            onSwitchToLogin={() => setCurrentView('login')} 
          />
        )}
        
        {currentView === 'dashboard' && user && (
          <Dashboard user={user} onAccountDeleted={handleAccountDeleted} />
        )}
      </main>
    </div>
  );
};

export default App;
