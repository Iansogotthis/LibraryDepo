import { useState, useEffect } from 'react';
import axios from 'axios';

const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    axios.get('/api/current_user')
      .then(response => setIsAuthenticated(true))
      .catch(() => setIsAuthenticated(false));
  }, []);

  return { isAuthenticated };
};

export default useAuth;
