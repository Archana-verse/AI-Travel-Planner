
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, MapPin, Plane, Building, Calendar, MessageCircle, Moon, Sun } from 'lucide-react';

const Navbar = () => {
  const location = useLocation();
  const [darkMode, setDarkMode] = React.useState(false);
  
  const navItems = [
    { name: 'Home', path: '/', icon: Home },
    { name: 'Plan', path: '/plan', icon: MapPin },
    { name: 'Flights', path: '/flights', icon: Plane },
    { name: 'Hotels', path: '/hotels', icon: Building },
    { name: 'Itinerary', path: '/itinerary', icon: Calendar },
    { name: 'Chat', path: '/chat', icon: MessageCircle },
  ];

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    document.documentElement.classList.toggle('dark');
  };

  return (
    <nav className="bg-card border-b border-border px-6 py-4 theme-transition sticky top-0 z-50 backdrop-blur-sm bg-card/95">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <Link to="/" className="flex-center hover-lift">
          <div className="w-10 h-10 rounded-full shadow-lg overflow-hidden mr-3">
            <img 
              src="/lovable-uploads/8046535e-962b-4e80-b6c5-36482f2a916b.png" 
              alt="Indian Flag" 
              className="w-full h-full object-cover"
            />
          </div>
          <span className="text-2xl font-semibold tracking-tight relative">
            <span className="text-orange-500 drop-shadow-sm">Ra</span>
            <span className="text-gray-700 dark:text-gray-200 drop-shadow-sm">a</span>
            <span className="text-gray-700 dark:text-gray-200 drop-shadow-sm">h</span>
            <span className="text-green-600 drop-shadow-sm">i</span>
          </span>
        </Link>
        
        <div className="flex items-center space-x-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            
            return (
              <Link
                key={item.name}
                to={item.path}
                className={`flex-center px-4 py-2.5 rounded-xl font-medium transition-all duration-200 ${
                  isActive
                    ? 'gradient-saffron text-white shadow-lg'
                    : 'text-muted-foreground hover:bg-accent hover:text-primary'
                }`}
              >
                <Icon size={18} />
                <span>{item.name}</span>
              </Link>
            );
          })}
        </div>
        
        <button 
          onClick={toggleDarkMode}
          className="p-2.5 rounded-xl hover:bg-accent transition-all duration-200 hover-lift"
        >
          {darkMode ? (
            <Sun className="w-5 h-5 text-muted-foreground hover:text-primary transition-colors" />
          ) : (
            <Moon className="w-5 h-5 text-muted-foreground hover:text-primary transition-colors" />
          )}
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
